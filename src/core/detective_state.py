"""
🧠 Detective State Management - Quantitative Focus
Pure math and counting - no NLP complexity!
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class QuantitativeState(TypedDict):
    """
    📊 Quantitative Investigation State
    Everything measurable, nothing subjective!
    """
    
    # === MISSION PARAMETERS ===
    search_query: str
    target_results: int
    investigation_id: str
    
    # === PROGRESS TRACKING ===
    current_phase: str
    start_time: str
    investigation_log: List[str]
    errors_log: List[str]
    
    # === RAW DATA COLLECTION ===
    raw_search_results: List[Dict[str, Any]]
    search_metadata: Dict[str, Any]
    
    # === QUANTITATIVE ANALYSIS ===
    brand_mentions: Dict[str, int]           # Pure counting
    engagement_scores: Dict[str, float]      # Math-based scoring  
    keyword_frequency: Dict[str, int]        # Word counting
    position_analysis: Dict[str, List[int]]  # Ranking positions
    
    # === BUSINESS METRICS ===
    sov_metrics: Dict[str, float]           # Share of Voice calculations
    competitive_landscape: Dict[str, Any]    # Market positioning
    content_gaps: List[str]                 # Opportunity identification
    
    # === INSIGHTS & RECOMMENDATIONS ===
    quantitative_insights: List[str]        # Data-driven insights
    action_recommendations: List[str]       # Business recommendations

def create_investigation_state(search_query: str = "smart fan") -> QuantitativeState:
    """
    🎬 Initialize a new quantitative investigation
    """
    investigation_id = f"sov_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return QuantitativeState(
        # Mission setup
        search_query=search_query,
        target_results=50,
        investigation_id=investigation_id,
        
        # Progress tracking
        current_phase="initialized",
        start_time=datetime.now().isoformat(),
        investigation_log=[f"🎯 Investigation '{investigation_id}' started for query: '{search_query}'"],
        errors_log=[],
        
        # Data collection
        raw_search_results=[],
        search_metadata={},
        
        # Analysis results
        brand_mentions={},
        engagement_scores={},
        keyword_frequency={},
        position_analysis={},
        
        # Business intelligence
        sov_metrics={},
        competitive_landscape={},
        content_gaps=[],
        
        # Insights
        quantitative_insights=[],
        action_recommendations=[]
    )

def log_progress(state: QuantitativeState, message: str) -> QuantitativeState:
    """📝 Add progress entry with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    updated_log = state["investigation_log"] + [log_entry]
    return {**state, "investigation_log": updated_log}

def log_error(state: QuantitativeState, error: str, recovery: str) -> QuantitativeState:
    """🚨 Log error with recovery action"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    error_entry = f"[{timestamp}] ❌ {error} | Recovery: {recovery}"
    
    updated_errors = state["errors_log"] + [error_entry]
    updated_log = state["investigation_log"] + [error_entry]
    
    return {
        **state,
        "errors_log": updated_errors, 
        "investigation_log": updated_log
    }

print("🧠 Quantitative Detective State Management Ready!")
