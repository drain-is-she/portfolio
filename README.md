# Priyanshi Goyal · The Project Express

A responsive, monochrome portfolio with digital typography and an illustrated project train for AI research, generative models, and computer vision. Built with semantic HTML, CSS, and vanilla JavaScript, hosted on GitHub Pages.

## Run locally

```sh
npm run dev
```

Open http://127.0.0.1:4173. No package installation is needed. Node.js and Python 3 are required for the development and checking commands.

```sh
npm run check
npm run build
```

The build copies only public website files into `dist/`. The GitHub Actions workflow validates and deploys `dist/` on every push to `main`.

## The train

- Select a window or route stop; use the previous/next controls or left/right keys inside the gallery.
- Swipe the coaches on narrow screens. The nearest coach becomes active after scrolling settles.
- Only the active GIF plays. Other coaches show static posters. Motion also stops when the gallery leaves view or the tab is hidden.
- A pause control and the system's reduced-motion preference are respected.
- Field notes use a native dialog with Escape dismissal, a close button, and focus restoration.

## Edit content

- `index.html`: introduction, coach summaries, experience, skills, and contact links.
- `script.js`: project field notes and interaction behavior.
- `styles.css`: typography, colors, train illustration, responsive styles.
- The original CV is kept locally in the ignored `.private/` directory and is excluded from the public repository and deployment.
- `scripts/generate_assets.py`: reproducible, original illustrated project GIFs and posters. Requires Pillow only if regenerating images.

The three animations illustrate concepts; they are not recordings or model-generated outputs. Team contributions are attributed as described in the CV. Evaluation results retain limitations from the project READMEs. The CV and mule README report different dataset sizes, so no dataset-size claim is used on the portfolio.

## Content and design sources

- Priyanshi Goyal's supplied master CV (2026).
- [Mule Account Detection](https://github.com/drain-is-she/mule_account_detection)
- [LLM From Scratch](https://github.com/drain-is-she/LLM_from_scratch)
- [Diffusion](https://github.com/drain-is-she/Diffusion)
- [Portfolio showcase generator skill](https://github.com/infinyte/portfolio-showcase-generator/blob/main/SKILL.md): evidence-based project storytelling.
- [Vitalik Korolev](https://www.korolev.uk/): expressive typography and playful composition.
- [AI Engineer Portfolio reference](https://coffee-doge-66115487.figma.site/): content coverage.
- [Mitchell Sparrow](https://www.mitchellsparrow.com/): research, experience, and project structure.
- [Jakub's interface details](https://jakub.kr/writing/details-that-make-interfaces-feel-better): text wrapping, focus on interaction details, interruptible transitions.

All illustrations are original. JetBrains Mono is self-hosted under the SIL Open Font License; notices are in `assets/fonts/`.
