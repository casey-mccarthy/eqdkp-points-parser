"""
Progress display management for user feedback.
"""
from rich.console import Console

class ProgressManager:
    """Manages user-friendly progress messages."""
    
    def __init__(self) -> None:
        """Initialize the progress manager."""
        self.console = Console()
        
    def show_progress(self, message: str, success: bool = True) -> None:
        """
        Display a progress message.
        
        Args:
            message: Progress message to display
            success: Whether to show as success or info
        """
        style = "green" if success else "cyan"
        self.console.print(f"[{style}]→ {message}[/{style}]") 