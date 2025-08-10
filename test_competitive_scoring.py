"""
🧪 Test Competitive Intelligence Scoring
"""

from src.core.detective_coordinator import run_multiplatform_investigation

def test_competitive_scoring():
    """Test the competitive intelligence scoring functionality"""
    
    print("🧪 Testing Competitive Intelligence Scoring...")
    print("="*60)
    
    try:
        # Test with Google (works with your current data)
        print("📋 Test: Single-platform investigation with competitive scoring")
        results = run_multiplatform_investigation("smart fan", ["google"])
        
        # Debug the results structure
        print(f"🔧 DEBUG: Final results keys: {list(results.keys())}")
        
        # Verify competitive intelligence was generated
        if "competitive_intelligence" not in results:
            print("❌ ERROR: competitive_intelligence not found in results")
            print(f"🔧 Available keys: {list(results.keys())}")
            return False
        
        competitive_intelligence = results["competitive_intelligence"]
        print(f"🔧 DEBUG: Competitive intelligence structure: {list(competitive_intelligence.keys())}")
        
        if competitive_intelligence.get("error"):
            print(f"❌ ERROR: Competitive intelligence failed: {competitive_intelligence['error']}")
            return False
        
        print("✅ Competitive intelligence analysis completed")
        
        # Check for key components
        if "competitive_scores" in competitive_intelligence:
            competitive_scores = competitive_intelligence["competitive_scores"]
            print(f"✅ Competitive scores generated for {len(competitive_scores)} brands")
            
            # Show Atomberg's score
            if "atomberg" in competitive_scores:
                atomberg_score = competitive_scores["atomberg"]["total_score"]
                tier = competitive_scores["atomberg"]["performance_tier"]
                print(f"✅ Atomberg competitive score: {atomberg_score:.1f}/100 ({tier})")
            else:
                print("⚠️ Atomberg not found in competitive scores")
                print(f"🔧 Available brands: {list(competitive_scores.keys())}")
        else:
            print("❌ ERROR: competitive_scores not found")
            return False
        
        if "market_positioning" in competitive_intelligence:
            print("✅ Market positioning analysis completed")
        
        if "competitive_insights" in competitive_intelligence:
            insights = competitive_intelligence["competitive_insights"]
            print(f"✅ Competitive insights generated: {len(insights)} insights")
            
            # Display sample insights
            if insights:
                print("\n💡 Sample Competitive Intelligence:")
                for insight in insights[:3]:
                    print(f"   • {insight}")
            else:
                print("⚠️ No competitive insights generated")
        
        print("\n🎉 Competitive intelligence scoring test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Competitive scoring test failed: {e}")
        import traceback
        print(f"🔧 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_competitive_scoring()
    if success:
        print("\n🚀 Your advanced competitive intelligence system is ready!")
    else:
        print("\n🔧 Please fix the competitive scoring setup before proceeding.")
