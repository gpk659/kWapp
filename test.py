from PIL import Image, ImageOps
import pytesseract

im = Image.open("Desktop/counter.jpg")
area = (223,21,394,75)
cropped_im = im.crop(area)
inverted = ImageOps.invert(cropped_im)

inverted.save('invNumber.png')
im1 = Image.open("invNumber.png")

text = pytesseract.image_to_string(cropped_im, config='-psm 6')
cropped_im.show()

print(text)
