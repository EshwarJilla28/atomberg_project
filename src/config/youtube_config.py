"""
🎥 YouTube Data API Configuration - .env File Support
Secure API key management using environment variables
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API Configuration
YOUTUBE_CONFIG = {
    "api_service_name": "youtube",
    "api_version": "v3",
    "max_results_per_request": 50,
    "target_videos_per_query": 25,
    "target_comments_per_video": 20,
    "search_order": "relevance",
    "search_types": ["video"],
    "requests_per_second": 2,
    "max_daily_requests": 10000,
}

# Video Engagement Scoring Factors
VIDEO_ENGAGEMENT_FACTORS = {
    "view_count_weight": 0.3,
    "like_count_weight": 0.25, 
    "comment_count_weight": 0.25,
    "subscriber_count_weight": 0.2,
    "video_age_decay": 0.1
}

# Comment Analysis Settings
COMMENT_ANALYSIS = {
    "max_comment_length": 500,
    "min_comment_length": 10,
    "skip_spam_indicators": ["http", "subscribe", "follow me"],
    "prioritize_recent": True
}

def get_youtube_api_key():
    """
    🔑 Get YouTube API key from .env file
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        raise ValueError(
            "❌ YouTube API key not found!\n\n"
            "Please create a .env file in your project root with:\n"
            "YOUTUBE_API_KEY=your_actual_api_key_here\n\n"
            "Make sure:\n"
            "1. The .env file is in the same directory as main.py\n"
            "2. No quotes around the API key\n"
            "3. No spaces around the = sign\n"
            "4. python-dotenv is installed: pip install python-dotenv"
        )
    
    if len(api_key.strip()) < 30:
        raise ValueError("❌ Invalid YouTube API key format - too short")
    
    return api_key.strip()

print("🎥 YouTube API Configuration with .env support ready!")
