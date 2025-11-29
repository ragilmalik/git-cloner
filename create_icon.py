"""
Create application icon for RagilmalikGitCloner
Uses Pillow to generate a .ico file from scratch
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image (standard for Windows icons)
    size = (256, 256)
    # Gradient background (Dark blue to purple)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw rounded background circle
    margin = 10
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill='#1E90FF', outline='#00BFFF', width=5)
    
    # Draw Git-like branch icon (Simplified)
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Main branch (Vertical)
    draw.line([center_x, size[1]-50, center_x, 50], fill='white', width=20)
    
    # Forked branch (Right)
    draw.line([center_x, center_y, center_x + 60, center_y - 60], fill='white', width=20)
    
    # Nodes (Circles)
    node_radius = 25
    # Bottom
    draw.ellipse([center_x-node_radius, size[1]-70-node_radius, center_x+node_radius, size[1]-70+node_radius], fill='white')
    # Top Main
    draw.ellipse([center_x-node_radius, 70-node_radius, center_x+node_radius, 70+node_radius], fill='white')
    # Top Fork
    draw.ellipse([center_x+60-node_radius, center_y-60-node_radius, center_x+60+node_radius, center_y-60+node_radius], fill='white')

    # Ensure assets folder exists
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Save as PNG first
    image.save('assets/icon.png')
    
    # Save as ICO (containing multiple sizes for best scaling)
    image.save('assets/icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    print("Icon created: assets/icon.ico")

if __name__ == "__main__":
    create_icon()