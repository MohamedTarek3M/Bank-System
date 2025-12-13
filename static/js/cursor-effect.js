/**
 * Interactive Animated Gradient Background
 * Controls gradient animation speed based on cursor movement
 */

// Track mouse position and movement
let mouseX = 0;
let mouseY = 0;
let lastMouseX = 0;
let lastMouseY = 0;
let mouseSpeed = 0;

// Update mouse position and calculate speed
document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth) * 100;
    mouseY = (e.clientY / window.innerHeight) * 100;

    // Calculate mouse movement speed
    const deltaX = mouseX - lastMouseX;
    const deltaY = mouseY - lastMouseY;
    mouseSpeed = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

    // Update last position
    lastMouseX = mouseX;
    lastMouseY = mouseY;

    // Map speed to animation duration (faster mouse = faster animation)
    // Speed range: 0-10 (typical), Duration range: 5s (fast) to 20s (slow)
    const minDuration = 5;  // Fastest animation
    const maxDuration = 20; // Slowest animation
    const speedFactor = Math.min(mouseSpeed / 5, 1); // Normalize speed
    const duration = maxDuration - (speedFactor * (maxDuration - minDuration));

    // Update CSS custom property for animation duration
    document.documentElement.style.setProperty('--gradient-speed', duration + 's');
});

// Reset speed when mouse stops
let resetTimer;
document.addEventListener('mousemove', () => {
    clearTimeout(resetTimer);
    resetTimer = setTimeout(() => {
        // Gradually return to normal speed when mouse stops
        document.documentElement.style.setProperty('--gradient-speed', '20s');
    }, 500);
});

// Initialize gradient speed
document.documentElement.style.setProperty('--gradient-speed', '20s');
