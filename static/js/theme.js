// Theme Toggle Functionality

(function () {
    // Get theme from localStorage or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;

    // Apply theme on page load
    if (currentTheme === 'dark') {
        html.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    } else {
        html.removeAttribute('data-theme');
        updateThemeIcon('light');
    }

    // Theme toggle button (handle multiple instances - login page and navbar)
    const themeToggles = document.querySelectorAll('.theme-toggle');
    themeToggles.forEach(function (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const currentTheme = html.getAttribute('data-theme');

            if (currentTheme === 'dark') {
                // Switch to light mode
                html.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                updateThemeIcon('light');
            } else {
                // Switch to dark mode
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateThemeIcon('dark');
            }
        });
    });

    // Update theme icon (update all instances)
    function updateThemeIcon(theme) {
        const themeIcons = document.querySelectorAll('.theme-icon');
        themeIcons.forEach(function (themeIcon) {
            const lightDest = themeIcon.getAttribute('data-light-dest');
            const darkDest = themeIcon.getAttribute('data-dark-dest');

            if (theme === 'dark') {
                themeIcon.src = lightDest;
                themeIcon.parentElement.title = 'Switch to Light Mode';
            } else {
                themeIcon.src = darkDest;
                themeIcon.parentElement.title = 'Switch to Dark Mode';
            }
        });
    }

    // Update icon on page load
    updateThemeIcon(currentTheme);
})();

