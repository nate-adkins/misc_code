from PIL import Image

Image.MAX_IMAGE_PIXELS = None
img = Image.open("slopes.png").convert("L")
pixels = img.load()
width, height = img.size

for x in range(width):
    for y in range(height):
        gray = pixels[x, y]
        
        if gray < 56:
            pixels[x, y] = 5
        else:
            pixels[x, y] = 255

        

img.save("safe_slopes_20_degrees.png")
