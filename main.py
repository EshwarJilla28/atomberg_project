#!/usr/bin/env python3
"""
🚀 Enhanced Atomberg SoV Detective Agency - Multi-Platform Intelligence
Backward compatible with existing Google-only functionality
"""

import sys
import argparse
from src.core.detective_coordinator import run_multiplatform_investigation

def parse_arguments():
    """
    📋 Parse command line arguments for platform selection
    """
    
    parser = argparse.ArgumentParser(
        description="Atomberg Share of Voice Detective Agency - Multi-Platform Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Google only (original behavior)
  python main.py --platforms google                # Google only (explicit)
  python main.py --platforms google,youtube        # Google + YouTube
  python main.py "BLDC fan" --platforms google,youtube  # Custom query + multi-platform
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        default="smart fan",
        help="Search query to investigate (default: 'smart fan')"
    )
    
    parser.add_argument(
        "--platforms",
        type=str,
        default="google",
        help="Comma-separated list of platforms: google,youtube (default: google)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed logging output"
    )
    
    parser.add_argument(
        "--focus_brand",
        type=str,
        default="atomberg",
        help="Brand to focus on during investigation (default: 'atomberg')"
    )
    
    return parser.parse_args()

def main():
    """
    🎯 Enhanced Main Application Entry Point with Multi-Platform Support
    """
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Process platforms
    platforms = [p.strip() for p in args.platforms.split(",")]
    
    # Display welcome message
    print("🏢 Welcome to Atomberg SoV Detective Agency!")
    print("📊 Multi-platform competitive intelligence system")
    if len(platforms) == 1:
        print(f"⚡ Single-platform analysis: {platforms[0].upper()}")
    else:
        print(f"🌐 Multi-platform analysis: {', '.join(p.upper() for p in platforms)}")
    print()
    
    print(f"🎯 Investigation Target: '{args.query}'")
    print(f"📱 Enabled Platforms: {', '.join(platforms)}")
    print(f"🏷️ Focus Brand: '{args.focus_brand}'")
    
    # Validate platforms
    supported_platforms = ["google", "youtube"]
    invalid_platforms = [p for p in platforms if p not in supported_platforms]
    
    if invalid_platforms:
        print(f"❌ Unsupported platforms: {', '.join(invalid_platforms)}")
        print(f"✅ Supported platforms: {', '.join(supported_platforms)}")
        return None
    
    try:
        # Run the multi-platform investigation
        results = run_multiplatform_investigation(args.query, platforms, focus_brand=args.focus_brand)
        
        print(f"\n🎊 Multi-platform investigation completed successfully!")
        print(f"📊 Results saved to investigation: {results['investigation_id']}")
        
        # Optional: Save results to file
        if args.verbose:
            save_investigation_results(results)
        
        return results
        
    except Exception as e:
        print(f"\n❌ Investigation failed: {e}")
        print(f"🔧 Please check your setup and platform configurations")
        
        if "youtube" in platforms and "API key" in str(e):
            print(f"💡 Hint: Make sure you've set up your YouTube API key in src/config/youtube_config.py")
        
        return None

def save_investigation_results(results):
    """
    💾 Save detailed investigation results to file
    """
    
    import json
    from datetime import datetime
    
    filename = f"investigation_{results['investigation_id']}.json"
    
    # Create a serializable version of results
    serializable_results = {
        "investigation_id": results["investigation_id"],
        "search_query": results["search_query"],
        "platforms": results["enabled_platforms"],
        "timestamp": results["start_time"],
        "total_results": len(results.get("raw_search_results", [])),
        "brand_mentions": results.get("brand_mentions", {}),
        "sov_metrics": results.get("sov_metrics", {}),
        "insights": results.get("quantitative_insights", []),
        "recommendations": results.get("action_recommendations", []),
        "cross_platform_insights": results.get("cross_platform_insights", [])
    }
    
    if "platform_breakdown" in results:
        serializable_results["platform_breakdown"] = results["platform_breakdown"]
    
    try:
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        print(f"💾 Detailed results saved to: {filename}")
    except Exception as e:
        print(f"⚠️ Could not save results file: {e}")

if __name__ == "__main__":
    main()
