"""
🔄 Backward Compatibility Layer
Ensures existing Google-only code continues to work unchanged
"""

from .detective_state import MultiPlatformState, create_multiplatform_state

# Backward compatibility aliases
QuantitativeState = MultiPlatformState
create_investigation_state = create_multiplatform_state

def ensure_google_only_compatibility(state: MultiPlatformState) -> MultiPlatformState:
    """
    Ensure that Google-only workflows continue to work exactly as before
    """
    
    # If only Google is enabled, maintain original behavior
    if state["enabled_platforms"] == ["google"]:
        # Ensure original field names work
        if not state.get("raw_search_results") and state.get("youtube_results"):
            # This shouldn't happen, but safety check
            state = {**state, "raw_search_results": []}
    
    return state

print("🔄 Backward Compatibility Layer Ready!")
