# Neil Patel: Professional Portfolio

A static, GitHub Pages–ready professional portfolio highlighting Neil Patel’s software engineering background, robotics experience, projects, and technical resources. No build process, JavaScript, or paid services are required.

## Publish on GitHub Pages

1. Create a GitHub repository (a public repository is the simplest option for free GitHub Pages hosting).
2. Upload the **contents** of this folder to the repository root, not inside an additional `Portfolio` folder. Include `index.html`, `styles.css`, `llm-training-costs.html`, `LLM-Training-Costs.pdf`, `LLM-Training-Costs.png`, `llm-training-explanation.html`, `LLM-Training-Explanation.pdf`, `explainable-ai.html`, `Explainable-AI.pdf`, `Explainable-AI.png`, `explainable-ai-explanation.html`, `Explainable-AI-Explanation.pdf`, the `explainable-ai-assets/` folder, `neural-network-components.html`, `Neural-Network-Components.pdf`, the `neural-network-assets/` folder, `ML-Algorithm-Framework.pdf`, `ML-Algorithm-Framework.png`, and `.nojekyll`. Keep the deliverable filenames and capitalization unchanged.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the branch containing your files (usually `main`) and the **/ (root)** folder, then select **Save**.
6. Wait for the Pages deployment to finish. GitHub displays the published URL in Settings → Pages. A project repository typically uses `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`.
7. Visit the published URL and test the PDF and PNG downloads and the “Open the original PDF” link.

All local asset links are relative, so the site works under a repository subpath as well as a user-site domain. No custom domain is needed. Published site content, the PDF, and the PNG are public; review them for private information before uploading.

## Before publishing

- The bio introduces Neil Patel as a software engineer at a robotics company that develops sanding robots. Add specific career aspirations later if desired.
- In `index.html`, update the page title and description if desired.
- The featured framework documents the author’s supplied production process: ChatGPT/Codex-assisted synthesis and layout, Python/ReportLab PDF generation, and Poppler rendering and visual checks. It is a conceptual reference, not a report of trained models, datasets, experiments, or measured results.
- The site is presented as a general professional portfolio. Machine learning terminology is specific to the featured framework, not the overall site branding.

## Contents

- `index.html`: portfolio, bio, personal value proposition, artifact index, both artifacts with their artifact information, accessible summaries, and references.
- `styles.css`: responsive layout, keyboard focus states, and reduced-motion support.
- `ML-Algorithm-Framework.pdf`: the original, unchanged vector artifact.
- `ML-Algorithm-Framework.png`: a high-resolution rendering of the PDF for image-based display. The repository copy was rendered at 200 DPI using PyMuPDF; the portfolio describes the author’s original Poppler-based workflow.
- `neural-network-components.html`: the second artifact, a 12-slide neural network presentation. It scrolls as a page, has a full-screen **Present** mode (arrow keys, Esc to exit), and prints one slide per landscape page. Its styles and scripts are self-contained.
- `Neural-Network-Components.pdf`: the presentation exported from Chrome (12 pages, 13.333 × 7.5 in).
- `neural-network-assets/`: TensorFlow Playground decision-boundary images used in the slides and the slide-2 preview image used on the home page.
- `llm-training-costs.html`: the third artifact, a one-slide infographic on LLM training stages, resources, and model costs. It has a full-screen **Present** mode and prints to a single landscape page. Adding `?capture` to the URL hides the page controls for image export.
- `LLM-Training-Costs.pdf` and `LLM-Training-Costs.png`: the infographic exported from Chrome (13.333 × 7.5 in; 1920 × 1080).
- `llm-training-explanation.html` and `LLM-Training-Explanation.pdf`: the explanatory document for the infographic, with full references.
- `explainable-ai.html`: the fourth artifact, a single-page infographic on explainable AI, validation and metrics, and current lab techniques. It reflows on phones and prints to one tall page. Adding `?capture` to the URL hides the page controls for image export.
- `Explainable-AI.pdf` and `Explainable-AI.png`: the infographic exported from headless Chrome (1200 × 3520 px page; 2400 px wide PNG).
- `explainable-ai-assets/explainable-ai-preview.png`: the top of the infographic, used as the home page preview.
- `explainable-ai-explanation.html` and `Explainable-AI-Explanation.pdf`: the explanatory document, with the infographic embedded and full references.
- `.nojekyll`: serves the static site without Jekyll processing.

Each artifact includes Title, Introduction, Description, Objective, Process, Tools and Technologies Used, Value Proposition, Unique Value, Relevance, a usage note, and References.

### Regenerating the neural network PDF

After editing `neural-network-components.html`, re-export the PDF with headless Chrome from this folder:

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --no-pdf-header-footer --virtual-time-budget=5000 --print-to-pdf="%CD%\Neural-Network-Components.pdf" "%CD%\neural-network-components.html"
```

Adding `?slide=2` to the presentation URL shows a single slide full-window, which is how the preview image was captured.

## Preview locally

Open `index.html` in a web browser. No installation is needed. For a local HTTP preview on Windows, run:

```cmd
py -m http.server 8000
```

Then visit `http://localhost:8000`. Stop the preview with Ctrl+C.

## Add a project or resource

1. Add the finished deliverable to the repository (use a descriptive filename).
2. Add a detailed entry in `index.html` with a unique section ID and a working deliverable link. Use the featured framework’s structure as a starting point.
3. Update navigation links as needed so visitors can find the new work.
4. Include only work you can share publicly; do not publish confidential employer information.

Google Fonts loads DM Sans and Manrope from Google’s font service. System fonts are used if that service is unavailable; all substantive content and the PDF remain local. To avoid requests to Google entirely, remove the first `@import` line in `styles.css`.
