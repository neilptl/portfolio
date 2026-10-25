# Neil Patel: Professional Portfolio

A static, GitHub Pages–ready professional portfolio highlighting Neil Patel’s software engineering background, robotics experience, projects, and technical resources. No build process, JavaScript, or paid services are required.

## Publish on GitHub Pages

1. Create a GitHub repository (a public repository is the simplest option for free GitHub Pages hosting).
2. Upload the **contents** of this folder to the repository root, not inside an additional `Portfolio` folder. Include `index.html`, `styles.css`, `ML-Algorithm-Framework.pdf`, `ML-Algorithm-Framework.png`, and `.nojekyll`. Keep the deliverable filenames and capitalization unchanged.
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

- `index.html`: portfolio, bio, personal value proposition, first artifact, accessible algorithm summary, and references.
- `styles.css`: responsive layout, keyboard focus states, and reduced-motion support.
- `ML-Algorithm-Framework.pdf`: the original, unchanged vector artifact.
- `ML-Algorithm-Framework.png`: a high-resolution rendering of the PDF for image-based display. The repository copy was rendered at 200 DPI using PyMuPDF; the portfolio describes the author’s original Poppler-based workflow.
- `.nojekyll`: serves the static site without Jekyll processing.

The first artifact includes Title, Introduction, Description, Objective, Process, Tools and Technologies Used, Value Proposition, Unique Value, Relevance, How to Use the Guide, and References. The reference numbers match those in the PDF.

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
