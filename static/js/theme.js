// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved user preference and set it
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    }
    
    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            
            // Change chart colors if they exist
            updateChartColors('dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            
            // Change chart colors if they exist
            updateChartColors('light');
        }
    }
    
    // Listen for toggle
    toggleSwitch.addEventListener('change', switchTheme, false);
    
    // Function to update chart colors when theme changes
    function updateChartColors(theme) {
        // If Charts exist, update them
        if (typeof Chart !== 'undefined') {
            Chart.helpers.each(Chart.instances, function(instance) {
                let config = instance.config;
                
                if (theme === 'dark') {
                    // Update grid lines
                    if (config.options.scales && config.options.scales.x) {
                        config.options.scales.x.grid.color = 'rgba(255, 255, 255, 0.1)';
                        config.options.scales.x.ticks.color = '#e0e0e0';
                    }
                    
                    if (config.options.scales && config.options.scales.y) {
                        config.options.scales.y.grid.color = 'rgba(255, 255, 255, 0.1)';
                        config.options.scales.y.ticks.color = '#e0e0e0';
                    }
                    
                    // Update title and legend
                    if (config.options.plugins && config.options.plugins.title) {
                        config.options.plugins.title.color = '#e0e0e0';
                    }
                    
                    if (config.options.plugins && config.options.plugins.legend) {
                        config.options.plugins.legend.labels.color = '#e0e0e0';
                    }
                    
                } else {
                    // Update grid lines
                    if (config.options.scales && config.options.scales.x) {
                        config.options.scales.x.grid.color = 'rgba(0, 0, 0, 0.1)';
                        config.options.scales.x.ticks.color = '#666';
                    }
                    
                    if (config.options.scales && config.options.scales.y) {
                        config.options.scales.y.grid.color = 'rgba(0, 0, 0, 0.1)';
                        config.options.scales.y.ticks.color = '#666';
                    }
                    
                    // Update title and legend
                    if (config.options.plugins && config.options.plugins.title) {
                        config.options.plugins.title.color = '#666';
                    }
                    
                    if (config.options.plugins && config.options.plugins.legend) {
                        config.options.plugins.legend.labels.color = '#666';
                    }
                }
                
                instance.update();
            });
        }
    }
    
    // Initialize charts with current theme
    const theme = localStorage.getItem('theme') || 'light';
    updateChartColors(theme);
});