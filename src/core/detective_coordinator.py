"""
🎭 Enhanced LangGraph Detective Coordinator - Multi-Platform Support
Maintains backward compatibility while adding multi-platform orchestration
"""

from langgraph.graph import StateGraph, END
from ..core.detective_state import MultiPlatformState, create_multiplatform_state, log_platform_progress
from ..core.platform_orchestrator import platform_orchestration_agent
from ..analyzers.quantitative_analyzer import quantitative_analysis_agent  
from ..analyzers.sov_calculator import sov_calculation_agent
from typing import List

def create_multiplatform_workflow() -> StateGraph:
    """
    🏢 Create Enhanced Detective Agency Workflow with Multi-Platform Support
    Backward compatible with existing Google-only workflow
    """
    
    print("🏢 Building Enhanced Multi-Platform Detective Agency Workflow...")
    
    # Create the state graph with enhanced state
    workflow = StateGraph(MultiPlatformState)
    
    # Add agent nodes
    workflow.add_node("platform_orchestrator", platform_orchestration_agent)  # NEW: Multi-platform coordination
    workflow.add_node("quantitative_analyzer", quantitative_analysis_agent)   # EXISTING: Enhanced for multi-platform
    workflow.add_node("sov_calculator", sov_calculation_agent)                # EXISTING: Enhanced for multi-platform  
    workflow.add_node("insight_generator", enhanced_insight_generation_agent) # ENHANCED: Multi-platform insights
    
    # Define the enhanced workflow
    workflow.add_edge("platform_orchestrator", "quantitative_analyzer")    # Collect All → Analyze
    workflow.add_edge("quantitative_analyzer", "sov_calculator")            # Analyze → Calculate SoV
    workflow.add_edge("sov_calculator", "insight_generator")                # Calculate → Generate Insights
    workflow.add_edge("insight_generator", END)                             # Insights → Complete
    
    # Set entry point to new orchestrator
    workflow.set_entry_point("platform_orchestrator")
    
    print("✅ Enhanced Multi-Platform Detective Workflow Created!")
    print("👥 Active Agents: Platform Orchestrator → Analyzer → Calculator → Enhanced Insight Generator")
    
    return workflow.compile()

