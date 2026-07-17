import sys
from rich.console import Console
from jarvis.agents.orchestrator import OrchestratorAgent
from jarvis.agents.voice import VoiceAgent

console = Console()

def main():
    console.print("[bold green]Initializing Jarvis 2.0 AI Operating System...[/bold green]")
    
    # Initialize the Orchestrator with the desired model
    # Note: Requires ollama to be running, e.g. `ollama run llama3`
    agent = OrchestratorAgent(model_name="llama3")
    
    console.print("[bold green]Jarvis is online and ready.[/bold green]")
    console.print("Type 'exit' or 'quit' to shutdown.")
    console.print("Type '/voice' to record audio (5s).\n")
    
    voice_agent = None

    while True:
        try:
            user_input = console.input("[bold yellow]User:[/bold yellow] ")
            clean_input = user_input.strip().lower()
            
            if clean_input in ['exit', 'quit']:
                console.print("[bold red]Shutting down Jarvis. Goodbye![/bold red]")
                break
                
            if clean_input == '/voice':
                if not voice_agent:
                    console.print("[dim italic]Initializing VoiceAgent (this may take a moment on first run)...[/dim italic]")
                    voice_agent = VoiceAgent()
                console.print("[bold cyan]Jarvis is listening for 5 seconds...[/bold cyan]")
                transcribed_text = voice_agent.listen_and_transcribe(duration=5)
                console.print(f"[bold yellow]User (Voice):[/bold yellow] {transcribed_text}")
                user_input = transcribed_text
            
            if not user_input.strip():
                continue
                
            agent.handle_input(user_input)
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Force shutting down. Goodbye![/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
