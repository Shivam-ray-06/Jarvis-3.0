import json
import urllib.request
from typing import List, Dict, Any, Optional


class LocalLLM:
    """Wrapper for Ollama to manage local LLM interactions via REST API."""
    
    def __init__(self, model_name: str = "llama3", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, stream: bool = False):
        """Send a chat request to the local LLM, optionally with tools."""
        url = f"{self.host}/api/chat"
        data = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream
        }
        if tools:
            data["tools"] = tools
            
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as response:
                if stream:
                    for line in response:
                        if line:
                            chunk = json.loads(line.decode("utf-8"))
                            message = chunk.get("message", {})
                            if "content" in message and message["content"]:
                                yield message["content"]
                else:
                    result = json.loads(response.read().decode("utf-8"))
                    return result.get("message", {})
        except Exception as e:
            if stream:
                yield f"Error: {e}"
            else:
                return {"role": "assistant", "content": f"Error connecting to local LLM ({self.model_name}): {e}\nPlease make sure Ollama is running."}

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Legacy method for simple prompt/response."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.chat(messages, stream=False)
        return response.get("content", "")

    def chat_stream(self, messages: List[Dict[str, str]]):
        """Legacy method for streaming chat without tools."""
        return self.chat(messages, stream=True)
