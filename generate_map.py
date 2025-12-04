import gpxpy
import json
import glob
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
GPX_FILENAME = 'gpx_20251102_id10470_race1_20250929105512.gpx' 
OUTPUT_FILENAME = 'marathon_map.html'
STYLE_PATTERN = 'styles/*.json'  # Pattern to find all style files
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # Load from .env file

if not API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables. Please create a .env file with your API key.")

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <title>NYC Marathon Route 2025</title>
    <style>
      html, body { height: 100%; margin: 0; padding: 0; font-family: Arial, sans-serif; }
      #map { height: 100%; }
      #style-selector {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1000;
        background: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      }
      #style-selector label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 14px;
      }
      #style-selector select {
        padding: 8px;
        font-size: 14px;
        border: 1px solid #ccc;
        border-radius: 3px;
        min-width: 200px;
      }
    </style>
  </head>
  <body>
    <div id="style-selector">
      <label for="style-dropdown">Map Style:</label>
      <select id="style-dropdown" onchange="changeMapStyle(this.value)">
        __STYLE_OPTIONS__
      </select>
    </div>
    <div id="map"></div>
    <script>
      let map;
      let marathonPath;
      let startMarker;
      let finishMarker;
      
      // All available styles: Injected from Python
      const allStyles = __ALL_STYLES__;
      
      // Default style name: Injected from Python
      const defaultStyle = '__DEFAULT_STYLE__';

      function initMap() {
        // DATA: Injected from Python
        const routeCoords = __ROUTE_COORDS__;

        // Get default style
        const initialStyle = allStyles[defaultStyle] || [];

        // MAP SETUP
        map = new google.maps.Map(document.getElementById("map"), {
          center: routeCoords.length > 0 ? routeCoords[0] : { lat: 40.7128, lng: -74.0060 },
          zoom: 12,
          styles: initialStyle
        });

        // DRAW LINE
        marathonPath = new google.maps.Polyline({
          path: routeCoords,
          geodesic: true,
          strokeColor: "#FF0000",
          strokeOpacity: 1.0,
          strokeWeight: 4,
        });
        marathonPath.setMap(map);

        // Fit bounds
        const bounds = new google.maps.LatLngBounds();
        routeCoords.forEach(pt => bounds.extend(pt));
        map.fitBounds(bounds);

        // MARKERS
        if (routeCoords.length > 0) {
            startMarker = new google.maps.Marker({
                position: routeCoords[0],
                map: map,
                title: "Start",
                icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            });
            finishMarker = new google.maps.Marker({
                position: routeCoords[routeCoords.length - 1],
                map: map,
                title: "Finish",
                icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
            });
        }
      }
      
      function changeMapStyle(styleName) {
        if (map && allStyles[styleName]) {
          map.setOptions({ styles: allStyles[styleName] });
        }
      }
    </script>
    <script async
      src="https://maps.googleapis.com/maps/api/js?key=__API_KEY__&callback=initMap">
    </script>
  </body>
</html>
"""

def load_all_styles(pattern):
    """Load all map style files matching the pattern"""
    style_files = glob.glob(pattern)
    styles = {}
    
    if not style_files:
        print(f"Warning: No style files found matching pattern '{pattern}'. Using empty style.")
        return styles, None
    
    for style_file in sorted(style_files):
        try:
            with open(style_file, 'r') as f:
                style_data = json.load(f)
                # Use filename without extension as key
                style_name = os.path.splitext(os.path.basename(style_file))[0]
                styles[style_name] = style_data
               # print(f"Loaded style: {style_name}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {style_file}")
        except Exception as e:
            print(f"Error loading {style_file}: {e}")
    
    # Return first style as default
    default = list(styles.keys())[0] if styles else None
    return styles, default

def load_map_style(filename):
    """Load map style from JSON file (legacy function for backward compatibility)"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find {filename}. Using default style.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return []

def parse_gpx_to_json(filename):
    try:
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append({'lat': point.latitude, 'lng': point.longitude})
        return points
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        return []

def generate_html(route_data, all_styles_dict, default_style_name, api_key):
    # Convert Python objects to JSON strings for JavaScript
    json_coords = json.dumps(route_data)
    json_all_styles = json.dumps(all_styles_dict)
    
    # Generate dropdown options
    style_options = ""
    for style_name in sorted(all_styles_dict.keys()):
        selected = "selected" if style_name == default_style_name else ""
        display_name = style_name.replace("_", " ").title()
        style_options += f'<option value="{style_name}" {selected}>{display_name}</option>\n        '

    html_content = (
        HTML_TEMPLATE
        .replace("__ROUTE_COORDS__", json_coords)
        .replace("__ALL_STYLES__", json_all_styles)
        .replace("__DEFAULT_STYLE__", default_style_name or "")
        .replace("__STYLE_OPTIONS__", style_options)
        .replace("__API_KEY__", api_key)
    )
    return html_content

if __name__ == "__main__":
    print(f"Reading {GPX_FILENAME}...")
    coords = parse_gpx_to_json(GPX_FILENAME)
    
    if coords:
        print(f"Extracted {len(coords)} points.")
        print(f"Loading all map styles matching '{STYLE_PATTERN}'...")
        all_styles, default_style = load_all_styles(STYLE_PATTERN)
        
        if not all_styles:
            print("Warning: No styles loaded. Map will use default Google Maps style.")
            all_styles = {}
            default_style = None
        
        # Generate HTML with all styles
        html_output = generate_html(coords, all_styles, default_style, API_KEY)
        
        with open(OUTPUT_FILENAME, 'w') as f:
            f.write(html_output)
        print(f"Success! Map generated: {OUTPUT_FILENAME}")
        # print(f"Available styles: {', '.join(all_styles.keys())}")
    else:
        print("No data extracted.")