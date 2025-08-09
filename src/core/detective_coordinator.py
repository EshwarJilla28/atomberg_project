"""
🎭 LangGraph Detective Coordinator  
The master orchestrator that coordinates all agents using LangGraph
"""

from langgraph.graph import StateGraph, END
from ..core.detective_state import QuantitativeState, create_investigation_state, log_progress
from ..collectors.google_collector import google_search_agent
from ..analyzers.quantitative_analyzer import quantitative_analysis_agent
from ..analyzers.sov_calculator import sov_calculation_agent

def create_detective_workflow() -> StateGraph:
    """
    🏢 Create the Detective Agency Workflow
    Uses LangGraph to coordinate the investigation process
    """
    
    print("🏢 Building AI Detective Agency Workflow...")
    
    # Create the state graph
    workflow = StateGraph(QuantitativeState)
    
    # Add agent nodes
    workflow.add_node("google_collector", google_search_agent)
    workflow.add_node("quantitative_analyzer", quantitative_analysis_agent)  
    workflow.add_node("sov_calculator", sov_calculation_agent)
    workflow.add_node("insight_generator", insight_generation_agent)
    
    # Define the investigation flow
    workflow.add_edge("google_collector", "quantitative_analyzer")     # Collect → Analyze
    workflow.add_edge("quantitative_analyzer", "sov_calculator")       # Analyze → Calculate SoV
    workflow.add_edge("sov_calculator", "insight_generator")           # Calculate → Generate Insights
    workflow.add_edge("insight_generator", END)                        # Insights → Complete
    
    # Set entry point
    workflow.set_entry_point("google_collector")
    
    print("✅ Detective Workflow Created!")
    print("👥 Active Agents: Collector → Analyzer → Calculator → Insight Generator")
    
    return workflow.compile()

def insight_generation_agent(state: QuantitativeState) -> QuantitativeState:
    """
    💡 Business Insight Generator
    Converts quantitative analysis into actionable business recommendations
    """
    
    print("💡 Insight Generator: Creating business intelligence...")
    
    sov_metrics = state.get("sov_metrics", {})
    competitive_landscape = state.get("competitive_landscape", {})
    brand_mentions = state.get("brand_mentions", {})
    keyword_frequency = state.get("keyword_frequency", {})
    
    insights = []
    recommendations = []
    
    # Atomberg-specific analysis
    if 'atomberg' in sov_metrics:
        atomberg_data = sov_metrics['atomberg']
        atomberg_sov = atomberg_data['overall_sov']
        atomberg_rank = competitive_landscape.get('atomberg_rank', 0)
        
        # SoV Performance Insights
        if atomberg_sov < 15:
            insights.append(f"🚨 Low market presence: Atomberg has {atomberg_sov:.1f}% SoV - significant growth opportunity")
            recommendations.append("Increase content marketing and SEO efforts for 'smart fan' keywords")
        elif atomberg_sov < 25:
            insights.append(f"⚠️ Moderate presence: Atomberg at {atomberg_sov:.1f}% SoV - room for improvement")
            recommendations.append("Focus on high-engagement content to improve visibility")
        else:
            insights.append(f"✅ Strong presence: Atomberg leads with {atomberg_sov:.1f}% SoV")
        
        # Competitive Position Insights  
        if atomberg_rank and atomberg_rank > 1:
            market_leader = competitive_landscape.get('market_leader')
            insights.append(f"🥈 Atomberg ranks #{atomberg_rank} - {market_leader} currently leads the conversation")
            recommendations.append(f"Analyze {market_leader}'s content strategy for competitive insights")
        
        # Position Analysis
        avg_position = atomberg_data.get('average_position', 0)
        if avg_position > 3:
            insights.append(f"📍 SEO opportunity: Atomberg appears at position {avg_position:.1f} on average")
            recommendations.append("Optimize content for better search ranking - target top 3 positions")
    
    # Market Structure Insights
    concentration = competitive_landscape.get('market_concentration', '')
    if concentration == 'fragmented':
        insights.append("🌀 Fragmented market: No dominant player - opportunity for Atomberg to capture leadership")
        recommendations.append("Aggressive content marketing campaign to establish thought leadership")
    elif concentration == 'highly_concentrated':
        leader = competitive_landscape.get('market_leader')
        insights.append(f"🏰 Concentrated market: {leader} dominates - requires strategic approach")
        recommendations.append("Focus on niche positioning and unique value propositions")
    
    # Keyword Opportunity Analysis
    top_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_keywords:
        high_volume_keyword = top_keywords[0][0]
        insights.append(f"🔑 High-opportunity keyword: '{high_volume_keyword}' shows strong search volume")
        recommendations.append(f"Create targeted content around '{high_volume_keyword}' to capture search traffic")
    
    # Content Gap Analysis
    gaps = competitive_landscape.get('competitive_gaps', [])
    for gap in gaps:
        insights.append(f"📊 {gap}")
        if "SEO opportunity" in gap:
            recommendations.append("Implement technical SEO improvements and content optimization")
        elif "SoV gap" in gap:
            recommendations.append("Increase brand mention frequency through PR and content marketing")
    
    print(f"💡 Generated {len(insights)} insights and {len(recommendations)} recommendations")
    
    # Update state with insights
    state = log_progress(state, f"💡 Business intelligence generated: {len(insights)} insights, {len(recommendations)} actions")
    
    return {
        **state,
        "quantitative_insights": insights,
        "action_recommendations": recommendations,
        "current_phase": "investigation_complete"
    }

