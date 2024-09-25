import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

BASE_URL = "https://tiles.stadiamaps.com/tiles/alidade_satellite"
THEME_NAME = "alidade_satellite"
BASE_DIR = f'archieve/{THEME_NAME}'

headers = {
    'referer': f'{BASE_URL}',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

def download_tile(x, y, zoom_level):
    # Create the directory path
    dir_path = os.path.join(BASE_DIR, str(zoom_level), str(x))
    os.makedirs(dir_path, exist_ok=True)

    # Define the file path
    file_path = os.path.join(dir_path, f"{y}.png")

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File {file_path} already exists, skipping download.")
        return

    # Make the request to download the image
    res = requests.get(f"{BASE_URL}/{zoom_level}/{x}/{y}.png", headers=headers)
    if res.status_code == 404:
        print(f"Tile {x}/{y} at zoom level {zoom_level} not found.")
    else:
        print(res.status_code, f"{BASE_URL}/{zoom_level}/{x}/{y}.png")
        # Save the tile image
        with open(file_path, 'wb') as f:
            f.write(res.content)

        print(f'Downloading: {file_path}')

def download_tiles_in_range(x_range, y_range, zoom_level):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                futures.append(executor.submit(download_tile, x, y, zoom_level))

        # Wait for all the downloads to complete
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred

def calculate_max_range(zoom_level):
    max_tiles = pow(2, zoom_level)
    return (0, max_tiles - 1)

def main():
    parser = argparse.ArgumentParser(description='Download map tiles.')
    parser.add_argument('zoom_level', type=int, help='Zoom level for the tiles')
    parser.add_argument('--x_range', type=str, help='X tile range (e.g., 578-615)', default=None)
    parser.add_argument('--y_range', type=str, help='Y tile range (e.g., 429-468)', default=None)
    args = parser.parse_args()

    zoom_level = args.zoom_level

    # Determine X and Y ranges
    if args.x_range:
        x_start, x_end = map(int, args.x_range.split('-'))
    else:
        x_start, x_end = calculate_max_range(zoom_level)

    if args.y_range:
        y_start, y_end = map(int, args.y_range.split('-'))
    else:
        y_start, y_end = calculate_max_range(zoom_level)

    # Download tiles in the specified ranges
    download_tiles_in_range((x_start, x_end), (y_start, y_end), zoom_level)

if __name__ == "__main__":
    main()
