import pyautogui
import base64
import io
from jarvis.core.llm import LocalLLM

class VisionAgent:
    """Agent for analyzing the screen and providing UI understanding via Vision Models (e.g. LLaVA)."""
    
    def __init__(self, model_name: str = "llava"):
        self.llm = LocalLLM(model_name=model_name)
        
    def capture_screen_base64(self) -> str:
        """Takes a screenshot of the primary screen and returns it as a base64 encoded string."""
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        # Save as JPEG for better compression when sending to local LLM
        screenshot.save(buffer, format="JPEG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return encoded_image
        
    def analyze_screen(self, prompt: str = "Describe what is on the screen and identify any UI elements.") -> str:
        """Captures the screen and asks the vision model to analyze it."""
        try:
            b64_img = self.capture_screen_base64()
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [b64_img]
                }
            ]
            
            # Use the streaming or standard generate_response depending on how we call it
            # Since generate_response only takes system/user prompt explicitly, we need to bypass or add a raw message method
            # For now, let's use the chat_stream method since it accepts raw messages list
            full_response = ""
            for chunk in self.llm.chat_stream(messages):
                full_response += chunk
                
            return full_response
        except Exception as e:
            return f"Error analyzing screen: {e}"
