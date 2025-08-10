"""
🧪 Test YouTube API Connection
"""

from googleapiclient.discovery import build
from src.config.youtube_config import get_youtube_api_key, YOUTUBE_CONFIG

def test_youtube_connection():
    """Test that YouTube API is working"""
    
    try:
        # Get API key
        api_key = get_youtube_api_key()
        print(f"✅ API key loaded: {api_key[:10]}...")
        
        # Build YouTube service
        youtube = build(
            YOUTUBE_CONFIG["api_service_name"],
            YOUTUBE_CONFIG["api_version"], 
            developerKey=api_key
        )
        print("✅ YouTube service built successfully")
        
        # Test search
        request = youtube.search().list(
            part="snippet",
            q="smart fan",
            maxResults=5,
            type="video"
        )
        
        response = request.execute()
        print(f"✅ Search test successful: Found {len(response['items'])} videos")
        
        # Display first result
        if response['items']:
            first_video = response['items'][0]
            print(f"📺 Sample video: {first_video['snippet']['title']}")
            print(f"🔗 Video ID: {first_video['id']['videoId']}")
        
        return True
        
    except Exception as e:
        print(f"❌ YouTube API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_youtube_connection()
    if success:
        print("\n🎉 YouTube API is ready for integration!")
    else:
        print("\n🔧 Please fix the API setup before proceeding")
