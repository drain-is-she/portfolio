# Priyanshi Goyal · The Project Express

A responsive portfolio with digital typography, an illustrated project train, technical writing, and a 3D modelling gallery. Built with semantic HTML, CSS, and vanilla JavaScript, hosted on GitHub Pages.

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
- Scrolling makes the section under the viewport's midpoint colorful. All other sections remain grayscale. When the project section is current, its original color illustrations appear; the other sections show the grayscale versions.
- A pause control and the system's reduced-motion preference are respected.
- Field notes use a native dialog with Escape dismissal, a close button, and focus restoration.

## Writing and 3D work

- The writing window presents five LeetCode articles as accessible tabs. Arrow keys, Home, and End switch between them; each preview links to the full post.
- Each ZIP image set appears in one 3D gallery card with previous/next controls. The three local videos play with native controls and sound, and opening one pauses another.
- The supplied videos were rotated for upright display. The headphones clip is shown as a portrait video within its gallery window, with a further 180° rotation applied to its current orientation. Their AAC audio was preserved. Posters are still frames from those same videos.
- The 3D media is grayscale outside its section and appears in color while that section is current. The original ZIPs and videos remain on the user's desktop; the website serves only the selected images and web-ready copies.

## Edit content

- `index.html`: introduction, projects, experience, skills, writing, 3D work, and contact links.
- `script.js`: project notes, tabs, image galleries, and scroll behavior.
- `styles.css` and `sections.css`: typography, the train, the new sections, and responsive styles.
- `assets/3d/`: user-supplied image sets and upright, audio-preserving copies of the three videos.
- The original CV is kept locally in the ignored `.private/` directory and is excluded from the public repository and deployment.
- `scripts/generate_assets.py`: reproducible, original illustrated project GIFs and posters. Requires Pillow only if regenerating images.
- `assets/color/`: the original color GIFs and posters from the portfolio's first commit. The generated grayscale counterparts stay in `assets/`; keep both sets together when changing project artwork.

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

The train illustrations are original; the 3D media was supplied by Priyanshi. JetBrains Mono is self-hosted under the SIL Open Font License; notices are in `assets/fonts/`.
