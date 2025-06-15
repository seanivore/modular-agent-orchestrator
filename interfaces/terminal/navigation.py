# interfaces/terminal/navigation.py - Navigation State Manager

from typing import List, Optional


class NavigationManager:
    """Manages navigation state and history."""
    
    def __init__(self):
        self.history: List[str] = []
        self.current_index = -1
        self.max_history = 50
    
    def push(self, screen_name: str) -> None:
        """Push a new screen to navigation history."""
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        self.history.append(screen_name)
        self.current_index = len(self.history) - 1
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.current_index = len(self.history) - 1
    
    def pop(self) -> Optional[str]:
        """Go back to previous screen."""
        if self.can_go_back():
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def can_go_back(self) -> bool:
        """Check if we can go back."""
        return self.current_index > 0
    
    def current_screen(self) -> Optional[str]:
        """Get the current screen name."""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None
