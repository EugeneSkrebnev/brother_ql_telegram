from PIL import Image, ImageDraw, ImageFont


def image_with_696_width_from_path(image_path):
    img = Image.open(image_path)
    w, h = img.size
    size = (696, int(h / w * 696))
    res = img.resize(size)
    return res


def image_with_text_from_path(image_path, text):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/times-ro.ttf", 20)
    draw.text((0, 0), text, (255, 255, 255), font=font)
    return img
