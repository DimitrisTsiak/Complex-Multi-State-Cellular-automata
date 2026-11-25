import os
import shutil
from PIL import Image

# 1. Output configurations
OUTPUT_GIF_PATH = "winners_1x5_showcase.gif"
ARTIFACT_DIR = r"C:\Users\dimitris\.gemini\antigravity-cli\brain\ef3bfa56-bb9c-4382-99f6-46986bd58e36"

# 2. Dimensions and spacing (Seamless edge-to-edge stitching)
IMAGE_W = 240
IMAGE_H = 240
PADDING = 0  # 0 padding for seamless horizontal strip

# Calculate total canvas size
CANVAS_WIDTH = 5 * IMAGE_W + 4 * PADDING
CANVAS_HEIGHT = IMAGE_H

# 3. Simple list of image paths to process (flat list).
#    showcase/ holds committed copies of the originals, so the GIF can be rebuilt from a clone.
IMAGE_LIST = [
    r"showcase/loop_01_rule_04_random.png",
    r"showcase/loop_02_rule_02_random.png",
    r"showcase/loop_02_rule_04_random.png",
    r"showcase/loop_02_rule_07_single_seed.png",
    r"showcase/loop_03_rule_08_single_seed.png",

    r"showcase/loop_06_rule_01_random.png",
    r"showcase/loop_08_rule_01_random.png",
    r"showcase/loop_08_rule_02_random.png",
    r"showcase/loop_09_rule_08_single_seed.png",
    r"showcase/loop_10_rule_08_single_seed.png",

    r"showcase/loop_11_rule_03_random.png",
    r"showcase/loop_25_rule_08_random.png",
    r"showcase/loop_11_rule_05_random.png",
    r"showcase/loop_12_rule_02_single_seed.png",
    r"showcase/loop_12_rule_04_random.png",

    r"showcase/loop_13_rule_04_random.png",
    r"showcase/loop_13_rule_10_single_seed.png",
    r"showcase/loop_14_rule_03_single_seed.png",
    r"showcase/loop_14_rule_07_single_seed.png",
    r"showcase/loop_15_rule_09_random.png",

    r"showcase/loop_17_rule_09_single_seed.png",
    r"showcase/loop_20_rule_05_single_seed.png",
    r"showcase/loop_20_rule_06_single_seed.png",
    r"showcase/loop_22_rule_07_single_seed.png",
    r"showcase/loop_23_rule_07_single_seed.png",

    r"showcase/loop_23_rule_05_random.png",
    r"showcase/loop_24_rule_01_single_seed.png",
    r"showcase/loop_24_rule_02_single_seed.png",
    r"showcase/loop_24_rule_09_single_seed.png",
    r"showcase/loop_25_rule_01_single_seed.png",



]

def create_1x5_showcase():
    # Only keep images that can form full groups of 5
    num_full_groups = len(IMAGE_LIST) // 5
    total_images_to_use = num_full_groups * 5
    
    # Warn about discarded images
    discarded = len(IMAGE_LIST) - total_images_to_use
    if discarded > 0:
        print(f"WARNING: Discarding {discarded} remaining image(s) as they cannot make up a full group of 5.")
        
    images_to_process = IMAGE_LIST[:total_images_to_use]
    frames = []
    
    print(f"Stitching {total_images_to_use} images into {num_full_groups} frames (1x5 layout)...")
    
    for g_idx in range(num_full_groups):
        # Create base canvas for this frame
        frame_canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), color=(0, 0, 0, 255))
        
        # Get the 5 images for this group
        group_images = images_to_process[g_idx * 5 : (g_idx + 1) * 5]
        
        for i_idx, img_path in enumerate(group_images):
            x_offset = i_idx * (IMAGE_W + PADDING)
            
            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGBA")
                img_resized = img.resize((IMAGE_W, IMAGE_H), Image.Resampling.LANCZOS)
                frame_canvas.paste(img_resized, (x_offset, 0), img_resized)
            else:
                # Black placeholder if path doesn't exist
                placeholder = Image.new("RGBA", (IMAGE_W, IMAGE_H), color=(0, 0, 0, 255))
                frame_canvas.paste(placeholder, (x_offset, 0))
                print(f"  WARNING: Image path not found, using black placeholder: {img_path}")
                
        frames.append(frame_canvas.convert("RGB"))
        
    if not frames:
        print("ERROR: No frames created. GIF compilation aborted.")
        return
        
    # Save the frames as an animated GIF
    frames[0].save(
        OUTPUT_GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=2000,  # 2.0 seconds per frame
        loop=0
    )
    print(f"SUCCESS: Animated 1x5 showcase GIF saved to: {OUTPUT_GIF_PATH}")
    
    # Copy to the artifact directory
    if os.path.exists(ARTIFACT_DIR):
        dest_artifact = os.path.join(ARTIFACT_DIR, OUTPUT_GIF_PATH)
        shutil.copy2(OUTPUT_GIF_PATH, dest_artifact)
        print(f"SUCCESS: Copied GIF to artifact folder: {dest_artifact}")

if __name__ == "__main__":
    create_1x5_showcase()
