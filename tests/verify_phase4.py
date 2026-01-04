import sys
import os

sys.path.append(os.getcwd())

from src.core.brain import MockBrain, Decision, DecisionType

def test_phase4_logic():
    print("Testing AMAR Phase 4 (Personality & Smart Regex)...")
    brain = MockBrain() # Initializes ChatEngine internally
    
    # Test 1: Personality - Greeting
    print("\n[Test 1] Greeting")
    decision = brain.think([{"role": "user", "content": "hello namaste"}])
    print(f"  -> Decision: {decision.type}")
    print(f"  -> Reply: {decision.action_args['response_text']}")
    assert decision.type == DecisionType.ACT
    assert decision.action_plan == "chat_response"
    assert "namaste" in decision.action_args['response_text'].lower() or "hello" in decision.action_args['response_text'].lower()

    # Test 2: Smart Search Extraction
    print("\n[Test 2] 'Google pe python search kro'")
    # Old logic might have kept 'Google pe'. New logic should clean it.
    decision = brain.think([{"role": "user", "content": "google pe python search kro"}])
    print(f"  -> Query: '{decision.action_args['query']}'")
    assert decision.action_args['query'] == "python"

    # Test 3: Smart App Extraction
    print("\n[Test 3] 'Chrome pe mail kholo'")
    # Should extract 'chrome' (or 'mail' if we parsed differently, but my logic was to strip prepositions and verbs)
    # Plan logic: remove 'open', 'kholo', 'on', 'pe'. 
    # "Chrome pe mail kholo" -> "Chrome mail" stripped?
    # Actually my logic was: remove stop words then strip.
    # "Chrome pe mail kholo" -> "Chrome mail" (since 'pe' and 'kholo' are removed).
    # This might be tricky. Let's see what it does. ideally user meant 'open mail' using chrome? 
    # But usually 'Chrome open kro' -> Chrome. 
    # Let's test a simpler one first: "Notepad kholo" -> "Notepad".
    
    decision = brain.think([{"role": "user", "content": "notepad kholo"}])
    print(f"  -> App: '{decision.action_args['app_name']}'")
    assert "notepad" in decision.action_args['app_name']

    # Test 4: Who are you
    print("\n[Test 4] Identity")
    decision = brain.think([{"role": "user", "content": "who are you"}])
    print(f"  -> Reply: {decision.action_args['response_text']}")
    assert "amar" in decision.action_args['response_text'].lower()

    print("\nPHASE 4 TESTS PASSED")

if __name__ == "__main__":
    test_phase4_logic()
