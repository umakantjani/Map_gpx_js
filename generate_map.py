import gpxpy
import json

# --- CONFIGURATION ---
GPX_FILENAME = 'gpx_20251102_id10470_race1_20250929105512.gpx' 
OUTPUT_FILENAME = 'marathon_map.html'
MAP_STYLE_FILE = 'map_style.json'
API_KEY = 'AIzaSyAv4_E-2a4GY8g1nkp79rtxQDgwdXVNt4w'  # Paste your API key here

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <title>NYC Marathon Route 2025</title>
    <style>
      html, body { height: 100%; margin: 0; padding: 0; }
      #map { height: 100%; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      function initMap() {
        
        // 1. STYLE: Injected from Python
        const mapStyle = __MAP_STYLE__;

        // 2. DATA: Injected from Python
        const routeCoords = __ROUTE_COORDS__;

        // 3. MAP SETUP
        const map = new google.maps.Map(document.getElementById("map"), {
          center: routeCoords.length > 0 ? routeCoords[0] : { lat: 40.7128, lng: -74.0060 },
          zoom: 12,
          styles: mapStyle
        });

        // 4. DRAW LINE
        const marathonPath = new google.maps.Polyline({
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

        // 5. MARKERS
        if (routeCoords.length > 0) {
            new google.maps.Marker({
                position: routeCoords[0],
                map: map,
                title: "Start",
                icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            });
            new google.maps.Marker({
                position: routeCoords[routeCoords.length - 1],
                map: map,
                title: "Finish",
                icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
            });
        }
      }
    </script>
    <script async
      src="https://maps.googleapis.com/maps/api/js?key=__API_KEY__&callback=initMap">
    </script>
  </body>
</html>
"""

def load_map_style(filename):
    """Load map style from JSON file"""
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

def generate_html(route_data, style_data, api_key):
    # Convert Python objects to JSON strings for JavaScript
    json_coords = json.dumps(route_data)
    json_style = json.dumps(style_data)

    html_content = (
        HTML_TEMPLATE
        .replace("__MAP_STYLE__", json_style)
        .replace("__ROUTE_COORDS__", json_coords)
        .replace("__API_KEY__", api_key)
    )
    return html_content

if __name__ == "__main__":
    print(f"Reading {GPX_FILENAME}...")
    coords = parse_gpx_to_json(GPX_FILENAME)
    
    if coords:
        print(f"Extracted {len(coords)} points.")
        print(f"Loading map style from {MAP_STYLE_FILE}...")
        map_style = load_map_style(MAP_STYLE_FILE)
        # Pass the detailed style to the generator
        html_output = generate_html(coords, map_style, API_KEY)
        
        with open(OUTPUT_FILENAME, 'w') as f:
            f.write(html_output)
        print(f"Success! Map generated: {OUTPUT_FILENAME}")
    else:
        print("No data extracted.")