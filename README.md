# GPX Map Generator

A Python tool that converts GPX (GPS Exchange Format) files into interactive HTML maps using Google Maps API. Perfect for visualizing race routes, marathon paths, or any GPS track data.

## Features

- 🗺️ **Interactive Google Maps visualization** of GPX routes
- 🎨 **Multiple map styles** - Switch between various map styles via dropdown
- 📍 **Start/Finish markers** - Automatically marks the beginning and end of your route
- 🔴 **Route visualization** - Displays the complete route as a red polyline
- ⚙️ **Customizable** - Easy to configure GPX file and output settings

## Requirements

- Python 3.6+
- Google Maps API Key
- Python packages (see `requirements.txt`)

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Google Maps API key:
   ```
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

   To get a Google Maps API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the "Maps JavaScript API"
   - Create credentials (API Key)
   - Copy the API key to your `.env` file

## Usage

1. Place your GPX file in the project root directory

2. Update the `GPX_FILENAME` variable in `generate_map.py` to match your GPX file name:
   ```python
   GPX_FILENAME = 'your_file.gpx'
   ```

3. Run the script:
   ```bash
   python generate_map.py
   ```

4. Open the generated `marathon_map.html` file in your web browser to view the interactive map

## Configuration

You can customize the following settings in `generate_map.py`:

- **`GPX_FILENAME`**: Name of the GPX file to process
- **`OUTPUT_FILENAME`**: Name of the generated HTML file (default: `marathon_map.html`)
- **`STYLE_PATTERN`**: Pattern to find map style JSON files (default: `styles/*.json`)

## Map Styles

The project includes multiple map styles in the `styles/` directory. The script automatically loads all JSON style files and makes them available in the dropdown menu. You can:

- Use existing styles from the `styles/` directory
- Add your own custom styles by creating new JSON files in the `styles/` directory
- Customize styles using [Google Maps Styling Wizard](https://mapstyle.withgoogle.com/)

## Project Structure

```
Map_gpx_js/
├── generate_map.py          # Main Python script
├── marathon_map.html        # Generated HTML output
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── styles/                  # Map style JSON files
│   ├── _ms_blacks.json
│   ├── _ms_blue_days.json
│   └── ...
└── *.gpx                    # Your GPX files
```

## Dependencies

- **gpxpy**: For parsing GPX files
- **python-dotenv**: For loading environment variables from `.env` file

## Notes

- Make sure your Google Maps API key has the "Maps JavaScript API" enabled
- The generated HTML file contains the API key, so be careful when sharing it
- The map automatically fits the bounds of your route
- Start marker is green, finish marker is red

## License

This project is open source and available for personal and commercial use.

