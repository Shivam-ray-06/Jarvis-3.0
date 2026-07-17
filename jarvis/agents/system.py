import pyautogui
import subprocess

class SystemActionAgent:
    """Agent for controlling the host operating system (macOS targeted)."""
    
    def click(self, x: int, y: int):
        """Clicks at a specific screen coordinate."""
        try:
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        except Exception as e:
            return f"Error clicking: {e}"
            
    def type_text(self, text: str):
        """Types text using the keyboard."""
        try:
            pyautogui.write(text, interval=0.05)
            return f"Typed text successfully."
        except Exception as e:
            return f"Error typing: {e}"
            
    def run_applescript(self, script: str) -> str:
        """Executes an AppleScript command on macOS (e.g., controlling apps)."""
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip() if result.stdout else "Script executed successfully."
            else:
                return f"AppleScript error: {result.stderr.strip()}"
        except Exception as e:
            return f"Error executing AppleScript: {e}"
