import sys
import os

# Add root to python path
sys.path.append(os.getcwd())

from src.core.brain import MockBrain, Decision, DecisionType
from src.tools.registry import registry
import src.tools.automation # Ensure registered

def test_phase2_logic():
    print("Testing AMAR Phase 2 (Voice & Automation)...")
    brain = MockBrain()
    
    # Test 1: Search Intent
    try:
        # Test 1: Search Intent
        print("\n[Test 1] Web Search")
        user_msg = "search for AI agents"
        decision = brain.think([{"role": "user", "content": user_msg}])
        print(f"  -> Decision: {decision.type}")
        print(f"  -> Plan: {decision.action_plan}")
        print(f"  -> Args: {decision.action_args}")
        
        assert decision.type == DecisionType.ACT
        assert decision.action_plan == "web_search"
        assert decision.action_args["query"] == "ai agents"

        # Test 2: Open App Intent
        print("\n[Test 2] Open Application")
        user_msg = "open notepad"
        decision = brain.think([{"role": "user", "content": user_msg}])
        print(f"  -> Plan: {decision.action_plan}")
        print(f"  -> Args: {decision.action_args}")
        
        assert decision.action_plan == "open_application"
        assert decision.action_args["app_name"] == "notepad"

        # Test 3: WhatsApp Intent
        print("\n[Test 3] WhatsApp Sending")
        user_msg = "send whatsapp message"
        decision = brain.think([{"role": "user", "content": user_msg}])
        print(f"  -> Decision: {decision.type}")
        print(f"  -> Question: {decision.question}")
        
        assert decision.type == DecisionType.PAUSE
        assert decision.action_plan == "send_whatsapp"

        # Test 4: Registry Check
        print("\n[Test 4] Tool Registry")
        tool = registry.get_tool("web_search")
        assert tool is not None
        print(f"  -> Found tool: {tool.name}")

        print("\nPHASE 2 TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase2_logic()