def run_complete_investigation(search_query: str = "smart fan") -> QuantitativeState:
    """
    🚀 Execute Complete SoV Investigation
    The main function that runs the entire detective workflow
    """
    
    print(f"\n{'='*70}")
    print(f"🎬 ATOMBERG SoV INVESTIGATION: '{search_query.upper()}'")
    print(f"{'='*70}")
    
    # Create detective workflow
    detective_agency = create_detective_workflow()
    
    # Initialize investigation
    initial_state = create_investigation_state(search_query)
    
    print(f"📁 Investigation ID: {initial_state['investigation_id']}")
    print(f"🎯 Target: {initial_state['target_results']} search results")
    print(f"⏰ Started: {initial_state['start_time']}")
    
    try:
        # Execute the complete workflow
        print(f"\n🚀 Launching investigation workflow...")
        final_state = detective_agency.invoke(initial_state)
        
        # Display results
        print(f"\n{'='*70}")
        print(f"📋 INVESTIGATION COMPLETE!")
        print(f"{'='*70}")
        
        display_investigation_summary(final_state)
        
        return final_state
        
    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        print(f"🔧 Check agent implementations and configurations")
        raise

def display_investigation_summary(state: QuantitativeState):
    """Display a beautiful summary of the investigation results"""
    
    # Basic metrics
    raw_results = len(state.get("raw_search_results", []))
    brands_found = len(state.get("brand_mentions", {}))
    total_mentions = sum(state.get("brand_mentions", {}).values())
    
    print(f"📊 Data Collection:")
    print(f"   • Search results processed: {raw_results}")
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
        print(f"   • Average Position: {atomberg['average_position']:.1f}")
    
    # Top insights
    insights = state.get("quantitative_insights", [])[:3]
    if insights:
        print(f"\n💡 Key Insights:")
        for insight in insights:
            print(f"   • {insight}")
    
    # Top recommendations  
    recommendations = state.get("action_recommendations", [])[:3]
    if recommendations:
        print(f"\n🎯 Recommended Actions:")
        for rec in recommendations:
            print(f"   • {rec}")
    
    print(f"\n⏱️ Investigation Phase: {state.get('current_phase', 'Unknown')}")

print("🎭 LangGraph Detective Coordinator Ready!")
