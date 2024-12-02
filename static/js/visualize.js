document.addEventListener('DOMContentLoaded', () => {
    // Update metrics counters with animation
    const metrics = [
        { id: 'accuracy', value: 96, suffix: '' },
        { id: 'species', value: 4, suffix: '' },
        { id: 'predictions', value: 15234, suffix: '' }
    ];

    metrics.forEach(metric => {
        const element = document.getElementById(metric.id);
        if (!element) return;

        let current = 0;
        const target = metric.value;
        const duration = 2000; // 2 seconds
        const steps = 60;
        const increment = target / steps;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format the number based on the metric type
            let displayValue = current;
            if (metric.id === 'predictions') {
                displayValue = Math.round(current).toLocaleString();
            } else if (metric.id === 'species') {
                displayValue = Math.round(current);
            } else {
                displayValue = current.toFixed(1);
            }
            
            element.textContent = displayValue + metric.suffix;
        }, duration / steps);
    });
});