/**
 * Falling Coins Animation with Mouse Interaction
 * Creates an animated background with coins falling from top to bottom
 * Coins react to mouse cursor proximity
 */

// Global variable to control falling speed (default: 1.0)
window.fallingCoinsSpeed = 0.5;

class FallingCoinsBackground {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.coins = [];
        this.mouseX = -1000;
        this.mouseY = -1000;
        this.mouseRadius = 100; // Radius of mouse influence

        // Reduce coins on non-login pages and mobile devices
        const isLoginPage = document.getElementById('loginForm');
        const isMobile = window.innerWidth < 768;

        if (isLoginPage) {
            this.coinCount = isMobile ? 10 : 30; // 10 for mobile login, 30 for desktop login
        } else {
            this.coinCount = 3; // 3 for other pages
        }
        this.animationId = null;

        this.init();
    }

    async startEnergyMonitoring() {
        // Initial Update
        await this.updateEnergyState();

        // Listen for Reduced Motion changes
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addEventListener('change', () => this.updateEnergyState());

        // Listen for Battery changes
        try {
            if (navigator.getBattery) {
                const battery = await navigator.getBattery();
                battery.addEventListener('chargingchange', () => this.updateEnergyState());
                battery.addEventListener('levelchange', () => this.updateEnergyState());
            }
        } catch (e) {
            // Ignore battery API errors
        }
    }

    async updateEnergyState() {
        // 1. Check Reduced Motion
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        // 2. Check Hardware (Static)
        const weakHardware = (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);

        // 3. Check Battery
        let lowBattery = false;
        try {
            if (navigator.getBattery) {
                const battery = await navigator.getBattery();
                // Using User's logic: Unplugged OR Low Battery triggers mode
                if (!battery.charging || (battery.level < 0.2)) lowBattery = true;
            }
        } catch (e) { }

        this.lowPowerMode = reducedMotion || weakHardware || lowBattery;

        // Determine Base Target Count
        const isLoginPage = document.getElementById('loginForm');
        const isMobile = window.innerWidth < 768;
        let targetCount = isLoginPage ? (isMobile ? 6 : 30) : 3;

        // Apply Energy Mode Constraints
        if (this.lowPowerMode)
            if (targetCount > 10) targetCount = 10;

        this.coinCount = targetCount;

        // Adjust Coin Array Live
        // Trim if too many
        if (this.coins.length > this.coinCount) {
            this.coins = this.coins.slice(0, this.coinCount);
        }
        // Add if too few
        while (this.coins.length < this.coinCount) {
            this.coins.push(this.createCoin());
        }
    }

    async init() {
        // Create canvas element
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'falling-coins-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '1';
        this.canvas.style.opacity = '0.6';

        document.body.insertBefore(this.canvas, document.body.firstChild);

        this.ctx = this.canvas.getContext('2d');
        this.resize();

        // Start real-time monitoring (this handles initial coin creation too)
        await this.startEnergyMonitoring();

        // Event listeners
        window.addEventListener('resize', () => {
            this.resize();
            this.updateEnergyState(); // Re-check mobile/desktop status on resize
        });
        document.addEventListener('mousemove', (e) => this.updateMousePosition(e));

        // Start animation
        this.lastFrameTime = 0;
        this.animate(0);
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    updateMousePosition(e) {
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
    }

    createCoins() {
        for (let i = 0; i < this.coinCount; i++) {
            this.coins.push(this.createCoin());
        }
    }

    createCoin() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * -this.canvas.height, // Start above screen
            vx: (Math.random() - 0.5) * 1, // Horizontal velocity
            vy: (Math.random() * 2 + 1) * window.fallingCoinsSpeed, // Vertical velocity (falling speed)
            size: Math.random() * 20 + 15, // Coin size
            rotation: Math.random() * Math.PI * 2,
            rotationSpeed: (Math.random() - 0.5) * 0.1,
            type: Math.random() > 0.5 ? 'gold' : 'silver', // Coin color
            wobble: Math.random() * Math.PI * 2, // For wobble effect
            wobbleSpeed: Math.random() * 0.05 + 0.02
        };
    }

    drawCoin(coin) {
        this.ctx.save();
        this.ctx.translate(coin.x, coin.y);
        this.ctx.rotate(coin.rotation);

        // Draw coin circle
        this.ctx.beginPath();
        this.ctx.arc(0, 0, coin.size, 0, Math.PI * 2);

        const gradient = this.ctx.createRadialGradient(0, 0, 0, 0, 0, coin.size);
        if (coin.type === 'gold') {
            gradient.addColorStop(0, '#FFD700');
            gradient.addColorStop(0.5, '#FFA500');
            gradient.addColorStop(1, '#FF8C00');
        } else {
            gradient.addColorStop(0, '#E8E8E8');
            gradient.addColorStop(0.5, '#C0C0C0');
            gradient.addColorStop(1, '#A8A8A8');
        }
        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // 3D edge effect
        this.ctx.strokeStyle = coin.type === 'gold' ? '#B8860B' : '#808080';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();

        // Draw dollar sign
        this.ctx.fillStyle = coin.type === 'gold' ? '#8B6914' : '#505050';
        this.ctx.font = `bold ${coin.size * 0.8}px Arial`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('$', 0, 0);

        this.ctx.restore();
    }

    updateCoin(coin, timeScale = 1) {
        // Calculate distance from mouse
        const dx = this.mouseX - coin.x;
        const dy = this.mouseY - coin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Mouse interaction - repel coins
        if (distance < this.mouseRadius) {
            const force = (this.mouseRadius - distance) / this.mouseRadius;
            const angle = Math.atan2(dy, dx);
            // Apply force scaled by time
            const forceX = Math.cos(angle) * force * 0.5 * timeScale;
            const forceY = Math.sin(angle) * force * 0.5 * timeScale;
            coin.vx -= forceX;
            coin.vy -= forceY;
        }

        // Apply velocity with scaling
        coin.x += coin.vx * timeScale;
        coin.y += coin.vy * timeScale;


        // Add wobble effect
        coin.wobble += coin.wobbleSpeed * timeScale;
        coin.x += Math.sin(coin.wobble) * 0.5 * timeScale;

        // Damping - frame-rate independent friction
        // Logic: newV = oldV * friction^timeScale
        coin.vx *= Math.pow(0.98, timeScale);

        // Vertical terminal velocity lerp
        // Lerp towards target speed: target = ((Math.random() * 2 + 1) * window.fallingCoinsSpeed)
        // Rate of 0.02 per frame at 60fps
        const targetVy = (Math.random() * 2 + 1) * window.fallingCoinsSpeed;
        const lerpFactor = 1 - Math.pow(1 - 0.02, timeScale);
        coin.vy = coin.vy * (1 - lerpFactor) + targetVy * lerpFactor;
        coin.rotation += coin.rotationSpeed * timeScale;

        // Reset coin if it goes off screen
        if (coin.y > this.canvas.height + coin.size) {
            coin.y = -coin.size;
            coin.x = Math.random() * this.canvas.width;
            coin.vx = (Math.random() - 0.5) * 1;
            coin.vy = (Math.random() * 2 + 1) * window.fallingCoinsSpeed;
        }

        // Keep coins within horizontal bounds
        if (coin.x < -coin.size) {
            coin.x = this.canvas.width + coin.size;
        } else if (coin.x > this.canvas.width + coin.size) {
            coin.x = -coin.size;
        }
    }

    animate(timestamp) {
        if (!this.lastFrameTime) this.lastFrameTime = timestamp;

        // Calculate delta time
        const deltaTime = timestamp - this.lastFrameTime;
        this.lastFrameTime = timestamp;

        // Cap delta time to match physics if tab was inactive (prevent huge jumps)
        // 100ms max = min 10fps simulation
        const safeDeltaTime = Math.min(deltaTime, 100);

        // Calculate factor relative to 60fps (16.67ms)
        // If running at 60fps, timeScale = 1.0
        // If running at 120fps, timeScale = 0.5
        const timeScale = safeDeltaTime / (1000 / 60);

        // Clear canvas logic
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw coins
        this.coins.forEach(coin => {
            this.updateCoin(coin, timeScale);
            this.drawCoin(coin);
        });

        // Continue animation
        this.animationId = requestAnimationFrame((t) => this.animate(t));
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new FallingCoinsBackground();
    });
} else {
    new FallingCoinsBackground();
}
