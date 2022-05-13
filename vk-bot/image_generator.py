from PIL import Image, ImageDraw


def generate_image(occupied_time):
    base = Image.open("vk-bot/img/time_base.png")
    drawer = ImageDraw.Draw(base)
    
    for time in occupied_time:
        shape = [(49 + time[0] * 24, 176), (49 + time[1] * 24, 237)]
        drawer.rectangle(shape, fill='#b02b2b')
    
    base.save('vk-bot/img/time.png')
