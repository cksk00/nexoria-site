(function () {
  const PX = 5;

  const FRAMES = [
    [
      [0,0,1,1,1,0,0],
      [0,1,1,1,1,1,0],
      [1,1,2,1,2,1,1],
      [1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1],
      [1,0,1,0,1,0,1],
      [0,0,0,0,0,0,0],
    ],
    [
      [0,0,1,1,1,0,0],
      [0,1,1,1,1,1,0],
      [1,1,2,1,2,1,1],
      [1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1],
      [0,1,0,1,0,1,0],
      [0,0,0,0,0,0,0],
    ],
    [
      [0,0,1,1,1,0,0],
      [0,1,1,1,1,1,0],
      [1,1,1,2,1,2,1],
      [1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1],
      [1,0,1,0,1,0,1],
      [0,0,0,0,0,0,0],
    ],
    [
      [0,0,1,1,1,0,0],
      [0,1,1,1,1,1,0],
      [1,1,1,2,1,2,1],
      [1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1],
      [0,1,0,1,0,1,0],
      [0,0,0,0,0,0,0],
    ],
  ];

  const COLS    = FRAMES[0][0].length;
  const ROWS    = FRAMES[0].length;
  const GHOST_W = COLS * PX;
  const GHOST_H = ROWS * PX;

  const canvas = document.getElementById('cat-canvas');
  const ctx    = canvas.getContext('2d');
  canvas.width  = 220;
  canvas.height = GHOST_H;

  let ghostX        = -GHOST_W;
  let frameIdx      = 0;
  let lastFrameTime = 0;
  let lastTime      = null;
  let startTime     = null;

  const BOOT_MS  = 5000;
  const FRAME_MS = 180;
  const SPEED    = 45;

  // ── Sequential boot text ──────────────────────
  const STAGES = [
    'Boot sequence started...',
    'Verifying integrity...',
    'Access granted.',
    'Execute.',
  ];
  const DELAYS = [0, 1300, 2600, 3700]; // ms from boot start

  const textEl = document.getElementById('boot-text');

  STAGES.forEach((msg, i) => {
    setTimeout(() => {
      textEl.style.opacity = '0';
      setTimeout(() => {
        textEl.textContent = msg;
        textEl.style.opacity = '1';
      }, 150);
    }, DELAYS[i]);
  });

  // ── Ghost animation ───────────────────────────
  function drawGhost(ts) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const bobY = Math.sin(ts * 0.004) * 3;
    const grid = FRAMES[frameIdx];
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const v = grid[r][c];
        if (!v) continue;
        ctx.fillStyle = v === 2 ? '#222' : '#d8d8d8';
        ctx.fillRect(Math.round(ghostX) + c * PX, Math.round(bobY) + r * PX, PX, PX);
      }
    }
  }

  function animate(ts) {
    if (!startTime) startTime = ts;
    if (!lastTime)  lastTime  = ts;

    const elapsed = ts - startTime;
    const delta   = ts - lastTime;
    lastTime = ts;

    if (ts - lastFrameTime > FRAME_MS) {
      frameIdx = (frameIdx + 1) % FRAMES.length;
      lastFrameTime = ts;
    }

    ghostX += SPEED * (delta / 1000);
    if (ghostX > canvas.width) ghostX = -GHOST_W;

    drawGhost(ts);

    if (elapsed < BOOT_MS) {
      requestAnimationFrame(animate);
    } else {
      const screen = document.getElementById('boot-screen');
      screen.classList.add('boot-out');
      setTimeout(() => screen.remove(), 900);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    requestAnimationFrame(animate);
  });
})();
