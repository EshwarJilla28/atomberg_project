"""
🎥 YouTube Intelligence Collector Agent
Specialized in gathering video content and engagement data
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from ..core.detective_state import MultiPlatformState, log_platform_progress
from ..config.youtube_config import (
    get_youtube_api_key, YOUTUBE_CONFIG, VIDEO_ENGAGEMENT_FACTORS, COMMENT_ANALYSIS
)
from config import get_search_queries

class YouTubeIntelligenceCollector:
    """
    🎥 YouTube Data Collection and Analysis Engine
    """
    
    def __init__(self):
        self.api_key = get_youtube_api_key()
        self.youtube = build(
            YOUTUBE_CONFIG["api_service_name"],
            YOUTUBE_CONFIG["api_version"],
            developerKey=self.api_key
        )
        self.requests_made = 0
        self.daily_quota_used = 0
        
    def collect_youtube_intelligence(self, state: MultiPlatformState) -> MultiPlatformState:
        """
        🕵️ Main YouTube Intelligence Collection Function
        """
        
        print("🎥 YouTube Intelligence Collector: Starting video analysis...")
        
        search_query = state["search_query"]
        youtube_config = state["platform_configs"].get("youtube", {})
        
        state = log_platform_progress(state, "youtube", f"Starting intelligence collection for: '{search_query}'")
        
        try:
            start_time = time.time()
            
            # Generate YouTube-specific search queries
            search_queries = self.generate_youtube_queries(search_query)
            print(f"🔍 YouTube search strategy: {len(search_queries)} specialized queries")
            
            all_videos = []
            all_comments = []
            channel_data = {}
            
            # Collect videos for each query
            for i, query in enumerate(search_queries):
                print(f"🎬 Executing YouTube search {i+1}/{len(search_queries)}: '{query}'")
                
                # Search for videos
                videos = self.search_videos(query, max_results=youtube_config.get("target_videos", 25))
                
                if videos:
                    print(f"   📺 Found {len(videos)} videos")
                    
                    # Get detailed video information
                    detailed_videos = self.get_video_details(videos)
                    
                    # Collect comments for each video
                    video_comments = self.collect_video_comments(
                        detailed_videos, 
                        max_per_video=youtube_config.get("target_comments_per_video", 20)
                    )
                    
                    # Analyze channels
                    video_channels = self.analyze_video_channels(detailed_videos)
                    
                    all_videos.extend(detailed_videos)
                    all_comments.extend(video_comments)
                    channel_data.update(video_channels)
                    
                    print(f"   ✅ Collected {len(detailed_videos)} videos, {len(video_comments)} comments")
                
                # Respectful delay between searches
                if i < len(search_queries) - 1:
                    delay = random.uniform(2, 4)
                    print(f"   ⏸️  YouTube API pause: {delay:.1f}s")
                    time.sleep(delay)
            
            end_time = time.time()
            
            # Compile YouTube metadata
            youtube_metadata = {
                "queries_executed": search_queries,
                "videos_collected": len(all_videos),
                "comments_collected": len(all_comments),
                "channels_analyzed": len(channel_data),
                "collection_time_seconds": round(end_time - start_time, 2),
                "api_requests_made": self.requests_made,
                "quota_used": self.daily_quota_used
            }
            
            print(f"🏁 YouTube collection completed in {youtube_metadata['collection_time_seconds']}s")
            print(f"📊 Total YouTube data: {len(all_videos)} videos, {len(all_comments)} comments")
            
            # Update state with YouTube results
            state = log_platform_progress(
                state, 
                "youtube", 
                f"Collection completed: {len(all_videos)} videos, {len(all_comments)} comments"
            )
            
            return {
                **state,
                "youtube_results": all_videos + all_comments,  # Combined for unified processing
                "youtube_metadata": youtube_metadata,
                "youtube_channels": channel_data,
                "current_phase": "youtube_collection_complete"
            }
            
        except Exception as e:
            error_msg = f"YouTube collection failed: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Return state with error but continue processing
            return {
                **state,
                "youtube_results": [],
                "youtube_metadata": {"error": error_msg, "fallback_used": True},
                "errors_log": state["errors_log"] + [error_msg]
            }
    
    def generate_youtube_queries(self, base_query: str) -> List[str]:
        """
        🎯 Generate YouTube-optimized search queries
        """
        
        # Start with base queries
        queries = get_search_queries(base_query)
        
        # Add YouTube-specific variations
        youtube_specific = [
            f"{base_query} review 2024",
            f"{base_query} comparison test",
            f"{base_query} installation guide",
            f"best {base_query} India"
        ]
        
        # Combine and deduplicate
        all_queries = list(set(queries + youtube_specific))
        
        return all_queries[:3]  # Limit to 3 for API quota management
    
    def search_videos(self, query: str, max_results: int = 25) -> List[Dict]:
        """
        🔍 Search for videos using YouTube Data API
        """
        
        try:
            request = self.youtube.search().list(
                part="id,snippet",
                q=query,
                type="video",
                maxResults=min(max_results, 50),  # API limit is 50
                order=YOUTUBE_CONFIG["search_order"],
                publishedAfter=(datetime.now() - timedelta(days=365)).isoformat() + 'Z'  # Last year only
            )
            
            response = request.execute()
            self.requests_made += 1
            self.daily_quota_used += 100  # Each search costs 100 quota units
            
            videos = []
            for item in response.get('items', []):
                video = {
                    "type": "video",
                    "video_id": item['id']['videoId'],
                    "title": item['snippet']['title'],
                    "description": item['snippet']['description'],
                    "channel_id": item['snippet']['channelId'],
                    "channel_title": item['snippet']['channelTitle'],
                    "published_at": item['snippet']['publishedAt'],
                    "thumbnail": item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                    "search_query": query
                }
                videos.append(video)
            
            return videos
            
        except HttpError as e:
            print(f"   ❌ YouTube search failed for '{query}': {e}")
            return []
    
    def get_video_details(self, videos: List[Dict]) -> List[Dict]:
        """
        📊 Get detailed engagement metrics for videos
        """
        
        if not videos:
            return []
        
        video_ids = [v["video_id"] for v in videos]
        
        try:
            # Get statistics for all videos in batch
            request = self.youtube.videos().list(
                part="statistics,contentDetails",
                id=','.join(video_ids)
            )
            
            response = request.execute()
            self.requests_made += 1
            self.daily_quota_used += 1  # Videos.list costs 1 quota unit
            
            # Create lookup dictionary
            stats_lookup = {}
            for item in response.get('items', []):
                video_id = item['id']
                stats = item['statistics']
                content_details = item['contentDetails']
                
                stats_lookup[video_id] = {
                    "view_count": int(stats.get('viewCount', 0)),
                    "like_count": int(stats.get('likeCount', 0)),
                    "comment_count": int(stats.get('commentCount', 0)),
                    "duration": content_details.get('duration', ''),
                    "engagement_score": self.calculate_video_engagement_score(stats)
                }
            
            # Merge with original video data
            enhanced_videos = []
            for video in videos:
                video_id = video["video_id"]
                if video_id in stats_lookup:
                    enhanced_video = {**video, **stats_lookup[video_id]}
                    enhanced_videos.append(enhanced_video)
            
            return enhanced_videos
            
        except HttpError as e:
            print(f"   ❌ Failed to get video details: {e}")
            return videos  # Return original videos without stats
    
    def calculate_video_engagement_score(self, stats: Dict) -> float:
        """
        📈 Calculate engagement score based on video metrics
        """
        
        view_count = int(stats.get('viewCount', 0))
        like_count = int(stats.get('likeCount', 0))
        comment_count = int(stats.get('commentCount', 0))
        
        if view_count == 0:
            return 0.0
        
        # Normalize metrics
        like_rate = like_count / view_count if view_count > 0 else 0
        comment_rate = comment_count / view_count if view_count > 0 else 0
        
        # Calculate weighted engagement score
        engagement_score = (
            (view_count ** 0.5) * VIDEO_ENGAGEMENT_FACTORS["view_count_weight"] +
            (like_count * 10) * VIDEO_ENGAGEMENT_FACTORS["like_count_weight"] +
            (comment_count * 50) * VIDEO_ENGAGEMENT_FACTORS["comment_count_weight"]
        )
        
        return round(engagement_score, 2)
    
    def collect_video_comments(self, videos: List[Dict], max_per_video: int = 20) -> List[Dict]:
        """
        💬 Collect comments from videos for brand mention analysis
        """
        
        all_comments = []
        
        for video in videos[:10]:  # Limit to first 10 videos to manage quota
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video["video_id"],
                    maxResults=max_per_video,
                    order="relevance"  # Get most relevant comments first
                )
                
                response = request.execute()
                self.requests_made += 1
                self.daily_quota_used += 1
                
                for item in response.get('items', []):
                    comment_snippet = item['snippet']['topLevelComment']['snippet']
                    
                    comment = {
                        "type": "comment",
                        "comment_id": item['snippet']['topLevelComment']['id'],
                        "video_id": video["video_id"],
                        "video_title": video["title"],
                        "text": comment_snippet['textDisplay'],
                        "like_count": comment_snippet.get('likeCount', 0),
                        "published_at": comment_snippet['publishedAt'],
                        "author": comment_snippet['authorDisplayName'],
                        "search_query": video.get("search_query", "")
                    }
                    
                    # Filter out spam and very short comments
                    if self.is_valid_comment(comment):
                        all_comments.append(comment)
                
                # Small delay between comment requests
                time.sleep(0.5)
                
            except HttpError as e:
                # Comments might be disabled for some videos
                print(f"   ⚠️ Could not get comments for video {video['video_id']}: {e}")
                continue
        
        return all_comments
    
    def is_valid_comment(self, comment: Dict) -> bool:
        """Filter out spam and low-quality comments"""
        
        text = comment["text"].lower()
        
        # Skip very short or very long comments
        if len(text) < COMMENT_ANALYSIS["min_comment_length"]:
            return False
        if len(text) > COMMENT_ANALYSIS["max_comment_length"]:
            return False
        
        # Skip obvious spam
        for spam_indicator in COMMENT_ANALYSIS["skip_spam_indicators"]:
            if spam_indicator in text:
                return False
        
        return True
    
    def analyze_video_channels(self, videos: List[Dict]) -> Dict[str, Dict]:
        """
        📺 Analyze channels for influencer identification
        """
        
        channel_ids = list(set([v["channel_id"] for v in videos]))
        channel_data = {}
        
        try:
            # Get channel statistics
            request = self.youtube.channels().list(
                part="statistics,snippet",
                id=','.join(channel_ids[:50])  # API limit
            )
            
            response = request.execute()
            self.requests_made += 1
            self.daily_quota_used += 1
            
            for item in response.get('items', []):
                channel_id = item['id']
                stats = item['statistics']
                snippet = item['snippet']
                
                channel_data[channel_id] = {
                    "channel_title": snippet['title'],
                    "subscriber_count": int(stats.get('subscriberCount', 0)),
                    "video_count": int(stats.get('videoCount', 0)),
                    "view_count": int(stats.get('viewCount', 0)),
                    "description": snippet.get('description', ''),
                    "influence_score": self.calculate_influence_score(stats)
                }
        
        except HttpError as e:
            print(f"   ⚠️ Could not get channel data: {e}")
        
        return channel_data
    
    def calculate_influence_score(self, stats: Dict) -> float:
        """Calculate channel influence based on metrics"""
        
        subscriber_count = int(stats.get('subscriberCount', 0))
        video_count = int(stats.get('videoCount', 0))
        total_views = int(stats.get('viewCount', 0))
        
        if subscriber_count == 0:
            return 0.0
        
        # Average views per video
        avg_views = total_views / video_count if video_count > 0 else 0
        
        # Engagement rate approximation
        engagement_rate = avg_views / subscriber_count if subscriber_count > 0 else 0
        
        # Influence score (combines reach and engagement)
        influence_score = (subscriber_count ** 0.3) * (engagement_rate * 1000)
        
        return round(influence_score, 2)

def youtube_intelligence_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    🎥 YouTube Intelligence Agent - Main Entry Point
    Integrates with existing LangGraph workflow
    """
    
    if "youtube" not in state.get("enabled_platforms", []):
        print("⏭️ YouTube collection skipped - not enabled")
        return state
    
    collector = YouTubeIntelligenceCollector()
    return collector.collect_youtube_intelligence(state)

print("🎥 YouTube Intelligence Collector Ready!")
