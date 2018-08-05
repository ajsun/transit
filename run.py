import time
import os
import atexit
import ImageFont
import Image
import ImageDraw
from rgbmatrix import Adafruit_RGBmatrix
from feeds import get_display_info

RED = '#EE352E'
GREEN = '#00933C'
YELLOW = '#FCCC0A'
BLUE = '#0039A6'
WHITE = '#808080'
ORANGE = '#E67E22'
BLACK = '#000000'
PURPLE = '#B933AD'
LIGHT_GRAY = '#A7A9AC' # L
GRAY = '#808183' # SHUTTLE
LIGHT_GREEN = '#6CBE45' # G
BROWN = '#996633'
curr_path = os.path.dirname(os.path.abspath(__file__))
SMALL_FONT_PATH = os.path.join(curr_path, '4x6.pil')
FONT_PATH = os.path.join(curr_path, '5x8.pil')


COLOR_MAPPING = {
    "1": RED,
    "2": RED,
    "3": RED,
    "4": GREEN,
    "5": GREEN,
    "6": GREEN,
    "7": PURPLE,
    "A": BLUE,
    "C": BLUE,
    "E": BLUE,
    "N": YELLOW,
    "Q": YELLOW,
    "R": YELLOW,
    "W": YELLOW,
    "B": ORANGE,
    "D": ORANGE,
    "F": ORANGE,
    "M": ORANGE,
}

def draw_subway_row(matrix, route_color, route_number, direction, minutes, station, row_start):
    if not matrix:
        raise Exception('No adafruit matrix passed')
    if (type(route_number) != 'string'):
        route_number = str(route_number)
    if (type(minutes) != 'string'):
        minutes = str(minutes)
    font = ImageFont.load(FONT_PATH)
    small_font = ImageFont.load(SMALL_FONT_PATH)
    row_width = 64
    row_height = 8
    x = 0
    y = 0
    circle_d = 6
    circle_text_y_offset = 1
    circle_text_x_offset = 2
    text_offset = 45
    station_letters = 6


    image = Image.new('RGB', (row_width, row_height))
    draw = ImageDraw.Draw(image)

    # background
    draw.rectangle((x, y, row_width, row_height), fill=BLACK)
    # subway line
    draw.ellipse(((x, y), (x + circle_d, y + circle_d)), fill=route_color)
    draw.text((x + circle_text_x_offset, y + circle_text_y_offset), route_number, font=small_font, fill=WHITE)
    # information
    draw.text((8, y), direction, font=font, fill=WHITE)
    draw.text((50, y), 'min', font=font, fill=WHITE)

    if int(minutes) > 9:
        text_offset -= 5
        station_letters -= 1

    draw.text((14, y), station[:station_letters], font=font, fill=WHITE)
    draw.text((text_offset, y), minutes, font=font, fill=ORANGE)

    matrix.SetImage(image.im.id, x, row_start)


def run():
    if os.environ['env'] == 'dev':
        while True:
        try:
            display_info = get_display_info(10)
        except Exception as e:
            print e
            continue
        for i in range(12):
            print(matrix,
                            COLOR_MAPPING[display_info[top_i]['route']],
                            display_info[top_i]['route'],
                            display_info[top_i]['route_direction'],
                            display_info[top_i]['minutes'],
                            display_info[top_i]['stop_name'],
                            first_row_y)
            print(matrix,
                            COLOR_MAPPING[display_info[bot_i]['route']],
                            display_info[bot_i]['route'],
                            display_info[bot_i]['route_direction'],
                            display_info[bot_i]['minutes'],
                            display_info[bot_i]['stop_name'],
                            second_row_y)
            time.sleep(5.0)
            
    # Rows and chain length are both required parameters:
    matrix = Adafruit_RGBmatrix(16, 2)
    # matrix.SetPWMBits(8)
    def clearOnExit():
	    matrix.Clear()
    atexit.register(clearOnExit)

    row_width = 64
    row_height = 8
    fps = 20  # Scrolling speed (ish)
    first_row_y = 0
    second_row_y = 8

    while True:
        try:
            display_info = get_display_info(10)
        except Exception as e:
            print e
            continue
        top_i = 0
        bot_i = 1
        for i in range(12):
            draw_subway_row(matrix,
                            COLOR_MAPPING[display_info[top_i]['route']],
                            display_info[top_i]['route'],
                            display_info[top_i]['route_direction'],
                            display_info[top_i]['minutes'],
                            display_info[top_i]['stop_name'],
                            first_row_y)
            draw_subway_row(matrix,
                            COLOR_MAPPING[display_info[bot_i]['route']],
                            display_info[bot_i]['route'],
                            display_info[bot_i]['route_direction'],
                            display_info[bot_i]['minutes'],
                            display_info[bot_i]['stop_name'],
                            second_row_y)
            top_i += 2
            bot_i += 2
            if top_i >= len(display_info):
                top_i = 0
            if bot_i >= len(display_info):
                bot_i = 1
            time.sleep(5.0)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        raise e