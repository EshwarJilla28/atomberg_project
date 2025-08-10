"""
🔍 Google Search Collector Agent
Specialized in gathering evidence from Google search results
Enhanced with human-like behavior to avoid bot detection
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from datetime import datetime
from typing import List, Dict

from ..core.detective_state import MultiPlatformState, log_platform_progress, log_error
from config import SEARCH_CONFIG, CHROME_OPTIONS, get_search_queries


def perform_human_like_search(driver, query):
    """
    🤖➡️🧑 Make the bot behave more like a human to avoid detection
    """
    try:
        print(f"   🧑 Performing human-like search for: '{query}'")
        
        # Go to Google homepage first (more natural behavior)
        driver.get("https://www.google.com")
        time.sleep(random.uniform(2, 4))
        
        # Find search box and wait for it to be interactive
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        
        # Clear any existing text
        search_box.clear()
        time.sleep(random.uniform(0.5, 1.0))
        
        # Type with human-like delays (simulates natural typing)
        print(f"   ⌨️  Typing query naturally...")
        for char in query:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # Human typing speed
        
        # Random pause before pressing Enter (humans think before pressing Enter)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Press Enter to search
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load (humans wait and observe)
        time.sleep(random.uniform(3, 5))
        
        # Try multiple CSS selectors (Google changes these frequently)
        result_selectors = [
            "div.g",           # Traditional selector
            "[data-ved]",      # Attribute-based selector  
            ".tF2Cxc",         # Modern selector
            ".g .yuRUbf",      # Nested selector
            "div[class*='g']", # Partial class match
            ".srg .g",         # Search results group
        ]
        
        results = []
        successful_selector = None
        
        # Try each selector until we find results
        for selector in result_selectors:
            try:
                results = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(results) > 0:
                    successful_selector = selector
                    print(f"   ✅ Found {len(results)} results with selector: '{selector}'")
                    break
            except Exception as e:
                continue
        
        if not results:
            # Last resort: try to find any clickable links that look like search results
            print(f"   🔄 Trying fallback: looking for any result links...")
            results = driver.find_elements(By.CSS_SELECTOR, "h3 a, .yuRUbf a, [data-ved] a")
            if results:
                print(f"   📍 Found {len(results)} fallback results")
        
        return results, successful_selector
        
    except Exception as e:
        print(f"   ❌ Human-like search failed: {str(e)[:100]}...")
        return [], None


def extract_result_data(container, index, query, selector_type):
    """
    📝 Extract title, URL, and snippet from a search result container
    Handles different Google result structures
    """
    try:
        result_data = {
            "title": "No title",
            "url": "",
            "snippet": ""
        }
        
        # Extract title (try multiple approaches)
        title_selectors = ["h3", ".LC20lb", ".DKV0Md", "[role='heading']"]
        for title_sel in title_selectors:
            try:
                title_elem = container.find_element(By.CSS_SELECTOR, title_sel)
                if title_elem and title_elem.text.strip():
                    result_data["title"] = title_elem.text.strip()
                    break
            except:
                continue
        
        # Extract URL (try multiple approaches)
        url_selectors = ["a", ".yuRUbf a", "h3 a", "[data-ved] a"]
        for url_sel in url_selectors:
            try:
                link_elem = container.find_element(By.CSS_SELECTOR, url_sel)
                href = link_elem.get_attribute("href")
                if href and href.startswith("http"):
                    result_data["url"] = href
                    break
            except:
                continue
        
        # Extract snippet (try multiple approaches)
        snippet_selectors = [
            ".VwiC3b", ".s3v9rd", ".st", "[data-sncf]", 
            "span", ".IsZvec", ".aCOpRe"
        ]
        snippet_texts = []
        
        for snippet_sel in snippet_selectors:
            try:
                snippet_elems = container.find_elements(By.CSS_SELECTOR, snippet_sel)
                for elem in snippet_elems[:3]:  # Limit to first 3 elements
                    text = elem.text.strip()
                    if text and len(text) > 10:  # Only meaningful text
                        snippet_texts.append(text)
            except:
                continue
        
        # Combine snippet texts
        if snippet_texts:
            result_data["snippet"] = " ".join(snippet_texts)[:500]  # Limit length
        
        # Validation: must have at least title or URL
        if not result_data["title"] and not result_data["url"]:
            return None
            
        return result_data
        
    except Exception as e:
        print(f"      ⚠️ Failed to extract data from result {index}: {str(e)[:50]}...")
        return None


def google_search_agent(state: MultiPlatformState) -> MultiPlatformState:
    """
    🕵️ Enhanced Google Search Detective
    Collects evidence from Google search results using human-like behavior
    """
    
    print("🔍 Google Search Agent: Starting evidence collection...")
    
    search_query = state["search_query"]
    target_results = state["target_results"]
    
    # Update state to show we're starting
    state = log_platform_progress(state,"google", f"🔍 Starting Google search for: '{search_query}'")
    
    # Generate search queries
    search_queries = get_search_queries(search_query)
    print(f"📋 Search strategy: {len(search_queries)} query variations")
    
    all_results = []
    search_metadata = {
        "queries_executed": [],
        "results_per_query": {},
        "total_time_seconds": 0,
        "errors_encountered": 0,
        "selectors_used": [],
        "human_like_enabled": True
    }
    
    # Enhanced Chrome options for better stealth
    chrome_options = Options()
    for option in CHROME_OPTIONS:
        chrome_options.add_argument(option)
    
    # Additional stealth options
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        start_time = time.time()
        
        # Initialize driver with webdriver-manager
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Additional stealth measures
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🤖 Chrome browser initialized (stealth mode)")
        
        # Random delay before starting (humans don't search immediately)
        time.sleep(random.uniform(1, 3))
        
        for i, query in enumerate(search_queries):
            print(f"🔎 Executing search {i+1}/{len(search_queries)}: '{query}'")
            
            try:
                # Use human-like search behavior
                result_containers, successful_selector = perform_human_like_search(driver, query)
                
                if successful_selector:
                    search_metadata["selectors_used"].append(successful_selector)
                
                print(f"   📊 Found {len(result_containers)} result containers")
                
                query_results = []
                
                # Extract information from each result
                for j, container in enumerate(result_containers[:SEARCH_CONFIG['target_results_per_query']]):
                    
                    # Extract result data
                    result_data = extract_result_data(container, j, query, successful_selector)
                    
                    if result_data:
                        # Create result object
                        result = {
                            "id": f"google_{i}_{j}",
                            "title": result_data["title"],
                            "url": result_data["url"],
                            "snippet": result_data["snippet"],
                            "search_query": query,
                            "position": j + 1,  # Search result position
                            "timestamp": datetime.now().isoformat(),
                            "source": "google",
                            "selector_used": successful_selector
                        }
                        
                        query_results.append(result)
                        
                        # Human-like pause between extractions
                        if j % 5 == 0 and j > 0:
                            time.sleep(random.uniform(0.5, 1.0))
                    else:
                        search_metadata["errors_encountered"] += 1
                
                all_results.extend(query_results)
                search_metadata["queries_executed"].append(query)
                search_metadata["results_per_query"][query] = len(query_results)
                
                print(f"   ✅ Collected {len(query_results)} results for this query")
                
                # Human-like delay between searches (very important!)
                if i < len(search_queries) - 1:  # Don't delay after last search
                    delay = random.uniform(8, 15)  # Longer delay between searches
                    print(f"   ⏸️  Pausing for {delay:.1f}s before next search...")
                    time.sleep(delay)
                
            except Exception as e:
                error_msg = f"Enhanced search failed for query '{query}': {str(e)}"
                print(f"   ❌ {error_msg}")
                state = log_error(state, error_msg, "Continuing with next query")
                search_metadata["errors_encountered"] += 1
                continue
        
        # Clean up
        driver.quit()
        end_time = time.time()
        search_metadata["total_time_seconds"] = round(end_time - start_time, 2)
        
        print(f"🏁 Enhanced search completed in {search_metadata['total_time_seconds']}s")
        print(f"📊 Total results collected: {len(all_results)}")
        
        # If we got very few results, it might still be bot detection
        if len(all_results) < 5:
            print("⚠️ Low result count - possible bot detection")
            print("🔄 Consider using sample data fallback for development")
        
        # Update state with results
        state = log_platform_progress(state,"google", f"🔍 Enhanced Google search completed: {len(all_results)} results from {len(search_queries)} queries")
        
        return {
            **state,
            "raw_search_results": all_results,
            "search_metadata": search_metadata,
            "current_phase": "data_collection_complete"
        }
        
    except Exception as e:
        error_msg = f"Critical enhanced search failure: {str(e)}"
        print(f"❌ {error_msg}")
        
        if 'driver' in locals():
            try:
                driver.quit()
            except:
                pass
        
        # Fallback to sample data
        print("🔄 Falling back to sample data...")
        sample_results = create_sample_data(search_queries if 'search_queries' in locals() else ["smart fan"])
        
        return {
            **state,
            "raw_search_results": sample_results,
            "search_metadata": {"sample_data": True, "fallback_reason": error_msg},
            "current_phase": "data_collection_complete"
        }


def create_sample_data(search_queries):
    """
    🧪 High-quality sample data for testing when Google scraping fails
    """
    return [
        {
            "id": "sample_1",
            "title": "Atomberg Efficio Plus 1200mm BLDC Motor Ceiling Fan Review",
            "url": "https://www.amazon.in/dp/B07PQZXYZ/",
            "snippet": "Atomberg Efficio Plus smart ceiling fan with BLDC motor offers 65% energy savings compared to traditional fans. Features remote control, app connectivity and 3-year warranty. Customer rating: 4.3/5 stars from 2,847 reviews.",
            "search_query": search_queries[0] if search_queries else "smart fan review",
            "position": 1,
            "timestamp": datetime.now().isoformat(),
            "source": "google_sample"
        },
        {
            "id": "sample_2",
            "title": "Best Smart Ceiling Fans in India 2024: Atomberg, Havells, Bajaj Comparison",
            "url": "https://www.gadgets360.com/home-appliances/features/best-smart-ceiling-fans",
            "snippet": "Comprehensive comparison of smart ceiling fans available in India. Atomberg leads in energy efficiency with BLDC technology. Havells offers premium designer options. Bajaj provides budget-friendly smart fans with basic app control.",
            "search_query": search_queries[1] if len(search_queries) > 1 else "smart fan comparison",
            "position": 2,
            "timestamp": datetime.now().isoformat(),
            "source": "google_sample"
        },
        {
            "id": "sample_3",
            "title": "Havells Stealth Air 1200mm Smart Ceiling Fan with Remote - Latest Model",
            "url": "https://www.flipkart.com/havells-stealth-air-smart-fan",
            "snippet": "Havells introduces new Stealth Air smart ceiling fan series with aerodynamic design and remote control. Features reversible motor and LED lighting. Available in multiple finishes for modern homes.",
            "search_query": search_queries[0] if search_queries else "smart fan review",
            "position": 3,
            "timestamp": datetime.now().isoformat(),
            "source": "google_sample"
        },
        {
            "id": "sample_4",
            "title": "Bajaj Maxima 1200mm Ceiling Fan vs Smart Alternatives - Price Comparison",
            "url": "https://www.indianexpress.com/article/technology/reviews/bajaj-smart-fans",
            "snippet": "Bajaj Electricals launches smart ceiling fan range to compete with Atomberg and Havells. Offers app-based speed control and timer functions at competitive pricing. Good build quality with 2-year warranty.",
            "search_query": search_queries[2] if len(search_queries) > 2 else "smart fan best brand",
            "position": 4,
            "timestamp": datetime.now().isoformat(),
            "source": "google_sample"
        },
        {
            "id": "sample_5",
            "title": "Crompton HS Plus Smart Fan Review - Energy Efficient BLDC Motor",
            "url": "https://www.digit.in/reviews/home-appliances/crompton-smart-fan-review",
            "snippet": "Crompton HS Plus smart ceiling fan review reveals excellent energy efficiency and build quality. BLDC motor ensures silent operation. Mobile app allows speed control and scheduling features.",
            "search_query": search_queries[0] if search_queries else "smart fan review",
            "position": 5,
            "timestamp": datetime.now().isoformat(),
            "source": "google_sample"
        }
    ]


print("🔍 Enhanced Google Search Collector Agent Ready!")
