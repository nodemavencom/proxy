#!/usr/bin/env python3
"""
Script to download and update locations data from NodeMaven API.

This script downloads the complete locations database from NodeMaven
and saves it as locations.json for offline use and faster lookups.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime


def download_locations():
    """Download locations data from NodeMaven API."""
    
    api_key = os.getenv('NODEMAVEN_APIKEY')
    if not api_key:
        print("❌ Error: NODEMAVEN_APIKEY not found in environment variables")
        print("   Please set your API key in the .env file")
        return False
    
    base_url = os.getenv('NODEMAVEN_BASE_URL', 'https://dashboard.nodemaven.com')
    endpoint = f"{base_url}/api/v2/base/locations/all/"
    
    print("🌍 Downloading locations data from NodeMaven...")
    print(f"   Endpoint: {endpoint}")
    
    try:
        # Create request
        req = urllib.request.Request(
            endpoint,
            headers={
                'Authorization': f'x-api-key {api_key}',
                'Accept': 'application/json'
            }
        )
        
        # Download data
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                
                # Save to file
                output_file = 'locations.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Get file size
                file_size = os.path.getsize(output_file)
                file_size_mb = file_size / (1024 * 1024)
                
                print(f"✅ Locations data downloaded successfully!")
                print(f"   File: {output_file}")
                print(f"   Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")
                print(f"   Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Show summary statistics
                show_summary(data)
                
                return True
            else:
                print(f"❌ HTTP Error {response.status}: {response.reason}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        if e.code == 403:
            print("   💡 Tip: Check if your API key is valid and not expired")
        return False
    except Exception as e:
        print(f"❌ Error downloading locations: {e}")
        return False


def show_summary(data):
    """Show summary statistics of the locations data."""
    
    print("\n📊 Locations Summary:")
    
    try:
        if isinstance(data, list):
            countries = len(data)
            total_regions = 0
            total_cities = 0
            total_isps = 0
            
            sample_countries = []
            
            for country in data:
                if 'countryCode' in country:
                    sample_countries.append(country['countryCode'].upper())
                
                if 'regions' in country:
                    total_regions += len(country['regions'])
                    
                    for region in country['regions']:
                        if 'cities' in region:
                            total_cities += len(region['cities'])
                            
                            for city in region['cities']:
                                if 'isps' in city:
                                    total_isps += len(city['isps'])
            
            print(f"   🌍 Countries: {countries}")
            print(f"   🏞️  Regions: {total_regions}")
            print(f"   🏙️  Cities: {total_cities}")
            print(f"   🌐 ISPs: {total_isps}")
            
            if sample_countries:
                sample_display = ', '.join(sample_countries[:10])
                if len(sample_countries) > 10:
                    sample_display += f" ... (+{len(sample_countries) - 10} more)"
                print(f"   📝 Countries: {sample_display}")
        else:
            print("   ⚠️  Unexpected data structure")
            
    except Exception as e:
        print(f"   ⚠️  Could not parse summary: {e}")


def load_locations():
    """Load locations data from file."""
    
    try:
        with open('locations.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ locations.json not found. Run this script to download it first.")
        return None
    except Exception as e:
        print(f"❌ Error loading locations.json: {e}")
        return None


def search_locations(query):
    """Search locations by name or code."""
    
    data = load_locations()
    if not data:
        return []
    
    results = []
    query_lower = query.lower()
    
    try:
        for country in data:
            country_code = country.get('countryCode', '').lower()
            
            # Check country match
            if query_lower in country_code:
                results.append({
                    'type': 'country',
                    'code': country_code.upper(),
                    'name': country_code.upper()
                })
            
            # Check regions and cities
            for region in country.get('regions', []):
                region_code = region.get('regionCode', '').lower()
                
                if query_lower in region_code:
                    results.append({
                        'type': 'region',
                        'country': country_code.upper(),
                        'code': region_code,
                        'name': region_code.replace('_', ' ').title()
                    })
                
                for city in region.get('cities', []):
                    city_code = city.get('cityCode', '').lower()
                    
                    if query_lower in city_code:
                        results.append({
                            'type': 'city',
                            'country': country_code.upper(),
                            'region': region_code,
                            'code': city_code,
                            'name': city_code.replace('_', ' ').title()
                        })
                    
                    # Check ISPs
                    for isp in city.get('isps', []):
                        isp_code = isp.get('ispCode', '').lower()
                        
                        if query_lower in isp_code:
                            results.append({
                                'type': 'isp',
                                'country': country_code.upper(),
                                'region': region_code,
                                'city': city_code,
                                'code': isp_code,
                                'name': isp_code.replace('_', ' ').title()
                            })
    
    except Exception as e:
        print(f"❌ Error searching: {e}")
        return []
    
    return results


def main():
    """Main function."""
    
    print("🚀 NodeMaven Locations Updater")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "search" and len(sys.argv) > 2:
            query = sys.argv[2]
            print(f"🔍 Searching for: {query}")
            results = search_locations(query)
            
            if results:
                print(f"   Found {len(results)} results:")
                for result in results[:20]:  # Show first 20 results
                    if result['type'] == 'country':
                        print(f"   - Country: {result['code']}")
                    elif result['type'] == 'region':
                        print(f"   - Region: {result['name']} ({result['country']})")
                    elif result['type'] == 'city':
                        print(f"   - City: {result['name']} ({result['country']}/{result['region']})")
                    elif result['type'] == 'isp':
                        print(f"   - ISP: {result['name']} ({result['country']}/{result['city']})")
                
                if len(results) > 20:
                    print(f"   ... and {len(results) - 20} more")
            else:
                print("   No results found")
            return
        
        elif command == "info":
            data = load_locations()
            if data:
                show_summary(data)
            return
        
        elif command == "help":
            print("Usage:")
            print("  python update_locations.py          - Download latest locations")
            print("  python update_locations.py search <query>  - Search locations")
            print("  python update_locations.py info     - Show locations summary")
            print("  python update_locations.py help     - Show this help")
            return
    
    # Default action: download locations
    success = download_locations()
    
    if success:
        print("\n🎉 Locations update completed successfully!")
        print("\n💡 Usage examples:")
        print("   python scripts/update_locations.py search US")
        print("   python scripts/update_locations.py search california")
        print("   python scripts/update_locations.py info")
    else:
        print("\n❌ Locations update failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 