"""
🧠 Enhanced Detective State Management - Multi-Platform Support
Maintains backward compatibility while adding YouTube intelligence
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class MultiPlatformState(TypedDict):
    """
    📊 Enhanced State for Multi-Platform Intelligence
    Backward compatible with existing Google-only workflow
    """
    
    # === EXISTING FIELDS (Unchanged for compatibility) ===
    search_query: str
    target_results: int
    investigation_id: str
    current_phase: str
    start_time: str
    investigation_log: List[str]
    errors_log: List[str]
    
    # Original Google-specific fields (maintained for backward compatibility)
    raw_search_results: List[Dict[str, Any]]    # Google results
    search_metadata: Dict[str, Any]             # Google metadata
    
    # Original analysis fields (now enhanced for multi-platform)
    brand_mentions: Dict[str, int]
    sentiment_scores: Dict[str, float] 
    engagement_scores: Dict[str, float]
    keyword_frequency: Dict[str, int]
    position_analysis: Dict[str, List[int]]
    processed_content: List[Dict[str, Any]]
    
    # Original business intelligence (enhanced)
    sov_metrics: Dict[str, float]
    competitive_landscape: Dict[str, Any]
    quantitative_insights: List[str]
    action_recommendations: List[str]
    
    # === NEW MULTI-PLATFORM FIELDS ===
    # Platform Configuration
    enabled_platforms: List[str]                # ["google", "youtube"]
    platform_configs: Dict[str, Dict]           # Platform-specific settings
    
    # Platform-Specific Data Collection
    youtube_results: List[Dict[str, Any]]       # YouTube videos & comments
    youtube_metadata: Dict[str, Any]            # YouTube collection stats
    
    # Future platform placeholders
    instagram_results: List[Dict[str, Any]]     # For Phase 4B
    twitter_results: List[Dict[str, Any]]       # For Phase 4C
    
    # Unified Multi-Platform Analysis
    platform_sov_breakdown: Dict[str, Dict]     # SoV per platform
    overall_digital_sov: Dict[str, float]       # Unified cross-platform SoV
    content_type_analysis: Dict[str, Any]       # Video vs text performance
    cross_platform_insights: List[str]          # Multi-platform opportunities
    
    # Enhanced Business Intelligence
    platform_recommendations: Dict[str, List[str]]  # Platform-specific actions
    influencer_opportunities: List[Dict[str, Any]]   # Key accounts identified

def create_multiplatform_state(
    search_query: str = "smart fan", 
    platforms: List[str] = ["google"]
) -> MultiPlatformState:
    """
    🎬 Create Enhanced Investigation State with Platform Selection
    
    Backward compatible: create_multiplatform_state() works exactly like 
    create_investigation_state() for Google-only investigations
    """
    
    investigation_id = f"sov_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return MultiPlatformState(
        # Existing fields (unchanged)
        search_query=search_query,
        target_results=50,  # Will be distributed across platforms
        investigation_id=investigation_id,
        current_phase="initialized",
        start_time=datetime.now().isoformat(),
        investigation_log=[f"🎯 Multi-platform investigation '{investigation_id}' started"],
        errors_log=[],
        
        # Original data structures (maintained)
        raw_search_results=[],
        search_metadata={},
        brand_mentions={},
        sentiment_scores={}, 
        engagement_scores={},
        keyword_frequency={},
        position_analysis={},
        processed_content=[],
        sov_metrics={},
        competitive_landscape={},
        quantitative_insights=[],
        action_recommendations=[],
        
        # New multi-platform fields
        enabled_platforms=platforms,
        platform_configs=generate_platform_configs(platforms),
        
        # Platform-specific results
        youtube_results=[],
        youtube_metadata={},
        instagram_results=[],
        twitter_results=[],
        
        # Cross-platform analysis
        platform_sov_breakdown={},
        overall_digital_sov={},
        content_type_analysis={},
        cross_platform_insights=[],
        platform_recommendations={},
        influencer_opportunities=[]
    )

def generate_platform_configs(platforms: List[str]) -> Dict[str, Dict]:
    """Generate configuration for each enabled platform"""
    
    configs = {}
    
    if "google" in platforms:
        configs["google"] = {
            "target_results": 50 // len(platforms),  # Distribute results
            "human_like_delays": True,
            "stealth_mode": True
        }
    
    if "youtube" in platforms:
        configs["youtube"] = {
            "target_videos": 25,
            "target_comments_per_video": 20,
            "include_channel_analysis": True,
            "max_video_age_days": 365  # Only videos from last year
        }
    
    return configs

def log_platform_progress(state: MultiPlatformState, platform: str, message: str) -> MultiPlatformState:
    """📝 Log progress for specific platform"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] 🎬 {platform.upper()}: {message}"
    
    updated_log = state["investigation_log"] + [log_entry]
    return {**state, "investigation_log": updated_log}

def merge_platform_results(state: MultiPlatformState) -> MultiPlatformState:
    """
    🔄 Merge results from all platforms into unified structures
    Maintains backward compatibility with existing analyzers
    """
    
    all_results = []
    
    # Add Google results (existing format)
    if state.get("raw_search_results"):
        all_results.extend(state["raw_search_results"])
    
    # Add YouTube results (converted to unified format)
    if state.get("youtube_results"):
        unified_youtube = convert_youtube_to_unified_format(state["youtube_results"])
        all_results.extend(unified_youtube)
    
    # Update the main results field for backward compatibility
    return {
        **state,
        "raw_search_results": all_results,  # Maintains compatibility
        "unified_results": all_results      # New unified field
    }

def convert_youtube_to_unified_format(youtube_results: List[Dict]) -> List[Dict]:
    """Convert YouTube results to match Google result format"""
    
    unified = []
    
    for item in youtube_results:
        if item.get("type") == "video":
            unified.append({
                "id": f"youtube_video_{item['video_id']}",
                "title": item["title"],
                "url": f"https://www.youtube.com/watch?v={item['video_id']}",
                "snippet": item["description"][:500],
                "search_query": item.get("search_query", ""),
                "position": item.get("position", 0),
                "timestamp": item["published_at"],
                "source": "youtube_video",
                "engagement_data": {
                    "views": item.get("view_count", 0),
                    "likes": item.get("like_count", 0),
                    "comments": item.get("comment_count", 0)
                }
            })
        elif item.get("type") == "comment":
            unified.append({
                "id": f"youtube_comment_{item['comment_id']}",
                "title": f"Comment on: {item.get('video_title', 'YouTube Video')}",
                "url": f"https://www.youtube.com/watch?v={item['video_id']}",
                "snippet": item["text"][:500],
                "search_query": item.get("search_query", ""),
                "position": 0,
                "timestamp": item["published_at"], 
                "source": "youtube_comment",
                "engagement_data": {
                    "likes": item.get("like_count", 0)
                }
            })
    
    return unified

print("🧠 Enhanced Multi-Platform Detective State Ready!")

def log_error(state: MultiPlatformState, error_msg: str, recovery_msg: str) -> MultiPlatformState:
    """
    🚨 Log error with recovery action to the investigation state
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    error_entry = f"[{timestamp}] ❌ ERROR: {error_msg} | Recovery: {recovery_msg}"
    
    updated_errors = state.get("errors_log", []) + [error_entry]
    updated_log = state.get("investigation_log", []) + [error_entry]
    
    return {
        **state,
        "errors_log": updated_errors,
        "investigation_log": updated_log
    }

