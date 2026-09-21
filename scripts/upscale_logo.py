from PIL import Image, ImageFilter

im = Image.open('assets/logo_circle.png')
# Upscale to 320x320 using Lanczos
upscaled = im.resize((320, 320), Image.Resampling.LANCZOS)
# Gentle unsharp mask for crystal crisp Marathi typography
crisp = upscaled.filter(ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=3))
crisp.save('assets/logo.png')
print("Enhanced assets/logo.png saved at 320x320!")
