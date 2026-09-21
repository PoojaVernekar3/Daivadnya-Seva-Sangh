from PIL import Image
import numpy as np

# Let's inspect logo_uploaded.png
img_user = Image.open('assets/logo_uploaded.png')
print("Uploaded logo size:", img_user.size)

# The user uploaded image directly is:
# C:\Users\pooja\.gemini\antigravity-ide\brain\44e24a14-13ce-4428-91ad-5135c9fec645\.user_uploaded\media_1789977153880.png
# Let's also check if we can make a beautiful clean version of the uploaded image
# In the uploaded image:
# It's an orange circular badge with yellow brush strokes, Ganesh calligraphy, on a dark night/diya background.
# We can use the uploaded image directly or enhance it.
# Let's inspect its alpha channel or border.
arr = np.array(img_user)
print("Uploaded image shape:", arr.shape)
print("Has alpha?", arr.shape[2] == 4)

# Let's save a pristine version of the user's uploaded logo to assets/logo.png
img_user.save('assets/logo.png')
print("Saved assets/logo.png from user's uploaded image directly!")
