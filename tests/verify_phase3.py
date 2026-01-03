import sys
import os

sys.path.append(os.getcwd())

from src.core.brain import MockBrain, Decision, DecisionType
from src.tools.registry import registry
import src.tools.system_ops # Ensure registration

def test_hinglish_phase3():
    print("Testing AMAR Phase 3 (Hinglish & Terminal)...")
    brain = MockBrain()
    
    # Test 1: Hinglish Search
    print("\n[Test 1] 'Google pe python search kro'")
    decision = brain.think([{"role": "user", "content": "google pe python search kro"}])
    print(f"  -> Decision: {decision.type}")
    print(f"  -> Plan: {decision.action_plan}")
    print(f"  -> Args: {decision.action_args}")
    assert decision.action_plan == "web_search"
    assert decision.action_args["query"] == "python"

    # Test 2: Hinglish Open App
    print("\n[Test 2] 'Notepad kholo please'")
    decision = brain.think([{"role": "user", "content": "notepad kholo please"}])
    print(f"  -> Plan: {decision.action_plan}")
    assert decision.action_plan == "open_application"
    assert decision.action_args["app_name"] == "notepad"

    # Test 3: Terminal Command
    print("\n[Test 3] 'Terminal se dir run kro'")
    decision = brain.think([{"role": "user", "content": "terminal se dir run kro"}])
    print(f"  -> Decision: {decision.type}")
    print(f"  -> Args: {decision.action_args}")
    assert decision.type == DecisionType.PAUSE # Safety first!
    assert decision.action_plan == "run_terminal_command"
    assert "dir" in decision.action_args["command"]

    # Test 4: Run Terminal Tool
    print("\n[Test 4] Executing 'echo hello'")
    result = registry.execute("run_terminal_command", command="echo hello")
    print(f"  -> Result: {result}")
    assert "hello" in result.lower()

    print("\nPHASE 3 TESTS PASSED")

if __name__ == "__main__":
    test_hinglish_phase3()
