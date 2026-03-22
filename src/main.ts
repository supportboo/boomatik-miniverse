import { createMiniverse } from '@miniverse/core';

// Initialize the Boomatik Miniverse
const miniverse = createMiniverse({
  container: document.getElementById('app')!,
  width: window.innerWidth,
  height: window.innerHeight,
  pixelScale: 3,
});

// Update clock
function updateClock() {
  const el = document.getElementById('clock');
  if (el) {
    el.textContent = new Date().toLocaleTimeString('es-ES');
  }
  requestAnimationFrame(updateClock);
}
updateClock();

// Handle resize
window.addEventListener('resize', () => {
  miniverse.resize(window.innerWidth, window.innerHeight);
});

console.log('🤖 Boomatik Miniverse initialized');
console.log('📡 Server API: http://localhost:4321');
console.log('🌐 Frontend: http://localhost:5173');
