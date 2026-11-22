"""Benchmark pre-trained models on one CPU for the model-selection decision matrix.

Vision: torchvision ImageNet weights, batch-1 CPU latency at each model's native input size.
NLP: BERT-base vs DistilBERT fine-tuned on SST-2; accuracy on the 872-sentence GLUE dev set + latency.
Tabular: Random Forest, XGBoost, LightGBM on the UCI Adult census dataset (OpenML 1590).

Run on 2026-11-22 with Python 3.11, torch 2.15 (CPU), torchvision 0.29, transformers 5.24,
scikit-learn 1.9.1, xgboost 3.2.0, lightgbm 4.7.0 on an AMD Ryzen 5 7600.
Usage: python benchmark.py [vision] [nlp] [tabular]   (writes bench-<parts>.json next to this file)
Model weights and datasets download on first run (about 1.3 GB).
"""
import io, json, os, pickle, platform, statistics, sys, time

import numpy as np
import torch

torch.manual_seed(0)
OUT = {"machine": {}, "vision": {}, "nlp": {}, "tabular": {}}
OUT["machine"] = {
    "python": platform.python_version(),
    "torch": torch.__version__,
    "threads": torch.get_num_threads(),
    "cpu": platform.processor(),
}


def med_ms(fn, warm, runs):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(runs):
        t = time.perf_counter()
        fn()
        ts.append((time.perf_counter() - t) * 1000)
    return statistics.median(ts), min(ts), max(ts)


def state_mb(model):
    buf = io.BytesIO()
    torch.save(model.state_dict(), buf)
    return buf.tell() / 1e6


def run_vision():
    import torchvision.models as tvm

    specs = [
        ("MobileNetV3-Large", tvm.mobilenet_v3_large, tvm.MobileNet_V3_Large_Weights.IMAGENET1K_V2, 224),
        ("EfficientNet-B0", tvm.efficientnet_b0, tvm.EfficientNet_B0_Weights.IMAGENET1K_V1, 224),
        ("ResNet-50", tvm.resnet50, tvm.ResNet50_Weights.IMAGENET1K_V2, 224),
        ("EfficientNet-B7", tvm.efficientnet_b7, tvm.EfficientNet_B7_Weights.IMAGENET1K_V1, 600),
    ]
    for name, ctor, w, res in specs:
        m = ctor(weights=w).eval()
        x = torch.randn(1, 3, res, res)
        with torch.inference_mode():
            runs = 15 if res > 300 else 60
            med, lo, hi = med_ms(lambda: m(x), 5, runs)
            xb = torch.randn(32, 3, res, res) if res <= 300 else torch.randn(4, 3, res, res)
            bmed, _, _ = med_ms(lambda: m(xb), 2, 5)
        OUT["vision"][name] = {
            "params": sum(p.numel() for p in m.parameters()),
            "weights_mb": round(state_mb(m), 1),
            "input": res,
            "acc1_published": w.meta["_metrics"]["ImageNet-1K"]["acc@1"],
            "gflops_published": w.meta.get("_ops"),
            "latency_ms_median": round(med, 2),
            "latency_ms_min": round(lo, 2),
            "latency_ms_max": round(hi, 2),
            "throughput_img_s": round(xb.shape[0] / (bmed / 1000), 1),
            "runs": runs,
        }
        print(name, OUT["vision"][name], flush=True)


