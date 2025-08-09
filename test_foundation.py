"""
🧪 Test Your Simplified Foundation
"""

from src.core.detective_state import create_investigation_state, log_progress
from config import BRAND_PATTERNS, get_search_queries
import json

def test_foundation():
    """Test that everything is working"""
    
    print("🧪 Testing Simplified Foundation...")
    
    # Test 1: State creation
    state = create_investigation_state("smart fan")
    print(f"✅ State created: {state['investigation_id']}")
    
    # Test 2: Logging system
    state = log_progress(state, "Foundation test completed")
    print(f"✅ Logging works: {len(state['investigation_log'])} entries")
    
    # Test 3: Configuration
    queries = get_search_queries("smart fan")
    print(f"✅ Search queries generated: {queries}")
    
    # Test 4: Brand patterns
    print(f"✅ Brand patterns loaded: {len(BRAND_PATTERNS)} brands")
    
    print("\n🎉 Foundation test successful!")
    print("🚀 Ready for Phase 1 Step 2: Building the LangGraph Coordinator")
    
    return state

if __name__ == "__main__":
    test_foundation()
