from typing import List, Dict, Any
from jarvis.core.llm import LocalLLM
from jarvis.agents.browser import BrowserAgent
from jarvis.agents.coder import CoderAgent
from jarvis.agents.document import DocumentAgent
from jarvis.agents.system import SystemActionAgent
from jarvis.agents.vision import VisionAgent
from jarvis.core.memory import MemoryManager
from rich.console import Console

console = Console()

class OrchestratorAgent:
    """The main agent that analyzes user input and delegates tasks."""

    def __init__(self, model_name: str = "llama3"):
        self.llm = LocalLLM(model_name=model_name)
        
        # Initialize sub-agents
        self.browser = BrowserAgent()
        self.coder = CoderAgent()
        self.document = DocumentAgent()
        self.system = SystemActionAgent()
        self.vision = VisionAgent()
        
        # Initialize memory
        self.memory = MemoryManager()
        
        self.system_prompt = (
            "You are Jarvis, an advanced AI Operating System. "
            "You have access to tools that can execute python code, browse the web, "
            "extract text from PDFs, and run AppleScript commands. "
            "You are currently in Phase 2 (Integrated Tools). "
            "Use the provided tools to accomplish complex tasks for the user. "
            "Always be helpful, concise, and futuristic in your responses."
        )
        self.conversation_history: List[Dict[str, Any]] = [
            {'role': 'system', 'content': self.system_prompt}
        ]
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_python_code",
                    "description": "Executes python code in a subprocess and returns the output.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "The Python code to execute."}
                        },
                        "required": ["code"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_page_content",
                    "description": "Navigates to a URL and returns its text content.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "The URL to fetch."}
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "extract_text_from_pdf",
                    "description": "Reads a PDF file and extracts its text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "The absolute path to the PDF file."}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_applescript",
                    "description": "Executes an AppleScript command on macOS.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "script": {"type": "string", "description": "The AppleScript code to run."}
                        },
                        "required": ["script"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_screen",
                    "description": "Takes a screenshot of the primary screen and analyzes it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string", "description": "The prompt to ask about the screen."}
                        },
                        "required": ["prompt"]
                    }
                }
            }
        ]

    def handle_input(self, user_input: str):
        """Processes user input, optionally calling tools, and returns the response."""
        
        # Check memory
        memory_context = self.memory.retrieve(user_input)
        if memory_context:
            context_message = f"Relevant context from past memory:\n{memory_context}\n\nUser Input:\n{user_input}"
        else:
            context_message = user_input
            
        self.conversation_history.append({'role': 'user', 'content': context_message})
        
        console.print("\n[bold cyan]Jarvis:[/bold cyan] ", end="", flush=True)
        
        while True:
            response = self.llm.chat(self.conversation_history, tools=self.tools, stream=False)
            
            if response.get("tool_calls"):
                self.conversation_history.append(response)
                for tool_call in response["tool_calls"]:
                    function = tool_call["function"]
                    name = function["name"]
                    args = function.get("arguments", {})
                    
                    console.print(f"\n[dim italic]Jarvis is using tool: {name}...[/dim italic]", end="", flush=True)
                    
                    if name == "execute_python_code":
                        result = self.coder.execute_python_code(args.get("code", ""))
                    elif name == "fetch_page_content":
                        result = self.browser.fetch_page_content(args.get("url", ""))
                    elif name == "extract_text_from_pdf":
                        result = self.document.extract_text_from_pdf(args.get("file_path", ""))
                    elif name == "run_applescript":
                        result = self.system.run_applescript(args.get("script", ""))
                    elif name == "analyze_screen":
                        result = self.vision.analyze_screen(args.get("prompt", "Describe what is on the screen."))
                    else:
                        result = f"Unknown tool: {name}"
                        
                    self.conversation_history.append({
                        "role": "tool",
                        "content": result,
                        "name": name
                    })
                # Loop back to let the LLM generate the next response with tool results
            else:
                # Final response
                content = response.get("content", "")
                print(content)
                self.conversation_history.append(response)
                
                # Store interaction in memory
                if content:
                    self.memory.store(user_input, content)
                    
                break
