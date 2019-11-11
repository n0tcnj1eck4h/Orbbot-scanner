try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw
import pytesseract

import os

import os
if not os.path.exists('cuts'):
    os.makedirs('cuts')

if not os.path.exists('names'):
    os.makedirs('names')

def ocr_core(image):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(image, config=r'--psm 12')
    return text

im = Image.open('Scorpion.jpg') #input
im = im.crop((im.size[0]/2-25+29,0,im.size[0]/2-30+400,im.size[1]))
draw = ImageDraw.Draw(im)

d = False
for y in range(im.height):
    b = im.getpixel((16,y))[1] / (sum(im.getpixel((16,y)))/3) #green
    #print(y, b)
    if b > 1.5: 
        im = im.crop((0,y-20,im.width,im.height))
        break
        #draw.line((0, y, im.width, y), fill=(100,100,255), width=1)
    else:
        d = True

d = True
cuts = []
for y in range(im.height): #slice users
    b = sum(im.getpixel((0,y)))/3
    if y+30 > im.height or y+25-60 < 0:
        continue
    if b < 100 and im.getpixel((0,y+30))[2] < 240:
        if not d:
            continue
        d = False
        #print(y, b)
        cuts.append(im.crop((55,y+25-60,im.width,y+25)))
        #draw.line((0, y+25, im.width, y+25), fill=(255,100,100), width=1)
    else:
        d = True
im.save('out.png')
n = 0
data = []
for cut in cuts: 
    name = cut.crop((0,0,170,cut.height))
    cut.save(r'cuts\{}.png'.format(n))
    name.save(r'names\{}.png'.format(ocr_core(name)))
    xp = pytesseract.image_to_string(cut.crop((185,0,cut.width,27)), config=r'--psm 8')
    print(ocr_core(name), xp)
    
    n+=1