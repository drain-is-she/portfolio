'use strict';

const projects = {
  mule: {
    number: '01', title: 'Mule Account Detection', role: 'Team project · Graph machine learning',
    summary: 'A fraud-risk research project that combines transaction behavior with the relationships between accounts. The system ranks potentially suspicious accounts for human review.',
    flow: ['Transactions', 'Behavioral features', 'GraphSAGE + LightGBM', 'Review queue'],
    sections: [
      ['The question', 'Can we find money mule accounts when individual transactions look ordinary? The project audited 25 candidate behavioral indicators, then focused on signals including early activity spikes, synchronized credits and debits, and threshold capping.'],
      ['What I worked on', 'As part of the team, I developed graph and tabular modeling workflows, engineered behavioral signals, and evaluated discrimination and precision/recall trade-offs. The project advanced to Round 2 of the NFPC/Razorpay Buildathon.'],
      ['What we learned', 'The README reports validation ROC-AUC of 0.9172 for a 5% GraphSAGE / 95% LightGBM blend, compared with 0.9113 for LightGBM alone. Tabular features provide most of the signal; graph structure adds a modest lift.'],
    ],
    caveat: 'These are reported research results on a random validation split, not deployment performance. The README also documents an unresolved node-alignment risk and graph/community features that are not yet merged into model inputs. A temporal evaluation is still needed. Scores support human review; they do not automatically block accounts.',
    repo: 'https://github.com/drain-is-she/mule_account_detection'
  },
  llm: {
    number: '02', title: 'LLM From Scratch', role: 'Team project · Co-development & pretraining experiments',
    summary: 'A decoder-only Transformer built to understand every component of a language model: tokenization, embeddings, causal attention, and the training loop. The complete model has 163,037,184 parameters.',
    flow: ['GPT-2 tokenization', 'Embeddings', '12 Transformer blocks', 'Next-token prediction'],
    sections: [
      ['The question', 'What does it take to build and train a language model when the internals stay explicit? The project connects the underlying math to readable PyTorch components and a reproducible training workflow.'],
      ['What I worked on', 'I co-developed and pretrained the model with teammates, implementing and evaluating model and training components. The work included checkpoint recovery, held-out validation, cross-entropy and perplexity tracking, and generation experiments.'],
      ['Under the hood', 'Twelve causal attention blocks, 12 attention heads, a hidden width of 768, and a 1,024-token context. Training uses AdamW, gradient accumulation, checkpoint recovery, and BF16 on supported CUDA hardware. Token embeddings and the output projection have separate weights.'],
    ],
    caveat: 'The parameter count describes model size, not capability. Validation uses a fixed sample of held-out batches, rather than the full held-out corpus. Evaluated training results and model capabilities are not yet published in the README.',
    repo: 'https://github.com/drain-is-she/LLM_from_scratch'
  },
  diffusion: {
    number: '03', title: 'Diffusion Models', role: 'Team project · Generative modeling & controlled experiments',
    summary: 'An exploration of how images emerge from noise. An unconditional U-Net/DDPM pipeline and a class-conditioned workflow generate 28 × 28 MNIST digits, with DDPM and DDIM sampling and classifier-free guidance.',
    flow: ['Gaussian noise', 'U-Net denoising', 'Digit conditioning', '28 × 28 image'],
    sections: [
      ['The question', 'How do sampling steps and guidance strength change the behavior of a diffusion model? The project separates unconditional generation from class conditioning and compares samplers under controlled settings.'],
      ['What I worked on', 'I worked on unconditional and class-conditioned diffusion workflows, and compared sampling steps and guidance strengths using fixed seeds, GPU runtime measurements, and requested-digit classifier agreement.'],
      ['What we learned', 'Published experiments cover 1,200 generated images across 12 configurations. In the 100-image, 50-step DDIM test with guidance scale 3, all generated digits matched their requested labels according to the classifier. DDIM was slightly slower than DDPM at equal step counts in this run.'],
    ],
    caveat: 'These are small, fixed-seed experiments. Classifier agreement is not a realism or diversity score, and does not establish generalization or rule out memorization. Conditioning uses digit labels, not text prompts. The unconditional U-Net is implemented in PyTorch; the conditional model uses Hugging Face Diffusers.',
    repo: 'https://github.com/drain-is-she/Diffusion'
  }
};

const coaches = [...document.querySelectorAll('[data-coach]')];
const selectButtons = [...document.querySelectorAll('[data-select]')];
const trainScroll = document.querySelector('.train-scroll');
const motionButton = document.querySelector('.motion-toggle');
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const names = Object.values(projects).map(project => project.title);
let activeProject = 0;
let userPaused = motionPreference.matches;
let trainVisible = true;
let scrollTimer;
let navigationTimer;
let navigating = false;

