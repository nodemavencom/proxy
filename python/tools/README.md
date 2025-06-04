# NodeMaven Tools

Utility tools for NodeMaven proxy service data management.

## Contents

- **`update_locations.py`** - Script to update location data from the NodeMaven API
- **`locations.json`** - Cached location data (countries, regions, cities, ISPs)

## Usage

### Update Location Data

```bash
python update_locations.py
```

This script fetches the latest location data from the NodeMaven API and updates the `locations.json` file.

## Requirements

- Python 3.7+
- NodeMaven API key (set in environment or .env file)
- `requests` library

## Links

- [NodeMaven Website](https://nodemaven.com?utm_source=github&utm_medium=github_post&utm_campaign=developer_outreach&utm_content=tools_readme) 