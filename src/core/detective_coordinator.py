"""
🎭 Enhanced LangGraph Detective Coordinator - Multi-Platform Support
Maintains backward compatibility while adding multi-platform orchestration
"""

from langgraph.graph import StateGraph, END
from ..core.detective_state import MultiPlatformState, create_multiplatform_state
from ..core.platform_orchestrator import platform_orchestration_agent
from ..analyzers.quantitative_analyzer import quantitative_analysis_agent  
from ..analyzers.sov_calculator import sov_calculation_agent
from ..analyzers.competitive_scoring_analyzer import competitive_scoring_agent
from typing import List

def create_multiplatform_workflow() -> StateGraph:
    """
    🏢 Create Enhanced Detective Agency Workflow with Competitive Intelligence
    """
    
    print("🏢 Building Enhanced Multi-Platform Detective Agency Workflow...")
    
    # Create the state graph with enhanced state
    workflow = StateGraph(MultiPlatformState)
    
    # Add agent nodes
    workflow.add_node("platform_orchestrator", platform_orchestration_agent)
    workflow.add_node("quantitative_analyzer", quantitative_analysis_agent)
    workflow.add_node("sov_calculator", sov_calculation_agent)
    workflow.add_node("competitive_scorer", competitive_scoring_agent)  # NEW
    workflow.add_node("insight_generator", enhanced_insight_generation_agent)
    
    # Define the enhanced workflow with competitive scoring
    workflow.add_edge("platform_orchestrator", "quantitative_analyzer")
    workflow.add_edge("quantitative_analyzer", "sov_calculator")
    workflow.add_edge("sov_calculator", "competitive_scorer")  # NEW: Add competitive scoring
    workflow.add_edge("competitive_scorer", "insight_generator")
    workflow.add_edge("insight_generator", END)
    
    # Set entry point
    workflow.set_entry_point("platform_orchestrator")
    
    print("✅ Enhanced Multi-Platform Detective Workflow Created!")
    print("👥 Active Agents: Platform Orchestrator → Analyzer → Calculator → Competitive Scorer → Insight Generator")
    
    return workflow.compile()

def enhanced_insight_generation_agent(state: MultiPlatformState) -> MultiPlatformState:
    print("💡 Enhanced Insight Generator: Creating advanced competitive business intelligence...")
    
    focus_brand = state.get("focus_brand", "atomberg")
    
    # Get competitive intelligence - it should be there now
    competitive_intelligence = state.get("competitive_intelligence", {})
    print(f"🔧 DEBUG: Competitive intelligence found: {bool(competitive_intelligence)}")
    
    if competitive_intelligence and not competitive_intelligence.get("error"):
        competitive_insights = competitive_intelligence.get("competitive_insights", [])
        print(f"🔧 DEBUG: Found {len(competitive_insights)} competitive insights")
        
        # Process competitive recommendations
        competitive_recommendations = []
        if "competitive_scores" in competitive_intelligence:
            competitive_scores = competitive_intelligence["competitive_scores"]
            if focus_brand in competitive_scores:
                brand_data = competitive_scores[focus_brand]
                if brand_data["market_presence"] < 70:
                    competitive_recommendations.append("Increase market presence through content marketing")
                if brand_data["engagement_quality"] < 70:
                    competitive_recommendations.append("Improve content quality to enhance engagement")
    else:
        competitive_insights = []
        competitive_recommendations = []
        print("⚠️ No competitive intelligence found or error occurred")
    
    # Get existing insights
    existing_insights = state.get("quantitative_insights", [])
    existing_recommendations = state.get("action_recommendations", [])
    
    # Combine insights
    all_insights = existing_insights + competitive_insights
    all_recommendations = existing_recommendations + competitive_recommendations
    
    print(f"💡 Generated: {len(all_insights)} insights, {len(all_recommendations)} recommendations")
    
    # Return only the updates
    return {
        "quantitative_insights": all_insights,
        "action_recommendations": all_recommendations,
        "current_phase": "enhanced_investigation_complete"
    }

def run_multiplatform_investigation(
    search_query: str = "smart fan", 
    platforms: List[str] = ["google"],
    focus_brand: str = "atomberg"
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
    initial_state["focus_brand"] = focus_brand
    
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
    platform_breakdown = {}
    if len(enabled_platforms) > 1:
        google_results = len([r for r in state.get("raw_search_results", []) if r.get("source") == "google"])
        youtube_results = len([r for r in state.get("raw_search_results", []) if r.get("source", "").startswith("youtube")])
        
        print(f"   • Google results: {google_results}")
        print(f"   • YouTube results: {youtube_results}")
        platform_breakdown = {
            "platforms": enabled_platforms,
            "results_count": {
                "google": google_results,
                "youtube": youtube_results
            }
        }
    else:
        # Even if single platform, count results for it
        platform_breakdown = {
            "platforms": enabled_platforms,
            "results_count": {
                enabled_platforms[0]: raw_results
            }
        }
    
    # Attach platform breakdown to state for possible saving
    state["platform_breakdown"] = platform_breakdown
    
    # Brand analysis
    brands_found = len(state.get("brand_mentions", {}))
    total_mentions = sum(state.get("brand_mentions", {}).values())
    print(f"   • Brands identified: {brands_found}")  
    print(f"   • Total brand mentions: {total_mentions}")
    
    # SoV metrics
    sov_metrics = state.get("sov_metrics", {})
    focus_brand = state.get("focus_brand", "atomberg")
    if focus_brand in sov_metrics:
        brand_metrics = sov_metrics[focus_brand]
        print(f"\n🎯 {focus_brand.capitalize()} Performance:")
        print(f"   • Overall SoV: {brand_metrics['overall_sov']:.1f}%")
        print(f"   • Mention Share: {brand_metrics['mention_share']:.1f}%")
        print(f"   • Engagement Share: {brand_metrics['engagement_share']:.1f}%")
    
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

    # Add competitive intelligence summary
    competitive_intelligence = state.get("competitive_intelligence", {})
    if competitive_intelligence and "competitive_scores" in competitive_intelligence:
        print(f"\n🏆 Competitive Intelligence Analysis:")
        
        competitive_scores = competitive_intelligence["competitive_scores"]
        
        # Show focus brand's competitive score
        if focus_brand in competitive_scores:
            brand_data = competitive_scores[focus_brand]
            total_score = brand_data["total_score"]
            tier = brand_data["performance_tier"]
            cai = brand_data.get("competitive_advantage_index", 0)
            
            print(f"   • {focus_brand.capitalize()} Competitive Score: {total_score:.1f}/100 ({tier})")
            print(f"   • Competitive Advantage Index: {cai:+.2f}")
        
        # Show top competitors
        sorted_competitors = sorted(competitive_scores.items(), 
                                  key=lambda x: x[1]["total_score"], reverse=True)
        
        print(f"   • Market leader: {sorted_competitors[0][0]} ({sorted_competitors[0][1]['total_score']:.1f}/100)")
        
        # Show market positioning
        market_positioning = competitive_intelligence.get("market_positioning", {})
        if focus_brand in market_positioning:
            position = market_positioning[focus_brand]["position"]
            print(f"   • {focus_brand.capitalize()} position: {position}")

    else:
        print(f"\n⚠️ Competitive intelligence not available in final state")

# Backward compatibility - existing function names still work
run_complete_investigation = run_multiplatform_investigation  # Alias for compatibility

print("🎭 Enhanced LangGraph Detective Coordinator Ready!")
