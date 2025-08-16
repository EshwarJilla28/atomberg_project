"""
📊 Quantitative Analysis Agent
Pure math and pattern matching - no NLP required!
"""

import re
from typing import Dict, List, Any, Tuple
from collections import defaultdict

from ..core.detective_state import MultiPlatformState, log_platform_progress
from config import BRAND_PATTERNS, ENGAGEMENT_FACTORS, PRODUCT_KEYWORDS, get_engagement_score

def quantitative_analysis_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    🔬 Quantitative Analyst Agent
    Analyzes collected data using pure mathematics and pattern matching
    """
    
    print("📊 Quantitative Analyst: Processing evidence...")
    
    raw_results = state.get("raw_search_results", [])
    
    if not raw_results:
        print("⚠️ No data to analyze")
        return log_platform_progress(state,"google", "⚠️ Analysis skipped - no data available")
    
    print(f"🔬 Analyzing {len(raw_results)} pieces of evidence...")
    
    # Initialize analysis containers
    brand_mentions_raw = defaultdict(int)
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
        detected_brands_capped, detected_brands_raw = detect_brands_in_content(content)
        
        # === ENGAGEMENT CALCULATION (Pure Math) ===
        engagement = get_engagement_score(content, url, title)
        
        # === KEYWORD FREQUENCY ANALYSIS ===
        keywords = analyze_keyword_frequency(content)
        
        # Aggregate raw mention results
        for brand, count in detected_brands_raw.items():
            brand_mentions_raw[brand] += count
        
        # Aggregate capped mention results and engagement scores
        for brand, count in detected_brands_capped.items():
            brand_mentions[brand] += count
        
        if detected_brands_capped:
            for brand in detected_brands_capped:
                engagement_scores[brand] += engagement / len(detected_brands_capped)
                position_analysis[brand].append(position)
        
        for keyword, freq in keywords.items():
            keyword_frequency[keyword] += freq
        
        # Store processed result
        processed_content.append({
            "id": result.get("id"),
            "title": title,
            "url": url,
            "position": position,
            "brands_detected_raw": detected_brands_raw,
            "brands_detected": detected_brands_capped,
            "engagement_score": engagement,
            "keywords_found": keywords,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        })
    
    # Convert defaultdicts to regular dicts
    brand_mentions_raw = dict(brand_mentions_raw)
    brand_mentions = dict(brand_mentions)
    engagement_scores = dict(engagement_scores)
    keyword_frequency = dict(keyword_frequency)
    position_analysis = dict(position_analysis)
    
    print(f"📊 Analysis Results:")
    print(f"   • Brands detected (capped): {list(brand_mentions.keys())}")
    print(f"   • Total brand mentions (raw): {sum(brand_mentions_raw.values())}")
    print(f"   • Top keywords: {sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    # Update state with analysis results
    state = log_platform_progress(state,"google", f"📊 Quantitative analysis completed: {len(brand_mentions)} brands, {sum(brand_mentions_raw.values())} total raw mentions")
    
    return {
        **state,
        "brand_mentions_raw": brand_mentions_raw,
        "brand_mentions": brand_mentions,
        "engagement_scores": engagement_scores,
        "keyword_frequency": keyword_frequency,
        "position_analysis": position_analysis,
        "processed_content": processed_content,
        "current_phase": "quantitative_analysis_complete"
    }

def detect_brands_in_content(content: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    🎯 Detect brand mentions using regex patterns
    Returns two dicts:
    - capped mentions (max 1 per brand per content)
    - raw mention counts
    """
    content_lower = content.lower()
    brand_counts_raw = {}
    brand_counts_capped = {}
    
    for brand, patterns in BRAND_PATTERNS.items():
        total_mentions = 0
        for pattern in patterns:
            matches = re.findall(pattern, content_lower)
            total_mentions += len(matches)
        
        if total_mentions > 0:
            brand_counts_raw[brand] = total_mentions
            brand_counts_capped[brand] = 1
    
    return brand_counts_capped, brand_counts_raw

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
