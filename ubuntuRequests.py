import requests
import os
import hashlib
from urllib.parse import urlparse

def generate_unique_filename(url, content):
    """Generate a unique filename using URL and content hash"""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    content_hash = hashlib.md5(content).hexdigest()[:8]
    extension = os.path.splitext(urlparse(url).path)[1]
    return f"image_{url_hash}_{content_hash}{extension or '.jpg'}"

def is_duplicate_image(content, directory):
    """Check if image with same content already exists"""
    content_hash = hashlib.md5(content).hexdigest()
    for existing_file in os.listdir(directory):
        if existing_file.endswith(content_hash[:8]):
            return True
    return False

def validate_image_response(response):
    """Validate if response contains image data"""
    if not response.headers.get('Content-Type', '').startswith('image/'):
        raise ValueError("URL does not point to an image resource")
    if int(response.headers.get('Content-Length', 0)) > 10 * 1024 * 1024:  # 10MB limit
        raise ValueError("File size exceeds safety limit")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    url = input("Please enter the image URL: ").strip()
    
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
        
        # Fetch with headers to mimic browser request
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Community Image Collection Tool)'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Security validations
        validate_image_response(response)
        
        # Check for duplicates
        if is_duplicate_image(response.content, "Fetched_Images"):
            print("Image already exists in collection")
            return
            
        # Generate safe filename
        filename = generate_unique_filename(url, response.content)
        filepath = os.path.join("Fetched_Images", filename)
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        print("\nConnection strengthened. Community enriched.")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except ValueError as e:
        print(f"✗ Security validation failed: {e}")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()