def enhanced_insight_generation_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    💡 Enhanced Business Insight Generator with Multi-Platform Intelligence
    """
    
    print("💡 Enhanced Insight Generator: Creating multi-platform business intelligence...")
    
    enabled_platforms = state.get("enabled_platforms", ["google"])
    sov_metrics = state.get("sov_metrics", {})
    competitive_landscape = state.get("competitive_landscape", {})
    youtube_metadata = state.get("youtube_metadata", {})
    
    insights = []
    recommendations = []
    cross_platform_insights = []
    platform_recommendations = {}
    
    # Original Google insights (maintained for compatibility)
    if 'atomberg' in sov_metrics:
        atomberg_data = sov_metrics['atomberg']
        atomberg_sov = atomberg_data['overall_sov']
        
        if atomberg_sov < 15:
            insights.append(f"🚨 Low market presence: Atomberg has {atomberg_sov:.1f}% SoV")
            recommendations.append("Increase content marketing and SEO efforts")
        elif atomberg_sov < 25:
            insights.append(f"⚠️ Moderate presence: Atomberg at {atomberg_sov:.1f}% SoV")
            recommendations.append("Focus on high-engagement content to improve visibility")
        else:
            insights.append(f"✅ Strong presence: Atomberg leads with {atomberg_sov:.1f}% SoV")
    
    # NEW: Multi-Platform Insights
    if len(enabled_platforms) > 1:
        cross_platform_insights.append(f"🌐 Multi-platform analysis across {len(enabled_platforms)} channels")
        
        # YouTube-specific insights
        if "youtube" in enabled_platforms and youtube_metadata:
            videos_collected = youtube_metadata.get("videos_collected", 0)
            comments_collected = youtube_metadata.get("comments_collected", 0)
            
            if videos_collected > 0:
                cross_platform_insights.append(f"🎥 YouTube intelligence: {videos_collected} videos, {comments_collected} comments analyzed")
                
                # Video content insights
                if videos_collected < 20:
                    cross_platform_insights.append("📺 Limited video content presence - opportunity for video marketing expansion")
                    platform_recommendations["youtube"] = [
                        "Create educational content about smart fan installation",
                        "Develop product comparison videos",
                        "Partner with home improvement YouTubers"
                    ]
                else:
                    cross_platform_insights.append("🎬 Strong video content ecosystem detected")
                    platform_recommendations["youtube"] = [
                        "Optimize existing video content for better discoverability",
                        "Analyze top-performing video formats for replication"
                    ]
        
        # Google vs YouTube comparison
        if "google" in enabled_platforms and "youtube" in enabled_platforms:
            google_results = len([r for r in state.get("raw_search_results", []) if r.get("source") == "google"])
            youtube_results = len([r for r in state.get("raw_search_results", []) if r.get("source", "").startswith("youtube")])
            
            if youtube_results > google_results:
                cross_platform_insights.append("🎥 Video content dominance: More YouTube presence than traditional search")
                recommendations.append("Leverage video-first content strategy across all platforms")
            elif google_results > youtube_results * 2:
                cross_platform_insights.append("🔍 Search-heavy presence: Strong Google visibility, video content opportunity")
                recommendations.append("Expand video content creation to match search presence")
    
    # Platform-specific recommendations
    if "google" in enabled_platforms:
        platform_recommendations["google"] = [
            "Optimize for high-performing keywords identified in analysis",
            "Improve search ranking through technical SEO"
        ]
    
    print(f"💡 Generated {len(insights)} general insights, {len(cross_platform_insights)} cross-platform insights")
    
    # Update state with enhanced insights
    state = log_platform_progress(
        state, 
        "insight_generator", 
        f"Enhanced intelligence generated: {len(insights + cross_platform_insights)} total insights"
    )
    
    return {
        **state,
        "quantitative_insights": insights,
        "action_recommendations": recommendations,
        "cross_platform_insights": cross_platform_insights,
        "platform_recommendations": platform_recommendations,
        "current_phase": "enhanced_investigation_complete"
    }

def run_multiplatform_investigation(
    search_query: str = "smart fan", 
    platforms: List[str] = ["google"]
) -> MultiPlatformState:
    """
    🚀 Execute Complete Multi-Platform SoV Investigation
    Backward compatible: run_multiplatform_investigation("smart fan", ["google"]) 
    works exactly like the original run_complete_investigation()
    """
    
    print(f"\n{'='*70}")
    print(f"🎬 MULTI-PLATFORM SoV INVESTIGATION: '{search_query.upper()}'")
    print(f"📱 Platforms: {', '.join(platforms).upper()}")
    print(f"{'='*70}")
    
    # Create enhanced detective workflow
    detective_agency = create_multiplatform_workflow()
    
    # Initialize multi-platform investigation
    initial_state = create_multiplatform_state(search_query, platforms)
    
    print(f"📁 Investigation ID: {initial_state['investigation_id']}")
    print(f"🎯 Platforms enabled: {len(platforms)} ({', '.join(platforms)})")
    print(f"⏰ Started: {initial_state['start_time']}")
    
    try:
        # Execute the complete workflow
        print(f"\n🚀 Launching multi-platform investigation workflow...")
        final_state = detective_agency.invoke(initial_state)
        
        # Display results
        print(f"\n{'='*70}")
        print(f"📋 MULTI-PLATFORM INVESTIGATION COMPLETE!")
        print(f"{'='*70}")
        
        display_multiplatform_summary(final_state)
        
        return final_state
        
    except Exception as e:
        print(f"❌ Multi-platform investigation failed: {e}")
        print(f"🔧 Check agent implementations and platform configurations")
        raise

def display_multiplatform_summary(state: MultiPlatformState):
    """Display enhanced summary with multi-platform breakdown"""
    
    enabled_platforms = state.get("enabled_platforms", ["google"])
    raw_results = len(state.get("raw_search_results", []))
    
    print(f"📊 Multi-Platform Data Collection:")
    print(f"   • Platforms analyzed: {', '.join(enabled_platforms)}")
    print(f"   • Total results processed: {raw_results}")
    
    # Platform breakdown
    if len(enabled_platforms) > 1:
        google_results = len([r for r in state.get("raw_search_results", []) if r.get("source") == "google"])
        youtube_results = len([r for r in state.get("raw_search_results", []) if r.get("source", "").startswith("youtube")])
        
        print(f"   • Google results: {google_results}")
        print(f"   • YouTube results: {youtube_results}")
    
    # Brand analysis
    brands_found = len(state.get("brand_mentions", {}))
    total_mentions = sum(state.get("brand_mentions", {}).values())
    print(f"   • Brands identified: {brands_found}")  
    print(f"   • Total brand mentions: {total_mentions}")
    
    # SoV metrics
    sov_metrics = state.get("sov_metrics", {})
    if 'atomberg' in sov_metrics:
        atomberg = sov_metrics['atomberg']
        print(f"\n🎯 Atomberg Performance:")
        print(f"   • Overall SoV: {atomberg['overall_sov']:.1f}%")
        print(f"   • Mention Share: {atomberg['mention_share']:.1f}%")
        print(f"   • Engagement Share: {atomberg['engagement_share']:.1f}%")
    
    # Multi-platform insights
    cross_platform_insights = state.get("cross_platform_insights", [])
    if cross_platform_insights:
        print(f"\n🌐 Cross-Platform Insights:")
        for insight in cross_platform_insights[:3]:
            print(f"   • {insight}")
    
    # Regular insights (backward compatibility)
    insights = state.get("quantitative_insights", [])
    if insights:
        print(f"\n💡 Key Insights:")
        for insight in insights[:3]:
            print(f"   • {insight}")
    
    # Recommendations
    recommendations = state.get("action_recommendations", [])
    if recommendations:
        print(f"\n🎯 Recommended Actions:")
        for rec in recommendations[:3]:
            print(f"   • {rec}")
    
    print(f"\n⏱️ Investigation Phase: {state.get('current_phase', 'Unknown')}")

# Backward compatibility - existing function names still work
run_complete_investigation = run_multiplatform_investigation  # Alias for compatibility

print("🎭 Enhanced LangGraph Detective Coordinator Ready!")
