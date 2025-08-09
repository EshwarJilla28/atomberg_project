#!/usr/bin/env python3
"""
🚀 Atomberg SoV Detective Agency - Main Application
Complete quantitative Share of Voice analysis system
"""

import sys
from src.core.detective_coordinator import run_complete_investigation

def main():
    """
    🎯 Main Application Entry Point
    """
    
    print("🏢 Welcome to Atomberg SoV Detective Agency!")
    print("📊 Quantitative competitive intelligence system")
    print("⚡ Fast, accurate, no-NLP analysis\n")
    
    # Get search query from command line or use default
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "smart fan"
    
    print(f"🎯 Investigation Target: '{query}'")
    
    try:
        # Run the complete investigation
        results = run_complete_investigation(query)
        
        print(f"\n🎊 Investigation completed successfully!")
        print(f"📊 Results saved to investigation: {results['investigation_id']}")
        
        # Save to database (optional)
        # save_to_database(results)
        
        return results
        
    except Exception as e:
        print(f"\n❌ Investigation failed: {e}")
        print(f"🔧 Please check your setup and configuration")
        return None

if __name__ == "__main__":
    main()
