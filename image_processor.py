from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def process_images(input_dir: Path, output_dir: Path, width: int, height: int) -> int:
    """Resize images to target dimensions"""
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    
    for img_path in input_dir.glob("*"):
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue
        
        img = Image.open(img_path)
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        
        output_path = output_dir / img_path.name
        img.save(output_path, quality=95)
        count += 1
    
    return count

def add_watermark(image_dir: Path, text: str):
    """Add watermark text to all images in directory"""
    for img_path in image_dir.glob("*"):
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue
        
        img = Image.open(img_path).convert("RGBA")
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        try:
            font = ImageFont.truetype("Arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = img.width - text_width - 20
        y = img.height - text_height - 20
        
        draw.text((x, y), text, fill=(255, 255, 255, 128), font=font)
        
        watermarked = Image.alpha_composite(img, txt_layer)
        watermarked.convert("RGB").save(img_path, quality=95)
