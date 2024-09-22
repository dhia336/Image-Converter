from PIL import Image

def convert_image(input, output, format):
    with Image.open(input) as img:

        if format in ['JPEG', 'BMP'] and img.mode == 'RGBA':
            img = img.convert('RGB')  # Remove alpha channel
        elif format in ['PNG', 'ICO', 'GIF'] and img.mode != 'RGBA':
            img = img.convert('RGBA')  # transparency support
        
        img.save(output, format=format)
        print(f"Converted {input} to {output} in {format} format.")