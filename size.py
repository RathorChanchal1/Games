from PIL import Image

# Resize red.gif
img = Image.open("red.gif")
img = img.resize((30, 60))  # width, height
img.save("pics/red.gif")

# Resize white.gif
img = Image.open("white.gif")
img = img.resize((50, 60))
img.save("pics/white.gif")



