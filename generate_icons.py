from PIL import Image, ImageDraw
import os

# Create icons directory if it doesn't exist
os.makedirs('static/icons', exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

print("Generating PWA icons...")

for size in sizes:
    # Create a new image with background color
    img = Image.new('RGB', (size, size), color=(79, 70, 229))
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle in the center
    circle_size = size * 0.7
    margin = (size - circle_size) / 2
    draw.ellipse([margin, margin, margin + circle_size, margin + circle_size], 
                 fill=(255, 255, 255))
    
    # Draw a simple checkmark or "H" in the center
    center = size // 2
    
    # Draw a simple "H" for Habit
    bar_width = size * 0.08
    bar_height = size * 0.5
    bar_margin = size * 0.15
    
    # Left vertical bar
    draw.rectangle([center - bar_width - bar_margin, 
                   center - bar_height/2, 
                   center - bar_margin, 
                   center + bar_height/2], 
                   fill=(79, 70, 229))
    
    # Right vertical bar
    draw.rectangle([center + bar_margin, 
                   center - bar_height/2, 
                   center + bar_width + bar_margin, 
                   center + bar_height/2], 
                   fill=(79, 70, 229))
    
    # Horizontal bar
    draw.rectangle([center - bar_width - bar_margin, 
                   center - bar_width/2, 
                   center + bar_width + bar_margin, 
                   center + bar_width/2], 
                   fill=(79, 70, 229))
    
    # Save the icon
    filename = f'static/icons/icon-{size}x{size}.png'
    img.save(filename)
    print(f'✓ Generated {filename}')

print("\n✓ All icons generated successfully!")
print("You can now run the Django server.")