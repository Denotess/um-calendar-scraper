# UM Calendar Scraper

A Python web scraper for downloading calendar files (.ics) from the University of Maribor FOV schedule website.

## What It Does

This scraper fetches `.ics` calendar files from the UM FOV schedule system and saves them locally. The calendars can then be served through the [um-calendar-api-cs](../c%23/asp.net/um-calendar-api-cs) API.

## Features

- ✅ Automatically scrapes dropdown options from the schedule website
- ✅ Downloads calendar files in `.ics` format
- ✅ Robust error handling with timeouts
- ✅ Handles network failures gracefully
- ✅ Simple Python scripts - no framework needed

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

### 1. Clone/Navigate to the Project

```bash
cd um-calendar-scraper
```

### 2. Create and Activate Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate it (Linux/Mac)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install beautifulsoup4 requests
```

## Usage

### Get Available Calendar Names

```python
from getLinks import getDropdownNames

# Get list of all available calendar options
names = getDropdownNames()
print(names)
# Output: ['01---1-letnik-VS-Informacijski-sistemi-Redni', '02---1-letnik-VS-...', ...]
```

### Download Calendar Files

```python
from getFiles import downloadCalendars  # Assuming you have this function

# Download all calendars to a folder
downloadCalendars(output_dir='../c#/asp.net/um-calendar-api-cs/calendars')
```

## File Structure

```
um-calendar-scraper/
├── getLinks.py       # Scrapes dropdown names from the schedule website
├── getFiles.py       # Downloads .ics files (calendar downloader)
└── README.md         # This file
```

## How It Works

### `getLinks.py` - Scraping Schedule Names

1. **Fetches the main page** at `https://urnik.fov.um.si/`
2. **Finds the iframe** containing the schedule interface
3. **Loads the iframe content** and parses dropdown options
4. **Filters options** that start with a number (actual schedules)
5. **Returns a list** of available calendar names

**Error Handling:**
- Network timeouts (10 seconds)
- HTTP errors (404, 500, etc.)
- Missing iframe or attributes
- General exceptions

### `getFiles.py` - Downloading Calendars

Downloads the actual `.ics` calendar files based on the names from `getLinks.py`.

## Integration with um-calendar-api-cs

The scraped calendar files are designed to work with the companion API:

```bash
# 1. Run the scraper to download calendars
python getFiles.py

# 2. Files are saved to: ../c#/asp.net/um-calendar-api-cs/calendars/

# 3. Start the API to serve them
cd ../c#/asp.net/um-calendar-api-cs
dotnet run
```

## Example Output

```python
>>> from getLinks import getDropdownNames
>>> names = getDropdownNames()
>>> len(names)
47
>>> names[0]
'01---1-letnik-VS-Informacijski-sistemi-Redni'
```

## Error Handling

The scraper handles various errors gracefully:

- **Network Timeout**: Returns empty list after 10 seconds
- **HTTP Errors**: Catches 404, 500, etc. and returns empty list
- **Missing Elements**: Validates iframe and attributes exist
- **Unknown Errors**: Catches all exceptions with fallback handling

All errors are logged to console with descriptive messages.

## Technologies Used

- **Python 3** - Programming language
- **BeautifulSoup4** - HTML parsing and web scraping
- **Requests** - HTTP library for making web requests
- **urllib.parse** - URL manipulation

## Notes

- The scraper respects the source website's structure
- Uses timeouts to prevent hanging
- Returns empty lists on errors (never crashes)
- Designed for integration with the C# API

## Future Improvements

- Retry logic for failed downloads

## Related Projects

- **[um-calendar-api-cs](../c%23/asp.net/um-calendar-api-cs)** - ASP.NET Core API for serving the scraped calendars

## License

Free to use for educational purposes.
