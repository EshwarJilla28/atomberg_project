"""
📊 Quantitative Analysis Agent
Pure math and pattern matching - no NLP required!
"""

import re
from typing import Dict, List, Any
from collections import defaultdict

from ..core.detective_state import QuantitativeState, log_progress
from config import BRAND_PATTERNS, ENGAGEMENT_FACTORS, PRODUCT_KEYWORDS, get_engagement_score

def quantitative_analysis_agent(state: QuantitativeState) -> QuantitativeState:
    """
    🔬 Quantitative Analyst Agent
    Analyzes collected data using pure mathematics and pattern matching
    """
    
    print("📊 Quantitative Analyst: Processing evidence...")
    
    raw_results = state.get("raw_search_results", [])
    
    if not raw_results:
        print("⚠️ No data to analyze")
        return log_progress(state, "⚠️ Analysis skipped - no data available")
    
    print(f"🔬 Analyzing {len(raw_results)} pieces of evidence...")
    
    # Initialize analysis containers
    brand_mentions = defaultdict(int)
    engagement_scores = defaultdict(float)
    keyword_frequency = defaultdict(int)
    position_analysis = defaultdict(list)
    processed_content = []
    
    # Process each search result
    for result in raw_results:
        content = f"{result.get('title', '')} {result.get('snippet', '')}"
        title = result.get('title', '')
        url = result.get('url', '')
        position = result.get('position', 0)
        
        # === BRAND DETECTION (Pattern Matching) ===
        detected_brands = detect_brands_in_content(content)
        
        # === ENGAGEMENT CALCULATION (Pure Math) ===
        engagement = get_engagement_score(content, url, title)
        
        # === KEYWORD FREQUENCY ANALYSIS ===
        keywords = analyze_keyword_frequency(content)
        
        # Aggregate results
        for brand, count in detected_brands.items():
            brand_mentions[brand] += count
            engagement_scores[brand] += engagement / len(detected_brands) if detected_brands else 0
            position_analysis[brand].append(position)
        
        for keyword, freq in keywords.items():
            keyword_frequency[keyword] += freq
        
        # Store processed result
        processed_content.append({
            "id": result.get("id"),
            "title": title,
            "url": url,
            "position": position,
            "brands_detected": detected_brands,
            "engagement_score": engagement,
            "keywords_found": keywords,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        })
    
    # Convert defaultdicts to regular dicts
    brand_mentions = dict(brand_mentions)
    engagement_scores = dict(engagement_scores)
    keyword_frequency = dict(keyword_frequency)
    position_analysis = dict(position_analysis)
    
    print(f"📊 Analysis Results:")
    print(f"   • Brands detected: {list(brand_mentions.keys())}")
    print(f"   • Total brand mentions: {sum(brand_mentions.values())}")
    print(f"   • Top keywords: {sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    # Update state with analysis results
    state = log_progress(state, f"📊 Quantitative analysis completed: {len(brand_mentions)} brands, {sum(brand_mentions.values())} total mentions")
    
    return {
        **state,
        "brand_mentions": brand_mentions,
        "engagement_scores": engagement_scores,
        "keyword_frequency": keyword_frequency,
        "position_analysis": position_analysis,
        "processed_content": processed_content,
        "current_phase": "quantitative_analysis_complete"
    }

def detect_brands_in_content(content: str) -> Dict[str, int]:
    """
    🎯 Detect brand mentions using regex patterns
    """
    content_lower = content.lower()
    brand_counts = {}
    
    for brand, patterns in BRAND_PATTERNS.items():
        total_mentions = 0
        for pattern in patterns:
            matches = re.findall(pattern, content_lower)
            total_mentions += len(matches)
        
        if total_mentions > 0:
            brand_counts[brand] = total_mentions
    
    return brand_counts

def analyze_keyword_frequency(content: str) -> Dict[str, int]:
    """
    📈 Analyze product-related keyword frequency
    """
    content_lower = content.lower()
    keyword_counts = {}
    
    # Flatten all keyword categories
    all_keywords = []
    for category, keywords in PRODUCT_KEYWORDS.items():
        all_keywords.extend(keywords)
    
    for keyword in all_keywords:
        count = content_lower.count(keyword.lower())
        if count > 0:
            keyword_counts[keyword] = count
    
    return keyword_counts

print("📊 Quantitative Analysis Agent Ready!")
