#!/usr/bin/env python3
"""
NodeMaven Web Scraping Demo

This example demonstrates how to use NodeMaven proxies for web scraping
with different targeting options, session management, and error handling.

Features demonstrated:
- Multi-country scraping
- Session persistence 
- Error handling and retries
- IP rotation strategies
- Data extraction and validation

Requirements:
    pip install nodemaven requests beautifulsoup4
"""

import time
import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from nodemaven import NodeMavenClient
from nodemaven.utils import build_proxy_url, get_proxy_config


@dataclass
class ScrapingResult:
    """Result of a scraping operation."""
    url: str
    country: str
    ip_address: str
    status_code: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    response_time: float = 0.0


class NodeMavenScraper:
    """Professional web scraper using NodeMaven proxies."""
    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        """
        Initialize the scraper.
        
        Args:
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
        """
        self.client = NodeMavenClient()
        self.max_retries = max_retries
        self.timeout = timeout
        self.session_id = f"scraper_{int(time.time())}"
        
        # Verify connectivity
        user_info = self.client.get_user_info()
        print(f"✅ Connected as: {user_info['email']}")
        print(f"✅ Proxy Username: {user_info.get('proxy_username', 'N/A')}")
    
    def scrape_with_proxy(self, url: str, country: str, 
                         ttl: str = "10m") -> ScrapingResult:
        """
        Scrape a URL using a proxy from the specified country.
        
        Args:
            url: URL to scrape
            country: Country code for proxy (e.g., 'us', 'gb')
            ttl: Session time-to-live
            
        Returns:
            ScrapingResult with scraping outcome
        """
        start_time = time.time()
        
        for attempt in range(1, self.max_retries + 1):
            try:
                # Get proxy configuration
                proxies = get_proxy_config(
                    country=country,
                    session=f"{self.session_id}_{country}",
                    ttl=ttl,
                    filter="high"
                )
                
                print(f"🌍 [{country.upper()}] Attempt {attempt}/{self.max_retries}: {url}")
                
                # Make request through proxy
                response = requests.get(
                    url, 
                    proxies=proxies,
                    timeout=self.timeout,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                
                response_time = time.time() - start_time
                
                # Get IP address used
                ip_response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
                ip_address = ip_response.json().get('origin', 'Unknown')
                
                # Parse response based on content type
                data = self._parse_response(response)
                
                return ScrapingResult(
                    url=url,
                    country=country,
                    ip_address=ip_address,
                    status_code=response.status_code,
                    data=data,
                    response_time=response_time
                )
                
            except Exception as e:
                print(f"❌ [{country.upper()}] Attempt {attempt} failed: {e}")
                
                if attempt == self.max_retries:
                    return ScrapingResult(
                        url=url,
                        country=country,
                        ip_address="Unknown",
                        status_code=0,
                        error=str(e),
                        response_time=time.time() - start_time
                    )
                
                # Wait before retry
                time.sleep(2 ** attempt)
        
        return ScrapingResult(
            url=url,
            country=country, 
            ip_address="Unknown",
            status_code=0,
            error="Max retries exceeded"
        )
    
    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse response content based on content type."""
        content_type = response.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            return response.json()
        elif 'text/html' in content_type:
            soup = BeautifulSoup(response.content, 'html.parser')
            return {
                'title': soup.title.string if soup.title else None,
                'text_length': len(soup.get_text().strip()),
                'links': len(soup.find_all('a')),
                'images': len(soup.find_all('img')),
            }
        else:
            return {
                'content_type': content_type,
                'content_length': len(response.content),
                'status': 'success'
            }
    
    def multi_country_scrape(self, urls: List[str], 
                           countries: List[str]) -> List[ScrapingResult]:
        """
        Scrape multiple URLs from different countries simultaneously.
        
        Args:
            urls: List of URLs to scrape
            countries: List of country codes to use
            
        Returns:
            List of ScrapingResult objects
        """
        results = []
        
        # Create scraping tasks
        tasks = []
        for url in urls:
            for country in countries:
                tasks.append((url, country))
        
        print(f"🚀 Starting {len(tasks)} scraping tasks...")
        
        # Execute tasks in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_task = {
                executor.submit(self.scrape_with_proxy, url, country): (url, country)
                for url, country in tasks
            }
            
            for future in as_completed(future_to_task):
                url, country = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.error:
                        print(f"❌ [{country.upper()}] {url}: {result.error}")
                    else:
                        print(f"✅ [{country.upper()}] {url}: {result.ip_address} ({result.response_time:.2f}s)")
                        
                except Exception as e:
                    print(f"❌ [{country.upper()}] {url}: Exception - {e}")
                    results.append(ScrapingResult(
                        url=url,
                        country=country,
                        ip_address="Unknown",
                        status_code=0,
                        error=str(e)
                    ))
        
        return results
    
    def print_summary(self, results: List[ScrapingResult]) -> None:
        """Print a summary of scraping results."""
        print(f"\n{'='*60}")
        print(f"📊 SCRAPING SUMMARY")
        print(f"{'='*60}")
        
        successful = [r for r in results if not r.error]
        failed = [r for r in results if r.error]
        
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"🌍 Countries used: {len(set(r.country for r in results))}")
        
        if successful:
            avg_time = sum(r.response_time for r in successful) / len(successful)
            print(f"⏱️  Average response time: {avg_time:.2f}s")
            
            print(f"\n🌍 IPs by Country:")
            country_ips = {}
            for result in successful:
                if result.country not in country_ips:
                    country_ips[result.country] = set()
                country_ips[result.country].add(result.ip_address)
            
            for country, ips in country_ips.items():
                print(f"  {country.upper()}: {', '.join(sorted(ips))}")
        
        if failed:
            print(f"\n❌ Failed Requests:")
            for result in failed:
                print(f"  [{result.country.upper()}] {result.url}: {result.error}")


def demo_basic_scraping():
    """Demonstrate basic scraping with different countries."""
    print("🎯 Demo 1: Basic Multi-Country Scraping")
    print("="*50)
    
    scraper = NodeMavenScraper()
    
    # Test URLs
    urls = [
        "http://httpbin.org/ip",
        "http://httpbin.org/headers",
        "http://httpbin.org/user-agent"
    ]
    
    # Countries to test
    countries = ["us", "gb", "ca"]
    
    results = scraper.multi_country_scrape(urls, countries)
    scraper.print_summary(results)


def demo_ecommerce_scraping():
    """Demonstrate e-commerce price monitoring."""
    print("\n🛒 Demo 2: E-commerce Price Monitoring")
    print("="*50)
    
    scraper = NodeMavenScraper()
    
    # Example URLs (using httpbin for demo)
    urls = [
        "http://httpbin.org/json",  # Simulates product API
        "http://httpbin.org/xml",   # Simulates product feed
    ]
    
    countries = ["us", "gb", "de", "fr"]
    
    results = scraper.multi_country_scrape(urls, countries)
    
    # Analyze price differences (simulated)
    print(f"\n💰 Price Analysis:")
    for result in results:
        if result.data and not result.error:
            print(f"  [{result.country.upper()}] IP: {result.ip_address} - Response: {result.status_code}")


def demo_social_media_monitoring():
    """Demonstrate social media monitoring from different locations."""
    print("\n📱 Demo 3: Social Media Monitoring")
    print("="*50)
    
    scraper = NodeMavenScraper()
    
    # Social media APIs (using httpbin for demo)
    urls = [
        "http://httpbin.org/anything/social/posts",
        "http://httpbin.org/anything/social/trends",
    ]
    
    # Different regions for social media monitoring
    countries = ["us", "gb", "jp", "br"]
    
    results = scraper.multi_country_scrape(urls, countries)
    
    # Analyze social trends by region
    print(f"\n📈 Regional Trends:")
    for result in results:
        if not result.error:
            print(f"  [{result.country.upper()}] Monitoring from: {result.ip_address}")


def main():
    """Run all scraping demos."""
    print("🚀 NodeMaven Web Scraping Demo")
    print("🌍 Professional Web Scraping with Global Proxies")
    print("="*60)
    
    try:
        # Run demonstrations
        demo_basic_scraping()
        demo_ecommerce_scraping()
        demo_social_media_monitoring()
        
        print(f"\n🎉 All demos completed successfully!")
        print(f"💡 This demonstrates how NodeMaven enables:")
        print(f"   - Global data collection")
        print(f"   - Session management")
        print(f"   - Reliable proxy rotation")
        print(f"   - Professional error handling")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print(f"💡 Make sure you have:")
        print(f"   - Valid NodeMaven API key in .env file")
        print(f"   - Internet connection")
        print(f"   - Required packages: pip install nodemaven requests beautifulsoup4")


if __name__ == "__main__":
    main() 