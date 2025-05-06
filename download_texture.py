import urllib.request
import os

def download_earth_texture():
    url = "https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg"
    output_file = "earth_texture.jpg"
    
    if os.path.exists(output_file):
        print(f"Texture file already exists at: {output_file}")
        return
        
    print("Downloading Earth texture...")
    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"Successfully downloaded texture to: {output_file}")
    except Exception as e:
        print(f"Error downloading texture: {e}")

if __name__ == "__main__":
    download_earth_texture()
