// src/reportWebVitals.js

const reportWebVitals = async (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    try {
      const { getCLS, getFID, getFCP, getLCP, getTTFB } = await import('web-vitals');
      
      // Core Web Vitals
      getCLS(onPerfEntry); // Cumulative Layout Shift
      getFID(onPerfEntry); // First Input Delay
      getFCP(onPerfEntry); // First Contentful Paint
      getLCP(onPerfEntry); // Largest Contentful Paint
      getTTFB(onPerfEntry); // Time to First Byte

      // Additional Performance Metrics
      if (window.performance) {
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        
        // Report Navigation Timing metrics
        if (navigation) {
          onPerfEntry({
            name: 'DOM Complete',
            value: navigation.domComplete,
            delta: navigation.domComplete,
          });
        }

        // Report Paint Timing metrics
        paint.forEach(entry => {
          onPerfEntry({
            name: entry.name,
            value: entry.startTime,
            delta: entry.startTime,
          });
        });
      }
    } catch (error) {
      console.error('Error loading web-vitals:', error);
    }
  }
};

export default reportWebVitals;