import os
from PIL import Image, ImageDraw, ImageFont

# =====================================================================
# CONFIGURATION: Modify these paths and settings to change the GIF
# =====================================================================

# List of source image paths (relative to this script or absolute)
WINNING_IMAGES = [
    r"generations/loop_1/output/rule_04_random.png",
    r"generations/loop_2/output/rule_02_random.png",
    r"generations/loop_2/output/rule_04_random.png",
    r"generations/loop_2/output/rule_07_single_seed.png",
    r"generations/loop_3/output/rule_08_single_seed.png",
    r"generations/loop_6/output/rule_01_random.png",
    r"generations/loop_8/output/rule_01_random.png",
    r"generations/loop_8/output/rule_02_random.png",
    r"generations/loop_9/output/rule_08_single_seed.png",
    r"generations/loop_10/output/rule_08_single_seed.png",
]

# Labels to overlay on each corresponding frame (leave empty string to disable)
LABELS = [
    "Loop 1: Excitable Cascade (Rule 4)",
    "Loop 2: Parity-Gated Birth (Rule 2)",
    "Loop 3: Fractional Diffusion (Rule 8)",
    "Loop 4: Granular Jamming (Rule 7)",
    "Loop 5: Homeostatic Regulation (Rule 9)",
    "Loop 6: Advection-Diffusion (Rule 1)",
    "Loop 7: French Flag Morphogenesis (Rule 7)",
    "Loop 8: Beam Splitter Interferometer (Rule 8)",
    "Loop 9: Class Struggle & Revolution (Rule 8)",
    "Loop 10: Coupled Henon Map (Rule 6)"
]

# Output path for the animated GIF in the workspace
OUTPUT_GIF_PATH = "winners_showcase.gif"

# Duration for each frame in milliseconds (1500 ms = 1.5 seconds)
FRAME_DURATION = 1500

# Size to resize the images to (width, height). Set to None to keep original size.
RESIZE_DIMENSIONS = (800, 800)

# Text overlay settings
DRAW_TEXT_OVERLAY = False
BANNER_COLOR = (0, 0, 0, 180)  # RGBA color of the text background banner (semi-transparent black)
TEXT_COLOR = (255, 255, 255)    # RGB color of the text (white)
FONT_SIZE = 28                  # Font size in points

# =====================================================================
# GIF GENERATION CORE LOGIC
# =====================================================================

def get_font(size):
    # Try to load a clean system font (Windows standard)
    font_paths = [
        r"C:\Windows\Fonts\arialbd.ttf",  # Arial Bold
        r"C:\Windows\Fonts\arial.ttf",    # Arial
        "arial.ttf",
        "DejaVuSans.ttf"
    ]
    for p in font_paths:
        try:
            return ImageFont.truetype(p, size)
        except IOError:
            continue
    # Fallback to default PIL font
    return ImageFont.load_default()

def create_winners_gif():
    frames = []
    
    print("Starting GIF generation...")
    
    for idx, img_path in enumerate(WINNING_IMAGES):
        if not os.path.exists(img_path):
            print(f"WARNING: Image path not found: {img_path}. Skipping.")
            continue
            
        print(f"Processing frame {idx+1}/{len(WINNING_IMAGES)}: {img_path}")
        img = Image.open(img_path).convert("RGBA")
        
        # Resize if dimension is set
        if RESIZE_DIMENSIONS:
            img = img.resize(RESIZE_DIMENSIONS, Image.Resampling.LANCZOS)
            
        # Add text overlay
        if DRAW_TEXT_OVERLAY and idx < len(LABELS) and LABELS[idx]:
            # Create a separate layer for drawing semi-transparent shapes
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Text parameters
            text = LABELS[idx]
            font = get_font(FONT_SIZE)
            
            # Get text bounding box for positioning
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
            except AttributeError:
                # Fallback for older Pillow versions
                text_w, text_h = draw.textsize(text, font=font)
                
            w, h = img.size
            banner_h = text_h + 30
            banner_y1 = h - banner_h
            
            # Draw semi-transparent background banner at the bottom
            draw.rectangle([(0, banner_y1), (w, h)], fill=BANNER_COLOR)
            
            # Draw text centered in the banner
            text_x = (w - text_w) // 2
            text_y = banner_y1 + (banner_h - text_h) // 2 - 2  # slightly adjusted
            draw.text((text_x, text_y), text, fill=TEXT_COLOR, font=font)
            
            # Alpha composite overlay onto main image
            img = Image.alpha_composite(img, overlay)
            
        # Convert back to RGB for GIF compatibility
        frames.append(img.convert("RGB"))
        
    if not frames:
        print("ERROR: No images found. GIF could not be created.")
        return
        
    # Save the frames as an animated GIF
    frames[0].save(
        OUTPUT_GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )
    print(f"SUCCESS: Animated GIF saved successfully to: {os.path.abspath(OUTPUT_GIF_PATH)}")

    # Copy to the artifact directory if available
    artifact_dir = r"C:\Users\dimitris\.gemini\antigravity-cli\brain\f208e19b-b3a0-4c4c-8d44-6f8eecc8f6d1"
    if os.path.exists(artifact_dir):
        import shutil
        dest = os.path.join(artifact_dir, "winners_showcase.gif")
        shutil.copy2(OUTPUT_GIF_PATH, dest)
        print(f"Copied GIF to artifact directory: {dest}")

if __name__ == "__main__":
    create_winners_gif()
