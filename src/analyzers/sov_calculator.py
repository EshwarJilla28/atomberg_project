"""
📈 Share of Voice Calculator Agent
Pure mathematical SoV calculations and competitive analysis
"""

from typing import Dict,List,Any
from ..core.detective_state import MultiPlatformState, log_platform_progress
from config import SOV_WEIGHTS

def sov_calculation_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    📊 Share of Voice Calculator
    Calculates competitive positioning using quantitative metrics
    """
    
    print("📈 SoV Calculator: Computing competitive metrics...")
    
    brand_mentions = state.get("brand_mentions", {})
    engagement_scores = state.get("engagement_scores", {})
    position_analysis = state.get("position_analysis", {})
    
    if not brand_mentions:
        print("⚠️ No brand data available for SoV calculation")
        return log_platform_progress(state, "google", "⚠️ SoV calculation skipped - no brand data")
    
    # Calculate total market metrics
    total_mentions = sum(brand_mentions.values())
    total_engagement = sum(engagement_scores.values())
    
    print(f"📊 Market Overview:")
    print(f"   • Total brand mentions: {total_mentions}")
    print(f"   • Total engagement score: {total_engagement:.1f}")
    print(f"   • Brands in competition: {len(brand_mentions)}")
    
    # Calculate SoV metrics for each brand
    sov_metrics = {}
    competitive_landscape = {}
    
    for brand in brand_mentions.keys():
        mentions = brand_mentions.get(brand, 0)
        engagement = engagement_scores.get(brand, 0)
        positions = position_analysis.get(brand, [])
        
        # Core SoV calculations
        mention_share = (mentions / total_mentions) * 100 if total_mentions > 0 else 0
        engagement_share = (engagement / total_engagement) * 100 if total_engagement > 0 else 0
        
        # Position analysis
        avg_position = sum(positions) / len(positions) if positions else 0
        top_3_appearances = len([p for p in positions if p <= 3])
        
        # Weighted overall SoV
        overall_sov = (
            mention_share * SOV_WEIGHTS['mention_weight'] +
            engagement_share * SOV_WEIGHTS['engagement_weight']
        )
        
        # Position bonus (better ranking = bonus points)
        if avg_position > 0:
            position_bonus = max(0, (10 - avg_position) * SOV_WEIGHTS['position_bonus'])
            overall_sov += position_bonus
        
        sov_metrics[brand] = {
            "mention_share": round(mention_share, 2),
            "engagement_share": round(engagement_share, 2),
            "overall_sov": round(overall_sov, 2),
            "average_position": round(avg_position, 1),
            "top_3_appearances": top_3_appearances,
            "total_mentions": mentions,
            "total_engagement": round(engagement, 1)
        }
    
    # Competitive landscape analysis
    sorted_brands = sorted(sov_metrics.items(), key=lambda x: x[1]['overall_sov'], reverse=True)
    
    competitive_landscape = {
        "market_leader": sorted_brands[0][0] if sorted_brands else None,
        "atomberg_rank": next((i+1 for i, (brand, _) in enumerate(sorted_brands) if brand == 'atomberg'), None),
        "brand_rankings": [(brand, metrics['overall_sov']) for brand, metrics in sorted_brands],
        "market_concentration": calculate_market_concentration(sov_metrics),
        "competitive_gaps": identify_competitive_gaps(sov_metrics)
    }
    
    # Focus on Atomberg's performance
    atomberg_metrics = sov_metrics.get('atomberg', {})
    atomberg_sov = atomberg_metrics.get('overall_sov', 0)
    
    print(f"\n🎯 Atomberg SoV Analysis:")
    print(f"   • Overall SoV: {atomberg_sov:.1f}%")
    print(f"   • Market Rank: #{competitive_landscape.get('atomberg_rank', 'Not ranked')}")
    print(f"   • Mention Share: {atomberg_metrics.get('mention_share', 0):.1f}%")
    print(f"   • Engagement Share: {atomberg_metrics.get('engagement_share', 0):.1f}%")
    
    # Update state
    state = log_platform_progress(state,"google", f"📈 SoV calculation completed: Atomberg {atomberg_sov:.1f}% overall SoV")
    
    return {
        **state,
        "sov_metrics": sov_metrics,
        "competitive_landscape": competitive_landscape,
        "current_phase": "sov_calculation_complete"
    }

def calculate_market_concentration(sov_metrics: Dict[str, Any]) -> str:
    """Calculate if market is concentrated or fragmented"""
    if not sov_metrics:
        return "unknown"
    
    top_brand_sov = max(metrics['overall_sov'] for metrics in sov_metrics.values())
    
    if top_brand_sov > 50:
        return "highly_concentrated"
    elif top_brand_sov > 30:
        return "moderately_concentrated"
    else:
        return "fragmented"

def identify_competitive_gaps(sov_metrics: Dict[str, Any]) -> List[str]:
    """Identify competitive opportunities"""
    gaps = []
    
    if 'atomberg' in sov_metrics:
        atomberg_sov = sov_metrics['atomberg']['overall_sov']
        
        # Find brands significantly ahead
        stronger_competitors = [
            brand for brand, metrics in sov_metrics.items() 
            if brand != 'atomberg' and metrics['overall_sov'] > atomberg_sov + 10
        ]
        
        if stronger_competitors:
            gaps.append(f"Significant SoV gap vs {', '.join(stronger_competitors)}")
        
        if atomberg_sov < 20:
            gaps.append("Below 20% SoV threshold - needs increased market presence")
        
        # Position analysis
        atomberg_pos = sov_metrics['atomberg'].get('average_position', 0)
        if atomberg_pos > 5:
            gaps.append("Average search position beyond top 5 - SEO opportunity")
    
    return gaps

print("📈 SoV Calculator Agent Ready!")
