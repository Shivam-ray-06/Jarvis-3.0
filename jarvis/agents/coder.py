import subprocess
import tempfile
import os

class CoderAgent:
    """Agent responsible for writing and executing code."""
    
    def execute_python_code(self, code: str) -> str:
        """Executes python code in a subprocess and returns the output."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file_path = f.name
            
        try:
            # Run the python file, capturing stdout and stderr
            # Note: In a production environment, this should be a Docker container sandbox.
            result = subprocess.run(
                ["python3", temp_file_path],
                capture_output=True,
                text=True,
                timeout=30 # 30 seconds timeout limit
            )
            
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"\nError:\n{result.stderr}"
                
            return output if output else "Execution completed with no output."
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out after 30 seconds."
        except Exception as e:
            return f"Error executing code: {e}"
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
