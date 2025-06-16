#!/usr/bin/env python3
"""
MAO UI Design Playground
Interactive terminal design experimentation tool

Inspired by Claude Code's visual design:
- 4-color palette (Yellow, Light Blue, White, Pink)
- Character-based visual elements (no emojis)
- Typography-focused with careful spacing
- Left-anchored icons with intentional gaps
"""

import json
import os
from typing import Dict, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt, Confirm
from rich import box
import time

class MAOUIPlayground:
    """Interactive UI design playground for MAO terminal interface"""
    
    def __init__(self):
        self.console = Console()
        
        # Claude Code inspired 4-color palette
        self.colors = {
            "focus": "#FFD93D",      # Yellow - main focus
            "accent": "#74B9FF",     # Light blue - accents/secondary  
            "normal": "#F0F6FC",     # White - normal text
            "emphasis": "#FF6B9D",   # Pink - paths/names/bold
            "icon": "#0088CC",       # Darker blue - icons
            "subtle": "#8B949E"      # Faded tan - numbers/subtle
        }
        
        # Character library (no emojis - character-based visuals)
        self.visual_chars = {
            "bullets": ["※", "⏺", "▶", "◆", "⬥", "●", "○", "▪", "▫", "◦"],
            "icons": ["!", "✓", "✗", "?", ">", "<", "^", "⎿", "┌", "└", "├", "│"],
            "separators": ["─", "═", "┄", "┅", "╌", "╍", "·", "‧", "•"],
            "frames": ["┌", "┐", "└", "┘", "│", "─", "├", "┤", "┬", "┴", "┼"]
        }
        
        # Current design state
        self.current_design = {
            "bullet_char": "※",
            "icon_char": "⏺", 
            "anchor_gap": 6,
            "text_indent": 2,
            "color_scheme": "default"
        }
        
        # Saved designs
        self.saved_designs = self.load_saved_designs()
    
    def load_saved_designs(self) -> Dict:
        """Load saved design configurations"""
        config_file = "mao_ui_designs.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_design(self, name: str) -> None:
        """Save current design configuration"""
        self.saved_designs[name] = self.current_design.copy()
        with open("mao_ui_designs.json", 'w') as f:
            json.dump(self.saved_designs, f, indent=2)
        self.console.print(f"Design '{name}' saved!", style="bold green")
    
    def load_design(self, name: str) -> None:
        """Load a saved design configuration"""
        if name in self.saved_designs:
            self.current_design = self.saved_designs[name].copy()
            self.console.print(f"Design '{name}' loaded!", style="bold green")
        else:
            self.console.print(f"Design '{name}' not found", style="bold red")
    
    def create_sample_interface(self) -> Panel:
        """Create sample MAO interface with current design settings"""
        
        # Get current settings
        bullet = self.current_design["bullet_char"]
        icon = self.current_design["icon_char"] 
        gap = " " * self.current_design["anchor_gap"]
        indent = " " * self.current_design["text_indent"]
        
        # Create sample content with various UI patterns
        content = Text()
        
        # Header section
        content.append("^.^", style=f"bold {self.colors['emphasis']}")
        content.append("   Hello! I'm Mao. What do you want to build today?\n", style=self.colors['normal'])
        content.append(gap + "Let me know if you need any ideas, want to explore the tools,\n", style=self.colors['normal'])
        content.append(gap + "or if you want I can build the workflow for you with nothing\n", style=self.colors['normal'])  
        content.append(gap + "more than a goal.\n\n", style=self.colors['normal'])
        
        # Command execution example
        content.append("!", style=f"bold {self.colors['icon']}")
        content.append(" mao --goal create marketing plan\n", style=self.colors['emphasis'])
        content.append("⎿", style=self.colors['icon']) 
        content.append(f"{gap[1:]}Starting workflow creation...\n\n", style=self.colors['accent'])
        
        # Workflow phases with bullets
        content.append("🎭 WORKFLOW PHASES:\n", style=f"bold {self.colors['focus']}")
        
        phases = [
            ("Research Phase", "Analyzing market trends and competitors"),
            ("Strategy Phase", "Developing comprehensive marketing approach"),
            ("Content Phase", "Creating compelling marketing materials"),
            ("Launch Phase", "Coordinating campaign execution")
        ]
        
        for i, (phase, desc) in enumerate(phases, 1):
            content.append(f"{indent}{i}. ", style=self.colors['subtle'])
            content.append(f"{phase}\n", style=f"bold {self.colors['normal']}")
            content.append(f"{indent}{gap}{desc}\n", style=self.colors['accent'])
        
        content.append("\n")
        
        # Status indicators
        content.append(bullet, style=f"bold {self.colors['focus']}")
        content.append(f"{gap}Estimated cost: $0.23 | Duration: ~8 minutes\n", style=self.colors['normal'])
        
        content.append(icon, style=f"bold {self.colors['icon']}")
        content.append(f"{gap}Ready to execute? [Y/n]: ", style=self.colors['accent'])
        
        return Panel(
            content,
            title="[bold]MAO Terminal Interface Preview[/bold]",
            border_style=self.colors['accent'],
            box=box.ROUNDED
        )
    
    def create_color_picker(self) -> Table:
        """Create interactive color picker interface"""
        table = Table(title="Color Palette", box=box.SIMPLE)
        table.add_column("Role", style="bold")
        table.add_column("Current", justify="center")
        table.add_column("Color", justify="center")
        table.add_column("Usage")
        
        color_roles = {
            "focus": "Main highlights, important elements",
            "accent": "Secondary info, descriptions", 
            "normal": "Regular text content",
            "emphasis": "Paths, names, commands",
            "icon": "Visual indicators, symbols",
            "subtle": "Numbers, less important text"
        }
        
        for role, usage in color_roles.items():
            color = self.colors[role]
            sample = Text("██", style=color)
            table.add_row(role.title(), sample, color, usage)
        
        return table
    
    def create_character_picker(self) -> Table:
        """Create character selection interface"""
        table = Table(title="Visual Characters", box=box.SIMPLE)
        table.add_column("Category", style="bold")
        table.add_column("Options", justify="left")
        table.add_column("Current", justify="center")
        
        for category, chars in self.visual_chars.items():
            char_display = " ".join(chars[:10])  # Show first 10
            if category == "bullets":
                current = self.current_design["bullet_char"]
            elif category == "icons":
                current = self.current_design["icon_char"]
            else:
                current = "─"
            
            current_display = Text(current, style=f"bold {self.colors['focus']}")
            table.add_row(category.title(), char_display, current_display)
        
        return table
    
    def create_spacing_controls(self) -> Table:
        """Create spacing and layout controls"""
        table = Table(title="Layout Controls", box=box.SIMPLE)
        table.add_column("Setting", style="bold") 
        table.add_column("Current", justify="center")
        table.add_column("Description")
        
        settings = [
            ("anchor_gap", self.current_design["anchor_gap"], "Gap between icon anchor and text"),
            ("text_indent", self.current_design["text_indent"], "Base text indentation"),
        ]
        
        for setting, value, desc in settings:
            value_display = Text(str(value), style=f"bold {self.colors['accent']}")
            table.add_row(setting.replace("_", " ").title(), value_display, desc)
        
        return table
    
    def show_design_menu(self) -> None:
        """Show main design experimentation menu"""
        while True:
            self.console.clear()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(self.create_sample_interface(), name="preview", ratio=2),
                Layout(name="controls", ratio=1)
            )
            
            # Split controls into columns
            layout["controls"].split_row(
                Layout(self.create_color_picker(), name="colors"),
                Layout(self.create_character_picker(), name="chars"),
                Layout(self.create_spacing_controls(), name="spacing")
            )
            
            self.console.print(layout)
            
            # Menu options
            self.console.print("\n" + "─" * 60, style=self.colors['subtle'])
            self.console.print("MAO UI Design Playground", style=f"bold {self.colors['focus']}")
            self.console.print("─" * 60, style=self.colors['subtle'])
            
            options = [
                "[c] Change colors",
                "[h] Change characters", 
                "[s] Adjust spacing",
                "[save] Save design",
                "[load] Load design",
                "[list] List saved designs",
                "[reset] Reset to defaults",
                "[q] Quit"
            ]
            
            for option in options:
                self.console.print(f"  {option}", style=self.colors['accent'])
            
            choice = Prompt.ask("\nWhat would you like to adjust?", 
                              choices=["c", "h", "s", "save", "load", "list", "reset", "q"],
                              default="c").lower()
            
            if choice == "q":
                break
            elif choice == "c":
                self.adjust_colors()
            elif choice == "h":
                self.adjust_characters()
            elif choice == "s":
                self.adjust_spacing()
            elif choice == "save":
                name = Prompt.ask("Enter design name")
                if name:
                    self.save_design(name)
                    time.sleep(1)
            elif choice == "load":
                self.show_saved_designs()
                name = Prompt.ask("Enter design name to load")
                if name:
                    self.load_design(name)
                    time.sleep(1)
            elif choice == "list":
                self.show_saved_designs()
                input("Press Enter to continue...")
            elif choice == "reset":
                if Confirm.ask("Reset to default design?"):
                    self.reset_to_defaults()
    
    def adjust_colors(self) -> None:
        """Interactive color adjustment"""
        self.console.print("\n🎨 Color Adjustment", style=f"bold {self.colors['focus']}")
        
        role = Prompt.ask(
            "Which color role to adjust?",
            choices=list(self.colors.keys()),
            default="focus"
        )
        
        self.console.print(f"\nCurrent {role} color: {self.colors[role]}")
        new_color = Prompt.ask("Enter new hex color (e.g., #FFD93D)")
        
        if new_color.startswith("#") and len(new_color) == 7:
            self.colors[role] = new_color
            self.console.print(f"Updated {role} to {new_color}!", style="bold green")
        else:
            self.console.print("Invalid color format", style="bold red")
        
        time.sleep(1)
    
    def adjust_characters(self) -> None:
        """Interactive character adjustment"""
        self.console.print("\n📝 Character Adjustment", style=f"bold {self.colors['focus']}")
        
        category = Prompt.ask(
            "Which character category?",
            choices=list(self.visual_chars.keys()),
            default="bullets"
        )
        
        chars = self.visual_chars[category]
        self.console.print(f"\nAvailable {category}: {' '.join(chars)}")
        
        new_char = Prompt.ask("Enter character to use")
        
        if category == "bullets":
            self.current_design["bullet_char"] = new_char
        elif category == "icons":
            self.current_design["icon_char"] = new_char
        
        self.console.print(f"Updated {category} character!", style="bold green")
        time.sleep(1)
    
    def adjust_spacing(self) -> None:
        """Interactive spacing adjustment"""
        self.console.print("\n📏 Spacing Adjustment", style=f"bold {self.colors['focus']}")
        
        setting = Prompt.ask(
            "Which spacing to adjust?",
            choices=["anchor_gap", "text_indent"],
            default="anchor_gap"
        )
        
        current = self.current_design[setting]
        self.console.print(f"\nCurrent {setting}: {current}")
        
        try:
            new_value = int(Prompt.ask("Enter new value (0-20)", default=str(current)))
            if 0 <= new_value <= 20:
                self.current_design[setting] = new_value
                self.console.print(f"Updated {setting} to {new_value}!", style="bold green")
            else:
                self.console.print("Value must be between 0-20", style="bold red")
        except ValueError:
            self.console.print("Invalid number", style="bold red")
        
        time.sleep(1)
    
    def show_saved_designs(self) -> None:
        """Show list of saved designs"""
        if not self.saved_designs:
            self.console.print("No saved designs", style=self.colors['subtle'])
            return
        
        table = Table(title="Saved Designs", box=box.SIMPLE)
        table.add_column("Name", style="bold")
        table.add_column("Bullet", justify="center")
        table.add_column("Icon", justify="center") 
        table.add_column("Gap", justify="center")
        
        for name, design in self.saved_designs.items():
            table.add_row(
                name,
                design.get("bullet_char", "※"),
                design.get("icon_char", "⏺"),
                str(design.get("anchor_gap", 6))
            )
        
        self.console.print(table)
    
    def reset_to_defaults(self) -> None:
        """Reset to default design settings"""
        self.current_design = {
            "bullet_char": "※",
            "icon_char": "⏺",
            "anchor_gap": 6,
            "text_indent": 2,
            "color_scheme": "default"
        }
        self.console.print("Reset to defaults!", style="bold green")
        time.sleep(1)
    
    def run(self) -> None:
        """Run the UI playground"""
        self.console.print(Panel(
            Text.assemble(
                ("MAO UI Design Playground\n", f"bold {self.colors['focus']}"),
                ("Interactive terminal design experimentation\n\n", self.colors['accent']),
                ("Experiment with:\n", f"bold {self.colors['normal']}"),
                ("• Typography and character selection\n", self.colors['normal']),
                ("• Color palette and assignments\n", self.colors['normal']),
                ("• Spacing and text alignment\n", self.colors['normal']),
                ("• Visual hierarchy and grouping\n", self.colors['normal'])
            ),
            title="Welcome",
            border_style=self.colors['accent']
        ))
        
        input("\nPress Enter to start experimenting...")
        self.show_design_menu()
        
        self.console.print("\nThanks for experimenting with MAO UI design! 🎨", 
                          style=f"bold {self.colors['focus']}")

def main():
    """Run the MAO UI Design Playground"""
    try:
        playground = MAOUIPlayground()
        playground.run()
    except KeyboardInterrupt:
        print("\n\nExiting playground...")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()