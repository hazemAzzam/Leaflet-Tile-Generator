import os
from PIL import Image

def convert_png_to_webp_in_place(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_path = os.path.join(root, file)
                webp_path = os.path.splitext(png_path)[0] + '.webp'
                try:
                    with Image.open(png_path) as img:
                        img.save(webp_path, 'WEBP')
                    os.remove(png_path)
                    print(f"Converted: {png_path} to {webp_path}")
                except Exception as e:
                    print(f"Failed to convert {png_path}: {e}")

# Example usage
directory_path = 'archieve'
convert_png_to_webp_in_place(directory_path)
