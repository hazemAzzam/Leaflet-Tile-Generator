import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_png_to_webp(png_path):
    webp_path = os.path.splitext(png_path)[0] + '.webp'
    try:
        with Image.open(png_path) as img:
            img.save(webp_path, 'WEBP')
        os.remove(png_path)
        print(f"Converted: {png_path} to {webp_path}")
    except Exception as e:
        print(f"Failed to convert {png_path}: {e}")

def convert_png_to_webp_in_place(directory):
    png_files = []
    
    # Gather all PNG files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))

    # Use threading to convert files concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(convert_png_to_webp, png_path): png_path for png_path in png_files}
        
        # Wait for all threads to complete and handle any exceptions
        for future in as_completed(futures):
            png_path = futures[future]
            try:
                future.result()  # This will raise any exceptions that occurred
            except Exception as e:
                print(f"Error processing {png_path}: {e}")

# Example usage
directory_path = 'C:/Users/hazem/Desktop/tiles/archieve'
convert_png_to_webp_in_place(directory_path)
