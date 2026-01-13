#!/usr/bin/env python3
"""
Gallery Update Script
Automatically generates the photo grid HTML for galleries/2025.html
based on images found in images/2025/

Usage: python update_gallery.py
"""

import os
from pathlib import Path
import re

def get_images(image_dir):
    """Get all image files from the directory, sorted by name."""
    image_dir = Path(image_dir)
    
    # Support common image formats
    extensions = ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']
    images = []
    
    for ext in extensions:
        images.extend(image_dir.glob(ext))
    
    # Sort by filename, exclude cover.jpg
    images = sorted([img for img in images if img.name != 'cover.jpg'])
    
    return images

def generate_image_html(images, base_path='../images/2025'):
    """Generate HTML for all images."""
    html_lines = []
    
    for i, img in enumerate(images, 1):
        img_path = f"{base_path}/{img.name}"
        html_lines.append(
            f'        <a href="{img_path}" data-lightbox="gallery" data-title="Photo {i}" class="photo-item">\n'
            f'            <img src="{img_path}" alt="Photo {i}">\n'
            f'        </a>'
        )
    
    return '\n'.join(html_lines)

def update_gallery_file(gallery_file, new_images_html):
    """Update the gallery HTML file with new images."""
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the photo-grid section and replace its contents
    pattern = r'(<div class="photo-grid" id="photo-gallery">)(.*?)(</div>)'
    
    replacement = f'\\1\n{new_images_html}\n    \\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("⚠️  Warning: Could not find photo-grid section to update!")
        return False
    
    with open(gallery_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Configuration
    image_dir = 'images/2025'
    gallery_file = 'galleries/2025.html'
    
    print("🖼️  Gallery Update Script")
    print("=" * 50)
    
    # Check if directories exist
    if not os.path.exists(image_dir):
        print(f"❌ Error: Image directory '{image_dir}' not found!")
        return
    
    if not os.path.exists(gallery_file):
        print(f"❌ Error: Gallery file '{gallery_file}' not found!")
        return
    
    # Get images
    images = get_images(image_dir)
    
    if not images:
        print(f"❌ No images found in '{image_dir}'")
        return
    
    print(f"✓ Found {len(images)} images")
    
    # Generate HTML
    new_html = generate_image_html(images)
    
    # Update file
    if update_gallery_file(gallery_file, new_html):
        print(f"✓ Successfully updated '{gallery_file}'")
        print(f"\n📸 Gallery now contains {len(images)} images")
        print("\n⚡ Next steps:")
        print("   1. Review the changes in galleries/2025.html")
        print("   2. Commit and push:")
        print("      git add galleries/2025.html")
        print("      git commit -m 'Update gallery images'")
        print("      git push")
    else:
        print("❌ Failed to update gallery file")

if __name__ == "__main__":
    main()
