import subprocess
from ..tools.registry import registry

@registry.register("run_terminal_command", "Executes a shell command. HIGH RISK.", safety_level="RISKY")
def run_terminal_command(command: str):
    try:
        # Capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        return f"Output:\n{output}"
    except Exception as e:
        return f"Command Failed: {e}"

@registry.register("terminal_search", "Uses curl/requests to fetch info without browser (Simulated)")
def terminal_search(query: str):
    # Real implementation would use googlesearch-python or similar. 
    # For now, we simulate a 'quick answer' or just confirm we would search.
    # To be useful, let's just use the Run Command to ping or similar, OR just return a note.
    # User wanted "terminal se kre" -> implies automation.
    return f"Use 'run_terminal_command' to execute specific tasks, or I can search web: {query}"
