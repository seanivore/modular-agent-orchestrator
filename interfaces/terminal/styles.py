# interfaces/terminal/styles.py - Color Schemes and Styling

from rich.theme import Theme
from rich.style import Style
from typing import Dict, Any

# Professional color palette - Anthropic inspired, no emojis
MAO_COLORS = {
    # Primary brand colors
    "primary": "#00D4FF",        # Bright cyan - main accent
    "primary_dark": "#0088CC",   # Darker cyan for contrast
    "secondary": "#FF6B9D",      # Soft pink - secondary accent
    "accent": "#FFD93D",         # Warm yellow - highlights
    
    # Semantic colors
    "success": "#00FF88",        # Bright green
    "warning": "#FFB347",        # Orange
    "error": "#FF4757",          # Red
    "info": "#74B9FF",           # Light blue
    
    # Interface colors
    "background": "#0D1117",     # Deep dark blue
    "surface": "#161B22",        # Slightly lighter dark
    "surface_hover": "#21262D",  # Hover state
    "border": "#30363D",         # Subtle borders
    "text_primary": "#F0F6FC",   # High contrast white
    "text_secondary": "#8B949E", # Muted text
    "text_dim": "#6E7681",       # Very subtle text
    
    # Workflow status colors  
    "active": "#00FF88",         # Currently running
    "pending": "#FFD93D",        # Waiting to run
    "completed": "#00D4FF",      # Successfully finished
    "failed": "#FF4757",         # Error state
    "draft": "#8B949E",          # Not yet configured
}

# Rich theme configuration
MAO_THEME = Theme({
    "primary": MAO_COLORS["primary"],
    "secondary": MAO_COLORS["secondary"], 
    "accent": MAO_COLORS["accent"],
    "success": MAO_COLORS["success"],
    "warning": MAO_COLORS["warning"],
    "error": MAO_COLORS["error"],
    "info": MAO_COLORS["info"],
    "text.primary": MAO_COLORS["text_primary"],
    "text.secondary": MAO_COLORS["text_secondary"],
    "text.dim": MAO_COLORS["text_dim"],
})

# Component styling helpers
def get_panel_style(variant: str = "default") -> Dict[str, Any]:
    """Get consistent panel styling."""
    base_style = {
        "border_style": "rounded",
        "padding": (1, 2),
    }
    
    variants = {
        "default": {"border_style": MAO_COLORS["border"]},
        "primary": {"border_style": MAO_COLORS["primary"]},
        "success": {"border_style": MAO_COLORS["success"]},
        "warning": {"border_style": MAO_COLORS["warning"]},
        "error": {"border_style": MAO_COLORS["error"]},
    }
    
    return {**base_style, **variants.get(variant, variants["default"])}
