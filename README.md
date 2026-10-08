# Economics revision room

A static Class XII Economics study site: 12 Macro chapters and the six uploaded IED chapters. Short explanations, key points, recall cards, 14 exam diagram models, CBSE-style practice.

**Live site:** https://tannmay-python.github.io/economics-revision-room/

## Included

- 150 concept lessons with key concepts from the supplied textbook and boxes.
- 357 original practice questions: 146 MCQs, 46 numericals and 165 theory/application questions.
- MCQ checking, worked answers, chapter/type/search filters, sets of 20 questions and ten-question sprints.
- Browser-local progress; no account, analytics or external runtime dependencies.

IED covers the pre-independence economy, 1950–1990, reforms, human capital, rural development and employment. Environment/sustainable development and the India–China–Pakistan comparison were not supplied as chapters and are not included. Historical statistics retain their textbook context.

Practice formats were informed by official CBSE sample papers and marking schemes linked in the site's Sources & coverage section. Practice questions and mark targets are original, not official questions or predictions.

## Run and deploy

Serve `dist` with any static server, for example `python3 -m http.server 8765 --directory dist`. Run `python3 scripts/audit.py` to check chapter coverage, answer keys and asset references. Pushing to `main` runs the audit and deploys `dist` through GitHub Actions to GitHub Pages.

`dist/content.js` is the publishable content. Scripts document the local extraction/editorial workflow; the original HEIC/PDF files and OCR intermediates are outside this repository. Re-running editorial transformation scripts is not needed to deploy.

Textbook photographs are excluded from the published site. Teaching diagrams are generated directly as SVG.
