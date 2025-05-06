import urllib.request
import os

def download_maps():
    maps = {
        'earth_texture.jpg': 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg',
        'earth_political.jpg': 'https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57752/land_shallow_topo_2048.jpg',
        'earth_detailed.jpg': 'https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57730/land_ocean_ice_2048.jpg'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for filename, url in maps.items():
        if os.path.exists(filename):
            print(f"Map {filename} already exists")
            continue
            
        print(f"Downloading {filename}...")
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            print("You can manually download and save the file from:")
            print(url)

if __name__ == "__main__":
    download_maps()
