import subprocess
import os
import pygame

def load_png_keep_aspect_ratio(png_filename, height):
    # Load the PNG image data into Pygame
    image = pygame.image.load(png_filename)

    # Calculate new width to maintain aspect ratio
    aspect_ratio = image.get_width() / image.get_height()
    new_height = height
    new_width = int(aspect_ratio * new_height)

    # Scale the image to the new size
    image = pygame.transform.scale(image, (new_width, new_height))

    return image

def convert_svgs_to_pngs(svg_dir, png_dir, height):
    # Check if Inkscape is installed and in the system's PATH
    try:
        subprocess.run(['inkscape', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        raise RuntimeError("Inkscape is not installed or not found in PATH.")

    # Create the output directory if it does not exist
    os.makedirs(png_dir, exist_ok=True)

    # Iterate over all SVG files in the input directory
    for svg_file in os.listdir(svg_dir):
        if svg_file.lower().endswith('.svg'):
            svg_file_path = os.path.join(svg_dir, svg_file)
            png_file_path = os.path.join(png_dir, os.path.splitext(svg_file)[0] + '.png')

            # Construct the Inkscape command
            command = [
                'inkscape',
                svg_file_path,
                '--export-filename=' + png_file_path,
                '--export-height=' + str(height)
            ]

            # Execute the command
            try:
                subprocess.run(command, check=True)
                print(f"Converted {svg_file} to PNG.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {svg_file}: {e}")

#Use this function to convert the SVGs to PNGs
#convert_svgs_to_pngs('gui/assets/pieces/SVGs', 'gui/assets/pieces/PNGs', 600)