function updateAnimations() {
  coaches.forEach((coach, index) => {
    const image = coach.querySelector('img');
    const playing = index === activeProject && !userPaused && trainVisible && !document.hidden;
    const nextSource = playing ? image.dataset.animation : image.dataset.still;
    if (image.getAttribute('src') !== nextSource) image.setAttribute('src', nextSource);
    image.dataset.playing = String(playing);
  });
  motionButton.setAttribute('aria-pressed', String(userPaused));
  motionButton.setAttribute('aria-label', userPaused ? 'Play project animations' : 'Pause project animations');
  motionButton.innerHTML = userPaused ? '<span aria-hidden="true">▷</span> Play motion' : '<span aria-hidden="true">Ⅱ</span> Pause motion';
}

function selectProject(index, moveToCoach = false) {
  activeProject = (index + coaches.length) % coaches.length;
  coaches.forEach((coach, coachIndex) => {
    const selected = coachIndex === activeProject;
    coach.classList.toggle('is-active', selected);
    coach.querySelector('.coach-state').textContent = selected ? 'NOW EXPLORING' : 'NEXT STOP';
  });
  selectButtons.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.select) === activeProject)));
  document.getElementById('train-status').textContent = `At stop 0${activeProject + 1} — ${names[activeProject]}`;
  updateAnimations();
  if (moveToCoach && trainScroll.scrollWidth > trainScroll.clientWidth + 5) {
    navigating = true;
    clearTimeout(navigationTimer);
    const coachRect = coaches[activeProject].getBoundingClientRect();
    const containerRect = trainScroll.getBoundingClientRect();
    trainScroll.scrollTo({ left: trainScroll.scrollLeft + coachRect.left - containerRect.left - (trainScroll.clientWidth - coachRect.width) / 2, behavior: motionPreference.matches ? 'instant' : 'smooth' });
    navigationTimer = setTimeout(() => { navigating = false; }, 650);
  }
}

selectButtons.forEach(button => {
  button.addEventListener('click', () => selectProject(Number(button.dataset.select), true));
  button.addEventListener('focus', () => selectProject(Number(button.dataset.select)));
});
coaches.forEach((coach, index) => {
  coach.querySelector('.coach-window').addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') selectProject(index);
  });
});

document.getElementById('previous-project').addEventListener('click', () => selectProject(activeProject - 1, true));
document.getElementById('next-project').addEventListener('click', () => selectProject(activeProject + 1, true));
trainScroll.addEventListener('keydown', event => {
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
  event.preventDefault();
  selectProject(activeProject + (event.key === 'ArrowRight' ? 1 : -1), true);
});
trainScroll.addEventListener('scroll', () => {
  clearTimeout(scrollTimer);
  scrollTimer = setTimeout(() => {
    if (navigating || trainScroll.scrollWidth <= trainScroll.clientWidth + 5) return;
    const rect = trainScroll.getBoundingClientRect();
    const center = rect.left + rect.width / 2;
    const distances = coaches.map(coach => {
      const bounds = coach.getBoundingClientRect();
      return Math.abs(bounds.left + bounds.width / 2 - center);
    });
    selectProject(distances.indexOf(Math.min(...distances)));
  }, 110);
}, { passive: true });

motionButton.addEventListener('click', () => { userPaused = !userPaused; updateAnimations(); });
motionPreference.addEventListener('change', event => { userPaused = event.matches; updateAnimations(); });
document.addEventListener('visibilitychange', updateAnimations);
if ('IntersectionObserver' in window) {
  new IntersectionObserver(entries => {
    trainVisible = entries[0].isIntersecting;
    updateAnimations();
  }, { threshold: 0.05 }).observe(trainScroll);
}

const dialog = document.getElementById('project-dialog');
let dialogTrigger = null;
document.querySelectorAll('[data-project]').forEach(button => {
  button.addEventListener('click', () => {
    const project = projects[button.dataset.project];
    dialogTrigger = button;
    selectProject(Number(project.number) - 1);
    document.getElementById('dialog-number').textContent = `FIELD NOTES / STOP ${project.number}`;
    document.getElementById('dialog-content').innerHTML = `
      <h2 id="dialog-title">${project.title}</h2>
      <p class="dialog-role">${project.role}</p>
      <p class="dialog-summary">${project.summary}</p>
      <div class="dialog-flow" aria-label="Project workflow">${project.flow.map(step => `<span>${step}</span>`).join('<i aria-hidden="true">→</i>')}</div>
      <div class="dialog-body">${project.sections.map(([heading, content]) => `<h3>${heading}</h3><p>${content}</p>`).join('')}
        <h3>A note on the results</h3><p class="dialog-caveat">${project.caveat}</p>
        <a class="text-link" href="${project.repo}" target="_blank" rel="noopener noreferrer">Explore the code & full README <span aria-hidden="true">↗</span></a>
        <p class="dialog-footnote">Project details from the repository README; personal contributions from my CV. Window animations are illustrative sketches, not recorded model outputs.</p>
      </div>`;
    dialog.showModal();
    dialog.scrollTop = 0;
    document.body.classList.add('dialog-open');
    document.getElementById('close-dialog').focus();
  });
});
document.getElementById('close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const bounds = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('dialog-open');
  dialogTrigger?.focus({ preventScroll: true });
});
document.getElementById('year').textContent = new Date().getFullYear();
selectProject(0);
