from PIL import Image, ImageDraw
import numpy as np

# Load the cropped high-res image
crop = Image.open('assets/logo_raw_crop.png').convert('RGBA')
w, h = crop.size
print(f"Crop dimensions: {w}x{h}")

# The emblem is a circular medallion with saffron brush ring
# Let's find the circle center and radius
# We can create two versions:
# 1. assets/logo.png (the full artistic circular medallion with smooth transparent boundary)
# 2. assets/logo_badge.png (clean circle badge)

# Also let's inspect the user's uploaded image directly
user_img = Image.open(r'C:\Users\pooja\.gemini\antigravity-ide\brain\44e24a14-13ce-4428-91ad-5135c9fec645\.user_uploaded\media_1789977153880.png').convert('RGBA')
user_img.save('assets/user_logo_original.png')

# Now let's analyze the high-res crop to make a pristine circular logo with transparent background
# Let's inspect where the circle is:
# Center is approximately w/2, h/2
# Let's find the circular brush extent
crop_np = np.array(crop)
# Check non-dark pixels (dark background is almost black, around RGB < 30)
non_dark = np.any(crop_np[:, :, :3] > 40, axis=2)
y_indices, x_indices = np.where(non_dark)

if len(y_indices) > 0:
    min_x, max_x = x_indices.min(), x_indices.max()
    min_y, max_y = y_indices.min(), y_indices.max()
    print(f"Non-dark bounds: X=[{min_x}, {max_x}], Y=[{min_y}, {max_y}]")
    
    # Calculate circle center and radius to encompass the sun/medallion cleanly
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    radius = max((max_x - min_x), (max_y - min_y)) // 2 + 5
    print(f"Calculated circle: cx={cx}, cy={cy}, radius={radius}")

    # Create a smooth antialiased circular mask
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=255)
    
    # Also we can feather the outer edges or remove the dark background outside the circular brush
    # In the logo, outside the yellow brush halo is the dark navy/black background
    # Let's create an alpha channel where dark pixels outside the medallion fade to 0
    alpha = np.ones((h, w), dtype=np.uint8) * 255
    # Distance from center
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2)
    
    # Beyond radius, alpha is 0
    # Between radius - 15 and radius, smooth feathering
    feather_start = radius - 10
    outer_mask = dist_from_center > feather_start
    feather_factor = np.clip((radius - dist_from_center) / 10.0, 0, 1)
    
    # For pixels outside the central area, if brightness is low (the dark cover background), make them transparent
    brightness = np.mean(crop_np[:, :, :3], axis=2)
    dark_bg = brightness < 45
    
    # Combine masks
    final_alpha = np.ones((h, w), dtype=np.float32)
    final_alpha[dist_from_center > radius] = 0
    feather_zone = (dist_from_center >= feather_start) & (dist_from_center <= radius)
    final_alpha[feather_zone] = feather_factor[feather_zone]
    
    # Also fade dark background pixels outside core (radius > 160)
    outer_zone = dist_from_center > (radius * 0.75)
    fade_dark = outer_zone & (brightness < 60)
    final_alpha[fade_dark] = np.minimum(final_alpha[fade_dark], (brightness[fade_dark] / 60.0)**2)
    
    crop_np[:, :, 3] = (final_alpha * 255).astype(np.uint8)
    
    result = Image.fromarray(crop_np)
    # Crop to bounding box of content
    bbox = (cx - radius - 5, cy - radius - 5, cx + radius + 5, cy + radius + 5)
    result_cropped = result.crop(bbox)
    result_cropped.save('assets/logo.png')
    print("Saved assets/logo.png successfully! Size:", result_cropped.size)

    # Also make a square badge with circular border
    badge = Image.new('RGBA', (result_cropped.width, result_cropped.height), (0,0,0,0))
    badge.paste(result_cropped, (0, 0))
    badge.save('assets/logo_clean.png')
