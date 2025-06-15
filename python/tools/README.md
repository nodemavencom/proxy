# NodeMaven Tools

Utility tools for NodeMaven proxy service data management and location updates.

## Contents

- **`update_locations.py`** - Script to fetch and cache location data from NodeMaven API
- **`locations.json`** - Cached location data (countries, regions, cities, ISPs)

## Usage

### Update Location Data

```bash
# From the python directory
cd python/

# Run the location update tool
python tools/update_locations.py
```

This script:
- ✅ Fetches the latest location data from the NodeMaven API
- ✅ Updates the `locations.json` cache file
- ✅ Provides readable output of available locations
- ✅ Handles API errors gracefully

### Location Data Structure

The `locations.json` file contains:
```json
{
  "countries": [
    {"name": "United States", "code": "us"},
    {"name": "United Kingdom", "code": "gb"}
  ],
  "regions": [
    {"name": "California", "code": "california", "country": "us"},
    {"name": "New York", "code": "new_york", "country": "us"}
  ],
  "cities": [
    {"name": "Los Angeles", "code": "los_angeles", "region": "california"},
    {"name": "Brooklyn", "code": "brooklyn", "region": "new_york"}
  ],
  "isps": [
    {"name": "Verizon", "country": "us"},
    {"name": "BT Group", "country": "gb"}
  ]
}
```

## Requirements

- **Python**: 3.8+
- **NodeMaven API key**: Set in environment or `.env` file
- **Dependencies**: `requests` library (optional, falls back to urllib)

## Environment Setup

```bash
# Set your API key
export NODEMAVEN_APIKEY="your_api_key_here"

# Or add to .env file
echo "NODEMAVEN_APIKEY=your_api_key_here" >> .env
```

## Integration

The location data can be used in your applications:

```python
import json

# Load cached location data
with open('tools/locations.json', 'r') as f:
    locations = json.load(f)

# Get available countries
countries = locations['countries']
for country in countries:
    print(f"{country['name']} ({country['code']})")
```

## Automation

You can automate location updates:

```bash
# Add to crontab for daily updates
0 2 * * * cd /path/to/python && python tools/update_locations.py
```

## Links

- 📖 [NodeMaven Dashboard](https://dashboard.nodemaven.com?utm_source=github&utm_medium=tools_readme&utm_campaign=developer_outreach)
- 📋 [API Documentation](https://dashboard.nodemaven.com/documentation?utm_source=github&utm_medium=tools_readme&utm_campaign=developer_outreach) 