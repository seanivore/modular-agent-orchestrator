# Enabling Zoom/Pan for Mermaid Diagrams on Jekyll Sites

## Automatic Mermaid.js Zoom/Pan Features

When you publish to Jekyll/GitHub Pages, Mermaid.js automatically provides:

- **Mouse wheel zoom** in/out
- **Click and drag panning** 
- **Touch zoom/pan** on mobile devices
- **Double-click to reset** view
- **Automatic zoom controls** for large diagrams

## Jekyll Configuration (Add to _config.yml)

```yaml
# Enable Mermaid.js with zoom capabilities
plugins:
  - jekyll-mermaid

mermaid:
  version: "10.6.1"  # Latest stable version
  theme: default
  zoom: true         # Enable zoom/pan controls
  pan: true          # Enable panning
  securityLevel: 'loose'  # For better functionality
```

## Manual Setup (If needed)

Add to your Jekyll layout head section:

```html
<!-- Mermaid.js with zoom capabilities -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    flowchart: {
      useMaxWidth: false,  // Important for zoom
      htmlLabels: true
    }
  });
</script>

<!-- Optional: Add custom zoom controls CSS -->
<style>
.mermaid svg {
  max-width: none !important;  /* Allow zooming beyond container */
  cursor: grab;
}
.mermaid svg:active {
  cursor: grabbing;
}
</style>
```

## Enhanced Zoom Controls (Optional)

For even better zoom experience, add this JavaScript:

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
  // Add zoom controls to all Mermaid diagrams
  const mermaidDivs = document.querySelectorAll('.mermaid');
  
  mermaidDivs.forEach(div => {
    const svg = div.querySelector('svg');
    if (svg) {
      // Enable wheel zoom
      div.addEventListener('wheel', function(e) {
        e.preventDefault();
        const rect = svg.getBoundingClientRect();
        const scale = e.deltaY > 0 ? 0.9 : 1.1;
        
        // Apply zoom transform
        const currentTransform = svg.style.transform || 'scale(1)';
        const currentScale = parseFloat(currentTransform.match(/scale\(([^)]*)\)/)?.[1] || 1);
        const newScale = Math.max(0.1, Math.min(10, currentScale * scale));
        
        svg.style.transform = `scale(${newScale})`;
        svg.style.transformOrigin = 'center';
      });
      
      // Add reset button
      const resetBtn = document.createElement('button');
      resetBtn.innerHTML = '🔍 Reset Zoom';
      resetBtn.style.cssText = 'position: absolute; top: 10px; right: 10px; z-index: 1000;';
      resetBtn.onclick = () => svg.style.transform = 'scale(1)';
      
      div.style.position = 'relative';
      div.appendChild(resetBtn);
    }
  });
});
</script>
```

## Testing Your Setup

1. **Local testing:** Use the VS Code extensions mentioned above
2. **Jekyll serve:** Run `bundle exec jekyll serve` locally to test
3. **GitHub Pages:** Your zoom/pan will work automatically when deployed

## Responsive Design Considerations

```css
/* Make diagrams responsive with zoom */
.mermaid {
  overflow: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  max-height: 80vh;  /* Prevent diagrams from being too tall */
}

@media (max-width: 768px) {
  .mermaid svg {
    max-width: 100% !important;
    height: auto;
  }
}
```