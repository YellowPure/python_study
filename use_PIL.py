# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

from PIL import Image, ImageFilter, ImageFont, ImageDraw
import random
im = Image.open('loading_01.png')
print im.format, im.size, im.mode

# im.thumbnail((200, 100))
# im2 = im.filter(ImageFilter.BLUR)
# im2.save('thumb.jpg', 'JPEG')

# 随机字母
def rnChar():
    return chr(random.randint(65, 90))

# 随机颜色
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2
def rndColor2():
    return (random.randint(32, 127), random.randint(32 ,127), random.randint(32, 127))
    
width = 60 *4
height = 60
image = Image.new('RGB', (width, height), (255, 255,255))
font = ImageFont.truetype('Arial.ttf', 36)
draw = ImageDraw.Draw(image)

for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())

for t in range(4):
    draw.text((60*t + 10, 10), rnChar(), font=font, fill=rndColor2())

image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')