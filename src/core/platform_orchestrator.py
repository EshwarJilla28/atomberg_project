"""
🎭 Platform Orchestrator - Multi-Platform Coordination
Manages the collection and coordination of data from all platforms
"""

import asyncio
from typing import List
from ..core.detective_state import MultiPlatformState, log_platform_progress, merge_platform_results
from ..collectors.google_collector import google_search_agent  
from ..collectors.youtube_collector import youtube_intelligence_agent

class PlatformOrchestrator:
    """
    🎬 Coordinates data collection across all enabled platforms
    """
    
    def __init__(self):
        self.available_platforms = {
            "google": google_search_agent,
            "youtube": youtube_intelligence_agent,
            # Future platforms will be added here
            # "instagram": instagram_collector_agent,
            # "twitter": twitter_collector_agent,
        }
    
    def collect_all_platforms(self, state: MultiPlatformState) -> MultiPlatformState:
        """
        🚀 Execute data collection across all enabled platforms
        """
        
        enabled_platforms = state.get("enabled_platforms", ["google"])
        print(f"🎭 Platform Orchestrator: Coordinating {len(enabled_platforms)} platforms")
        
        state = log_platform_progress(
            state, 
            "orchestrator", 
            f"Starting collection across platforms: {', '.join(enabled_platforms)}"
        )
        
        # Sequential collection (for now - could be parallelized later)
        for platform in enabled_platforms:
            if platform in self.available_platforms:
                print(f"\n🔄 Executing {platform} collection...")
                
                try:
                    # Call the appropriate platform agent
                    platform_agent = self.available_platforms[platform]
                    state = platform_agent(state)
                    
                    print(f"✅ {platform} collection completed successfully")
                    
                except Exception as e:
                    error_msg = f"{platform} collection failed: {str(e)}"
                    print(f"❌ {error_msg}")
                    
                    state = {
                        **state,
                        "errors_log": state["errors_log"] + [error_msg]
                    }
            else:
                print(f"⚠️ Platform '{platform}' not yet implemented")
        
        # Merge all platform results into unified format
        state = merge_platform_results(state)
        
        # Update phase
        state = {
            **state,
            "current_phase": "multi_platform_collection_complete"
        }
        
        state = log_platform_progress(
            state,
            "orchestrator", 
            f"All platform collection completed - {len(state.get('raw_search_results', []))} total results"
        )
        
        return state

def platform_orchestration_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    🎭 Platform Orchestrator Agent - Main Entry Point for LangGraph
    """
    
    orchestrator = PlatformOrchestrator()
    return orchestrator.collect_all_platforms(state)

print("🎭 Platform Orchestrator Ready!")
