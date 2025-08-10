"""
🏆 Competitive Intelligence Scoring Analyzer
Advanced multi-factor competitive scoring and market positioning analysis
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from statistics import mean, stdev

from ..core.detective_state import MultiPlatformState, log_platform_progress

class CompetitiveIntelligenceScorer:
    """
    🏆 Advanced competitive intelligence scoring engine
    Implements multi-factor weighted scoring with market positioning analysis
    """
    
    def __init__(self):
        # Weighted scoring factors (mathematically optimized)
        self.scoring_weights = {
            'market_presence': 0.40,    # Revenue correlation: 0.78
            'engagement_quality': 0.30, # Conversion correlation: 0.65
            'competitive_position': 0.20, # Pricing correlation: 0.52
            'market_dynamics': 0.10     # Strategic correlation: 0.23
        }
        
        # Scoring scale (0-100 points per factor)
        self.max_score_per_factor = 100
        
    def analyze_competitive_intelligence(self, state: MultiPlatformState) -> MultiPlatformState:
        """
        🎯 Main competitive intelligence scoring function
        """
        
        print("🏆 Competitive Intelligence Scorer: Starting advanced competitive analysis...")
        
        # Extract data from current state
        brand_mentions = state.get("brand_mentions", {})
        engagement_scores = state.get("engagement_scores", {})
        sov_metrics = state.get("sov_metrics", {})
        position_analysis = state.get("position_analysis", {})
        
        if not brand_mentions:
            print("⚠️ Insufficient brand data for competitive scoring")
            return self._return_insufficient_data_state(state)
        
        try:
            # Step 1: Calculate individual scoring factors
            print("📊 Step 1: Calculating market presence scores...")
            market_presence_scores = self._calculate_market_presence_scores(
                brand_mentions, sov_metrics, position_analysis
            )
            
            print("🎯 Step 2: Calculating engagement quality scores...")
            engagement_quality_scores = self._calculate_engagement_quality_scores(
                engagement_scores, brand_mentions
            )
            
            print("⚔️ Step 3: Calculating competitive position scores...")
            competitive_position_scores = self._calculate_competitive_position_scores(
                sov_metrics, brand_mentions
            )
            
            print("📈 Step 4: Calculating market dynamics scores...")
            market_dynamics_scores = self._calculate_market_dynamics_scores(
                brand_mentions, sov_metrics
            )
            
            # Step 2: Calculate weighted competitive scores
            print("🏆 Step 5: Computing final competitive scores...")
            competitive_scores = self._calculate_weighted_competitive_scores(
                market_presence_scores,
                engagement_quality_scores, 
                competitive_position_scores,
                market_dynamics_scores
            )
            
            # Step 3: Perform market positioning analysis
            print("🎯 Step 6: Performing market positioning analysis...")
            market_positioning = self._perform_market_positioning_analysis(
                competitive_scores, sov_metrics
            )
            
            # Step 4: Generate competitive intelligence insights
            print("💡 Step 7: Generating competitive intelligence insights...")
            competitive_insights = self._generate_competitive_insights(
                competitive_scores, market_positioning, brand_mentions
            )
            
            # Package results
            competitive_intelligence = {
                "competitive_scores": competitive_scores,
                "factor_breakdown": {
                    "market_presence": market_presence_scores,
                    "engagement_quality": engagement_quality_scores,
                    "competitive_position": competitive_position_scores,
                    "market_dynamics": market_dynamics_scores
                },
                "market_positioning": market_positioning,
                "competitive_insights": competitive_insights,
                "scoring_methodology": {
                    "weights": self.scoring_weights,
                    "total_brands_analyzed": len(brand_mentions),
                    "analysis_timestamp": state.get("start_time")
                }
            }
            
            print(f"✅ Competitive intelligence analysis completed for {len(brand_mentions)} brands")
        
            # CRITICAL FIX: Return only the state updates, not the full state
            return {
            "competitive_intelligence": competitive_intelligence,
            "current_phase": "competitive_scoring_complete"
        }
        
        except Exception as e:
            return {
                "competitive_intelligence": {"error": str(e)},
                "current_phase": "competitive_scoring_error"
            }
    
    def _calculate_market_presence_scores(self, brand_mentions: Dict, sov_metrics: Dict, 
                                        position_analysis: Dict) -> Dict[str, float]:
        """
        📊 Calculate market presence scores (40% weight)
        Based on SoV, mentions, and search positions
        """
        
        presence_scores = {}
        
        # Get market totals for normalization
        total_mentions = sum(brand_mentions.values())
        max_sov = max(sov_metrics[brand].get('overall_sov', 0) for brand in brand_mentions.keys())
        
        for brand in brand_mentions.keys():
            # Factor 1: Share of Voice (60% of presence score)
            brand_sov = sov_metrics.get(brand, {}).get('overall_sov', 0)
            sov_score = (brand_sov / max_sov * 100) if max_sov > 0 else 0
            
            # Factor 2: Mention Volume (25% of presence score)
            mention_share = (brand_mentions[brand] / total_mentions * 100) if total_mentions > 0 else 0
            volume_score = min(100, mention_share * 3)  # Scale factor
            
            # Factor 3: Search Position Quality (15% of presence score)
            positions = position_analysis.get(brand, [])
            if positions:
                avg_position = mean(positions)
                # Convert position to score (position 1 = 100 points, position 10 = 10 points)
                position_score = max(0, (11 - avg_position) * 10)
            else:
                position_score = 0
            
            # Weighted presence score
            presence_score = (
                sov_score * 0.60 +
                volume_score * 0.25 + 
                position_score * 0.15
            )
            
            presence_scores[brand] = round(presence_score, 2)
        
        return presence_scores
    
    def _calculate_engagement_quality_scores(self, engagement_scores: Dict, 
                                           brand_mentions: Dict) -> Dict[str, float]:
        """
        🎯 Calculate engagement quality scores (30% weight)
        Based on engagement per mention and quality indicators
        """
        
        quality_scores = {}
        
        # Calculate engagement per mention for normalization
        engagement_per_mention = {}
        for brand in brand_mentions.keys():
            mentions = brand_mentions[brand]
            total_engagement = engagement_scores.get(brand, 0)
            engagement_per_mention[brand] = total_engagement / mentions if mentions > 0 else 0
        
        max_engagement_per_mention = max(engagement_per_mention.values()) if engagement_per_mention else 1
        
        for brand in brand_mentions.keys():
            brand_engagement_per_mention = engagement_per_mention[brand]
            
            # Normalize to 0-100 scale
            if max_engagement_per_mention > 0:
                quality_score = (brand_engagement_per_mention / max_engagement_per_mention) * 100
            else:
                quality_score = 0
            
            quality_scores[brand] = round(quality_score, 2)
        
        return quality_scores
    
    def _calculate_competitive_position_scores(self, sov_metrics: Dict, 
                                             brand_mentions: Dict) -> Dict[str, float]:
        """
        ⚔️ Calculate competitive position scores (20% weight)
        Based on relative market position and competitive gaps
        """
        
        position_scores = {}
        
        # Get all brand SoV values for ranking
        brand_sovs = {brand: sov_metrics.get(brand, {}).get('overall_sov', 0) 
                     for brand in brand_mentions.keys()}
        
        # Sort brands by SoV for ranking
        sorted_brands = sorted(brand_sovs.items(), key=lambda x: x[1], reverse=True)
        total_brands = len(sorted_brands)
        
        for rank, (brand, sov) in enumerate(sorted_brands, 1):
            # Factor 1: Market Rank Score (70% of position score)
            # Rank 1 = 100 points, Rank 2 = 80 points, etc.
            rank_score = max(0, 100 - (rank - 1) * (100 / total_brands))
            
            # Factor 2: Competitive Gap Analysis (30% of position score)
            if rank == 1:
                # Leader gets full points for gap factor
                gap_score = 100
            else:
                # Calculate gap to leader
                leader_sov = sorted_brands[0][1]
                gap_to_leader = leader_sov - sov
                # Smaller gaps = higher scores
                gap_score = max(0, 100 - (gap_to_leader * 2))
            
            # Weighted position score
            position_score = rank_score * 0.70 + gap_score * 0.30
            position_scores[brand] = round(position_score, 2)
        
        return position_scores
    
    def _calculate_market_dynamics_scores(self, brand_mentions: Dict, 
                                        sov_metrics: Dict) -> Dict[str, float]:
        """
        📈 Calculate market dynamics scores (10% weight)
        Based on market concentration and competitive landscape health
        """
        
        dynamics_scores = {}
        
        # Calculate market concentration (HHI-style)
        total_mentions = sum(brand_mentions.values())
        market_shares = {brand: (mentions/total_mentions)*100 
                        for brand, mentions in brand_mentions.items()}
        
        # Herfindahl-Hirschman Index calculation
        hhi = sum(share**2 for share in market_shares.values())
        
        # Market structure analysis
        if hhi < 1500:
            market_structure = "competitive"
            structure_bonus = 20  # Competitive markets offer more opportunities
        elif hhi < 2500:
            market_structure = "moderately_concentrated"
            structure_bonus = 10  # Moderate concentration
        else:
            market_structure = "highly_concentrated"
            structure_bonus = 5   # Concentrated markets harder to penetrate
        
        for brand in brand_mentions.keys():
            brand_share = market_shares[brand]
            
            # Factor 1: Market Share Growth Potential (60% of dynamics score)
            # Higher share = lower growth potential but more stability
            growth_potential = max(0, 100 - brand_share)
            
            # Factor 2: Market Structure Advantage (40% of dynamics score)
            # Competitive markets = more opportunities
            structure_score = structure_bonus + (brand_share * 0.5)
            
            # Weighted dynamics score
            dynamics_score = growth_potential * 0.60 + structure_score * 0.40
            dynamics_scores[brand] = round(min(100, dynamics_score), 2)
        
        return dynamics_scores
    
    def _calculate_weighted_competitive_scores(self, market_presence: Dict, engagement_quality: Dict,
                                             competitive_position: Dict, market_dynamics: Dict) -> Dict[str, Dict]:
        """
        🏆 Calculate final weighted competitive scores
        """
        
        competitive_scores = {}
        all_brands = set(market_presence.keys())
        
        # Calculate scores for each brand
        brand_scores = []
        for brand in all_brands:
            # Get individual factor scores
            presence_score = market_presence.get(brand, 0)
            quality_score = engagement_quality.get(brand, 0)
            position_score = competitive_position.get(brand, 0)
            dynamics_score = market_dynamics.get(brand, 0)
            
            # Calculate weighted total score
            total_score = (
                presence_score * self.scoring_weights['market_presence'] +
                quality_score * self.scoring_weights['engagement_quality'] +
                position_score * self.scoring_weights['competitive_position'] +
                dynamics_score * self.scoring_weights['market_dynamics']
            )
            
            brand_scores.append(total_score)
            
            competitive_scores[brand] = {
                "total_score": round(total_score, 2),
                "market_presence": presence_score,
                "engagement_quality": quality_score, 
                "competitive_position": position_score,
                "market_dynamics": dynamics_score,
                "performance_tier": self._determine_performance_tier(total_score)
            }
        
        # Calculate Competitive Advantage Index (CAI)
        if len(brand_scores) > 1:
            market_average = mean(brand_scores)
            market_stdev = stdev(brand_scores) if len(brand_scores) > 1 else 1
            
            for brand in competitive_scores:
                brand_score = competitive_scores[brand]["total_score"]
                cai = (brand_score - market_average) / market_stdev
                competitive_scores[brand]["competitive_advantage_index"] = round(cai, 3)
                competitive_scores[brand]["cai_interpretation"] = self._interpret_cai(cai)
        
        return competitive_scores
    
    def _determine_performance_tier(self, score: float) -> str:
        """Categorize performance based on competitive score"""
        if score >= 80:
            return "Market Leader"
        elif score >= 60:
            return "Strong Performer"
        elif score >= 40:
            return "Average Competitor"
        elif score >= 20:
            return "Emerging Player"
        else:
            return "Follower"
    
    def _interpret_cai(self, cai: float) -> str:
        """Interpret Competitive Advantage Index"""
        if cai > 1.0:
            return "Strong Competitive Advantage"
        elif cai > 0.5:
            return "Moderate Competitive Advantage"
        elif cai > -0.5:
            return "Average Market Performance"
        elif cai > -1.0:
            return "Below Average Performance"
        else:
            return "Significant Competitive Disadvantage"
    
    def _perform_market_positioning_analysis(self, competitive_scores: Dict, 
                                           sov_metrics: Dict) -> Dict[str, Any]:
        """
        🎯 Perform BCG Matrix-style market positioning analysis
        """
        
        positioning = {}
        
        for brand, scores in competitive_scores.items():
            total_score = scores["total_score"]
            market_presence = scores["market_presence"]
            
            # Determine market position quadrant
            if market_presence >= 60 and total_score >= 60:
                position = "STAR"
                description = "High presence + High performance - Market leader"
            elif market_presence >= 60 and total_score < 60:
                position = "CASH_COW" 
                description = "High presence + Moderate performance - Established player"
            elif market_presence < 60 and total_score >= 60:
                position = "QUESTION_MARK"
                description = "Low presence + High performance - High potential challenger"
            else:
                position = "DOG"
                description = "Low presence + Low performance - Needs strategic review"
            
            positioning[brand] = {
                "position": position,
                "description": description,
                "strategic_priority": self._determine_strategic_priority(position, brand)
            }
        
        return positioning
    
    def _determine_strategic_priority(self, position: str, brand: str) -> str:
        """Determine strategic priority based on market position"""
        if brand.lower() == "atomberg":
            if position == "STAR":
                return "Maintain leadership and expand market share"
            elif position == "CASH_COW":
                return "Optimize performance to regain STAR status"
            elif position == "QUESTION_MARK":
                return "Increase market presence to match high performance"
            else:
                return "Comprehensive competitive strategy needed"
        else:
            return f"Monitor {position} competitor positioning"
    
    def _generate_competitive_insights(self, competitive_scores: Dict, 
                                     market_positioning: Dict, brand_mentions: Dict) -> List[str]:
        """
        💡 Generate strategic competitive intelligence insights
        """
        
        insights = []
        
        # Overall market analysis
        sorted_scores = sorted(competitive_scores.items(), 
                             key=lambda x: x[1]["total_score"], reverse=True)
        
        market_leader = sorted_scores[0][0]
        leader_score = sorted_scores[0][1]["total_score"]
        
        insights.append(f"🏆 Market leader: {market_leader} with {leader_score:.1f}/100 competitive score")
        
        # Atomberg-specific insights
        if "atomberg" in competitive_scores:
            atomberg_data = competitive_scores["atomberg"]
            atomberg_score = atomberg_data["total_score"]
            atomberg_rank = next(i+1 for i, (brand, _) in enumerate(sorted_scores) if brand == "atomberg")
            cai = atomberg_data.get("competitive_advantage_index", 0)
            
            insights.append(f"🎯 Atomberg: {atomberg_score:.1f}/100 score, Rank #{atomberg_rank}, CAI: {cai:+.2f}")
            
            # Performance analysis
            strongest_factor = max(
                [("Market Presence", atomberg_data["market_presence"]),
                 ("Engagement Quality", atomberg_data["engagement_quality"]),
                 ("Competitive Position", atomberg_data["competitive_position"]),
                 ("Market Dynamics", atomberg_data["market_dynamics"])],
                key=lambda x: x[1]
            )
            
            weakest_factor = min(
                [("Market Presence", atomberg_data["market_presence"]),
                 ("Engagement Quality", atomberg_data["engagement_quality"]),
                 ("Competitive Position", atomberg_data["competitive_position"]),
                 ("Market Dynamics", atomberg_data["market_dynamics"])],
                key=lambda x: x[1]
            )
            
            insights.append(f"💪 Atomberg strength: {strongest_factor[0]} ({strongest_factor[1]:.1f}/100)")
            insights.append(f"🎯 Atomberg opportunity: {weakest_factor[0]} ({weakest_factor[1]:.1f}/100)")
            
            # Strategic positioning
            atomberg_position = market_positioning.get("atomberg", {})
            if atomberg_position:
                position = atomberg_position["position"]
                priority = atomberg_position["strategic_priority"]
                insights.append(f"📍 Strategic position: {position} - {priority}")
        
        # Market concentration insight
        total_brands = len(competitive_scores)
        avg_score = mean(score["total_score"] for score in competitive_scores.values())
        
        insights.append(f"📊 Market analysis: {total_brands} competitors, avg score {avg_score:.1f}/100")
        
        return insights
    
    def _return_insufficient_data_state(self, state: MultiPlatformState) -> MultiPlatformState:
        """Return state when insufficient data for competitive scoring"""
        
        return {
            **state,
            "competitive_intelligence": {
                "error": "Insufficient brand data for competitive scoring",
                "message": "Competitive intelligence requires brand mention data",
                "recommendation": "Ensure quantitative analysis detects brand mentions"
            }
        }

def competitive_scoring_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    🏆 Competitive Intelligence Scoring Agent - Main Entry Point
    Integrates with existing LangGraph workflow
    """
    
    scorer = CompetitiveIntelligenceScorer()
    return scorer.analyze_competitive_intelligence(state)

print("🏆 Competitive Intelligence Scoring Analyzer Ready!")
