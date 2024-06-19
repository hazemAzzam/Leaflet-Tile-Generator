import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = 'C:/Users/hazem/Desktop/tiles/archieve'
ZOOM_LEVEL = 7
BASE_URL = "https://a.tile.openstreetmap.org"

headers = {
    'referer': 'https://a.tile.openstreetmap.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

def download_tiles_for_x(x):
    y = 0
    while True:
        # Create the directory path
        dir_path = os.path.join(BASE_DIR, str(ZOOM_LEVEL), str(x))
        os.makedirs(dir_path, exist_ok=True)

        # Define the file path
        file_path = os.path.join(dir_path, f"{y}.png")

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File {file_path} already exists, skipping download.")
            y += 1
            continue

        # Make the request to download the image
        res = requests.get(f"{BASE_URL}/{ZOOM_LEVEL}/{x}/{y}.png", headers=headers)
        if res.status_code == 400:
            print(f"All tiles in {x}-Xaxis have been downloaded!!")
            break
        else:
            # Save the tile image
            with open(file_path, 'wb') as f:
                f.write(res.content)

            print(f'Downloading: {file_path}')

            y += 1

def main():
    max_workers = 10
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_tiles_for_x, x) for x in range(max_workers)]
        completed_x = max_workers

        while True:
            for future in as_completed(futures):
                x = completed_x
                completed_x += 1
                futures.remove(future)
                if (completed_x >= 127):
                    continue
                futures.append(executor.submit(download_tiles_for_x, x))

if __name__ == "__main__":
    main()