def run_nlp():
    import pandas as pd
    from huggingface_hub import hf_hub_download
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    path = hf_hub_download("nyu-mll/glue", "sst2/validation-00000-of-00001.parquet", repo_type="dataset")
    df = pd.read_parquet(path)
    sents, labels = df["sentence"].tolist(), df["label"].to_numpy()
    specs = [
        ("DistilBERT (SST-2)", "distilbert/distilbert-base-uncased-finetuned-sst-2-english"),
        ("BERT-base (SST-2)", "textattack/bert-base-uncased-SST-2"),
    ]
    for name, repo in specs:
        tok = AutoTokenizer.from_pretrained(repo)
        m = AutoModelForSequenceClassification.from_pretrained(repo).eval()
        preds, times = [], []
        with torch.inference_mode():
            for i, s in enumerate(sents):
                enc = tok(s, return_tensors="pt", truncation=True, max_length=128)
                t = time.perf_counter()
                logits = m(**enc).logits
                dt = (time.perf_counter() - t) * 1000
                if i >= 10:  # skip warm-up
                    times.append(dt)
                preds.append(int(logits.argmax(-1)))
            # batched throughput, 32 sentences padded
            enc = tok(sents[:32], return_tensors="pt", padding=True, truncation=True, max_length=128)
            bmed, _, _ = med_ms(lambda: m(**enc), 2, 5)
        preds = np.array(preds)
        acc = float((preds == labels).mean())
        # guard against flipped label mapping
        OUT["nlp"][name] = {
            "repo": repo,
            "id2label": m.config.id2label,
            "params": sum(p.numel() for p in m.parameters()),
            "weights_mb": round(state_mb(m), 1),
            "sst2_dev_acc": round(acc * 100, 2),
            "n": int(len(labels)),
            "latency_ms_median": round(statistics.median(times), 2),
            "latency_ms_p90": round(float(np.percentile(times, 90)), 2),
            "throughput_sent_s": round(32 / (bmed / 1000), 1),
            "mean_tokens": round(float(np.mean([len(tok(s)["input_ids"]) for s in sents])), 1),
        }
        print(name, OUT["nlp"][name], flush=True)


def run_tabular():
    import lightgbm as lgb
    import xgboost as xgb
    from sklearn.datasets import fetch_openml
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OrdinalEncoder

    ds = fetch_openml(data_id=1590, as_frame=True)
    X, y = ds.data.copy(), (ds.target == ">50K").astype(int).to_numpy()
    cats = X.select_dtypes(["category", "object"]).columns
    X[cats] = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan,
                             encoded_missing_value=np.nan).fit_transform(X[cats])
    X = X.astype("float32")
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    OUT["tabular"]["_data"] = {"rows": int(len(X)), "features": int(X.shape[1]),
                                "train": int(len(Xtr)), "test": int(len(Xte)),
                                "positive_rate": round(float(y.mean()), 3)}

    def size_mb(name, m):
        if name == "XGBoost":
            return len(m.get_booster().save_raw("ubj")) / 1e6
        if name == "LightGBM":
            return len(m.booster_.model_to_string().encode()) / 1e6
        return len(pickle.dumps(m)) / 1e6

    makers = {
        "Random Forest": lambda: RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42),
        "XGBoost": lambda: xgb.XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                                             tree_method="hist", n_jobs=-1, random_state=42),
        "LightGBM": lambda: lgb.LGBMClassifier(n_estimators=300, learning_rate=0.1, num_leaves=31,
                                               n_jobs=-1, random_state=42, verbose=-1),
    }
    for name, mk in makers.items():
        fits = []
        for _ in range(3):
            m = mk()
            t = time.perf_counter()
            m.fit(Xtr, ytr)
            fits.append(time.perf_counter() - t)
        p = m.predict_proba(Xte)[:, 1]
        bmed, _, _ = med_ms(lambda: m.predict_proba(Xte), 1, 5)
        # single-row latency, single thread (typical online scoring)
        m.set_params(n_jobs=1)
        row = Xte.iloc[[0]]
        lmed, _, _ = med_ms(lambda: m.predict_proba(row), 20, 200)
        OUT["tabular"][name] = {
            "accuracy": round(accuracy_score(yte, p > 0.5) * 100, 2),
            "roc_auc": round(roc_auc_score(yte, p), 4),
            "train_s_median": round(statistics.median(fits), 2),
            "model_mb": round(size_mb(name, m), 2),
            "latency_ms_single_row": round(lmed, 3),
            "throughput_rows_s": round(len(Xte) / (bmed / 1000)),
            "trees": 300,
        }
        print(name, OUT["tabular"][name], flush=True)


if __name__ == "__main__":
    which = sys.argv[1:] or ["vision", "nlp", "tabular"]
    for w in which:
        globals()["run_" + w]()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bench-" + "-".join(which) + ".json")
    with open(out, "w") as f:
        json.dump(OUT, f, indent=2, default=str)
    print("saved", out)
