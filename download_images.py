"""
Script to create placeholder images for products
Note: For production, replace with actual product images
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Create images directory if not exists
images_dir = 'static/images'
os.makedirs(images_dir, exist_ok=True)

# Create a simple placeholder image
def create_placeholder(filename, text):
    # Create image with gradient background
    img = Image.new('RGB', (400, 400), color=(100, 100, 200))
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, text, fill=(255, 255, 255), font=font)
    
    # Save
    img.save(os.path.join(images_dir, filename))
    print(f"Created: {filename}")

# Create placeholder for common product types
create_placeholder('placeholder.jpg', 'Product Image')

print("\nPlaceholder images created!")
print("Note: Replace these with actual product images for production")
