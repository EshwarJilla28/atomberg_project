"""
⚙️ Atomberg SoV Detective Agency Configuration
Central settings for your quantitative analysis engine
"""

from typing import Dict, List
import os

# === BRAND DETECTION PATTERNS ===
BRAND_PATTERNS = {
    'atomberg': [
        r'\batomberg\b',
        r'\batom\s*berg\b',
        r'@atomberg'
    ],
    'havells': [
        r'\bhavells\b',
        r'@havells'
    ],
    'bajaj': [
        r'\bbajaj\b',
        r'@bajajelectricals',
        r'bajaj\s+electrical'
    ],
    'crompton': [
        r'\bcrompton\b',
        r'@cromptongreaves'
    ],
    'orient': [
        r'\borient\b',
        r'orient\s+electric',
        r'@orientelectric'
    ],
    'usha': [
        r'\busha\b',
        r'@ushainternational'
    ]
}

# === SEARCH CONFIGURATION ===
SEARCH_CONFIG = {
    'target_results_per_query': 17,  # ~50 total across 3 queries
    'search_delay_range': (2, 4),   # Random delay between searches
    'max_retries': 3,
    'timeout_seconds': 30
}

# === SoV CALCULATION WEIGHTS ===
SOV_WEIGHTS = {
    'mention_weight': 0.6,        # How often brand appears
    'engagement_weight': 0.4,     # How much attention it gets
    'position_bonus': 0.1         # Higher ranking = bonus points
}

# === ENGAGEMENT SCORING FACTORS ===
ENGAGEMENT_FACTORS = {
    'content_length_multiplier': 0.1,     # Longer content = more comprehensive
    'title_mention_bonus': 50,            # Brand in title = high visibility  
    'authority_domain_bonus': 100,        # Trusted sites = more credible
    'review_keyword_bonus': 25,           # Review content = higher engagement
    'comparison_keyword_bonus': 75        # Comparison content = decision-making
}

# === KEYWORD CATEGORIES ===
PRODUCT_KEYWORDS = {
    'core_product': ['smart fan', 'ceiling fan', 'bldc fan', 'energy efficient fan'],
    'features': ['remote control', 'app control', 'wifi enabled', 'iot fan'],
    'technical': ['bldc motor', 'energy saving', 'power consumption'],
    'comparison': ['vs', 'versus', 'comparison', 'best', 'review']
}

# === AUTHORITY DOMAINS (Higher Credibility) ===
AUTHORITY_DOMAINS = [
    'amazon.com', 'flipkart.com', 'croma.com',
    'indiamart.com', 'justdial.com',
    'consumerreports.org', 'which.co.uk',
    'gadgets360.com', 'digit.in',
    '.edu', '.gov'
]

# === MONGODB CONFIGURATION ===
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'atomberg_sov',
    'collection': 'investigations'
}

# === SEARCH QUERY TEMPLATES ===
QUERY_TEMPLATES = [
    "{product} review",
    "{product} vs Havells vs Bajaj", 
    "{product} best brand India"
]

def get_search_queries(base_query: str) -> List[str]:
    """Generate search query variations"""
    return [template.format(product=base_query) for template in QUERY_TEMPLATES]

def get_engagement_score(content: str, url: str, title: str) -> float:
    """
    Calculate engagement score using quantitative factors only
    """
    score = 0.0
    content_lower = content.lower()
    
    # Content length factor
    score += len(content) * ENGAGEMENT_FACTORS['content_length_multiplier']
    
    # Title mention bonus
    if any(brand in title.lower() for brand in BRAND_PATTERNS.keys()):
        score += ENGAGEMENT_FACTORS['title_mention_bonus']
    
    # Authority domain bonus
    if any(domain in url for domain in AUTHORITY_DOMAINS):
        score += ENGAGEMENT_FACTORS['authority_domain_bonus']
    
    # Content type bonuses
    if any(keyword in content_lower for keyword in ['review', 'rating', 'star']):
        score += ENGAGEMENT_FACTORS['review_keyword_bonus']
    
    if any(keyword in content_lower for keyword in ['vs', 'versus', 'comparison', 'compare']):
        score += ENGAGEMENT_FACTORS['comparison_keyword_bonus']
    
    return score

# === CHROME DRIVER CONFIGURATION ===
CHROME_OPTIONS = [
    '--headless',
    '--no-sandbox', 
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
]

print("⚙️ Configuration loaded: Quantitative SoV Analysis Ready!")
