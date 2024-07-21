from collections import namedtuple
import random
import json
import sys
from dataclasses import dataclass
from shapely.geometry import Point

@dataclass
class Color:
    r: float
    g: float
    b: float

    def __init__(self, _r, _g, _b):
        self.r = _r
        self.g = _g
        self.b = _b

@dataclass
class Stroke:
    id: int
    cur_pos: Point
    final_pos: Point
    stroke_speed: float
    color: Color
    brush_size : float
    steps : int

    def __init__(self, _id, _cur_pos, _final_pos, _stroke_speed, _color, _size, _steps):
        self.id = _id
        self.cur_pos = _cur_pos
        self.final_pos = _final_pos
        self.stroke_speed = _stroke_speed
        self.color = _color
        self.brush_size = _size
        self.steps = _steps


BBox = namedtuple('BBox', ['x', 'y', 'w', 'h'])

#--------------------------------------------------
# Parameters for the animation
#--------------------------------------------------
NUM_FRAMES = 795 # Number of animation frames
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

INIT_EVENTS = [
    {
        # As in Rebelle's "File -> New Artwork..."
        "event_type": "NEW_ARTWORK",
        "width": CANVAS_WIDTH,
        "height": CANVAS_HEIGHT,
        "units": "px",
        "dpi": 350,
        "paper": {
            "preset": "Default/WK01 Washi",
            "color": { "r": 255, "g": 255, "b": 255 },
            "deckled_edges": False,
            "paper_scale":  40
        }
    },
    {
        "event_type": "SET_ENGINE_PARAMS",
        "absorbency": 5,
        "re_wet": 5,
        "texture_influence": 5,
        "edge_darkening": 5,
        "create_drips": True,
        "drip_size": 5,
        "drip_length": 5,
        "impasto_depth": 6,
        "gloss": 5,
        "paper_texture": 8,
        "paint_texture": 5,
        "gran_enabled": True,
        "gran_strength": 5,
        "gran_contrast": 5,
        "gran_texture": 2
    },
    {
        # Tilt Panel
        "event_type": "SET_CANVAS_TILT",
        "tilt": {
            "x": 0,
            "y": 1
        },
        "enabled": 1
    },
]


# Brushs for painting
# EVENT_THICK_HAIRY_BRUSH = {
#     "event_type": "SET_BRUSH",
#     "tool": "OIL_AND_ACRYLIC",
#     "preset": "Round/Thick Hairy",
#     "size" : 200,
#     "paint_type": "PAINT",
#     "color": { "r": 106, "g": 127, "b": 168}
# }

EVENT_FLAT_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 132, "g": 151, "b": 224}
}

EVENT_FLAT_OILY_2_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Oily 2",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 132, "g": 151, "b": 224}
}

EVENT_FLAT_DRY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Dry",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_FLAT_DRY_2_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Dry 2",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_FILBERT_DRY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Filbert Dry",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 133, "g": 152, "b": 226}
}

EVENT_RAKE_OILY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Rake/Rake Oily",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_RAKE_SHARP_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Rake/Rake Sharp",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

DARK_BLUE = Color(16, 36, 60) # { "r": 16, "g": 36, "b": 60 }
ORIGINAL_BLUE = Color(106, 127, 168) # { "r": 106, "g": 127, "b": 168 }

COLORS_GRADIENT = [
    [132, 151, 224],
    [131, 150, 222],
    [130, 149, 221],
    [129, 148, 220],
    [128, 147, 219],
    [127, 146, 217],
    [126, 145, 216],
    [125, 144, 215],
    [125, 143, 214],
    [124, 142, 212],
    [123, 141, 211],
    [122, 140, 210],
    [121, 139, 209],
    [120, 138, 207],
    [119, 137, 206],
    [118, 136, 205],
    [118, 135, 204],
    [117, 134, 202],
    [116, 133, 201],
    [115, 132, 200],
    [114, 131, 199],
    [113, 130, 197],
    [112, 129, 196],
    [111, 128, 195],
    [111, 127, 194],
    [110, 126, 192],
    [109, 125, 191],
    [108, 124, 190],
    [107, 123, 189],
    [106, 122, 187],
    [105, 121, 186],
    [104, 120, 185],
    [104, 119, 184],
    [103, 118, 182],
    [102, 117, 181],
    [101, 116, 180],
    [100, 115, 179],
    [99, 114, 177],
    [98, 113, 176],
    [98, 113, 175],
    [97, 112, 174],
    [96, 111, 173],
    [95, 110, 171],
    [94, 109, 170],
    [93, 108, 169],
    [92, 107, 168],
    [91, 106, 166],
    [91, 105, 165],
    [90, 104, 164],
    [89, 103, 163],
    [88, 102, 161],
    [87, 101, 160],
    [86, 100, 159],
    [85, 99, 158],
    [84, 98, 156],
    [84, 97, 155],
    [83, 96, 154],
    [82, 95, 153],
    [81, 94, 151],
    [80, 93, 150],
    [79, 92, 149],
    [78, 91, 148],
    [77, 90, 146],
    [77, 89, 145],
    [76, 88, 144],
    [75, 87, 143],
    [74, 86, 141],
    [73, 85, 140],
    [72, 84, 139],
    [71, 83, 138],
    [70, 82, 136],
    [70, 81, 135],
    [69, 80, 134],
    [68, 79, 133],
    [67, 78, 131],
    [66, 77, 130],
    [65, 76, 129],
    [64, 75, 128],
    [64, 75, 127],
    [63, 74, 126],
    [63, 73, 125],
    [62, 73, 125],
    [62, 72, 124],
    [61, 72, 123],
    [61, 71, 123],
    [60, 71, 122],
    [60, 70, 121],
    [59, 70, 121],
    [59, 69, 120],
    [58, 69, 119],
    [58, 68, 119],
    [57, 68, 118],
    [57, 67, 117],
    [56, 66, 116],
    [56, 66, 115],
    [55, 65, 115],
    [55, 65, 114],
    [54, 64, 113],
    [54, 63, 113],
    [53, 63, 112],
    [53, 62, 111],
    [52, 62, 111],
    [52, 61, 110],
    [51, 61, 109],
    [51, 60, 109],
    [51, 60, 108],
    [50, 59, 107],
    [49, 58, 106],
    [49, 58, 105],
    [48, 57, 105],
    [48, 57, 104],
    [47, 56, 103],
    [46, 55, 102],
    [46, 55, 101],
    [45, 54, 101],
    [45, 54, 100],
    [45, 53, 99],
    [44, 52, 99],
    [44, 52, 98],
    [43, 51, 97],
    [42, 50, 96],
    [42, 50, 95],
    [41, 49, 95],
    [41, 49, 94],
    [40, 48, 93],
    [39, 47, 92],
    [39, 47, 91],
    [39, 46, 91],
    [38, 46, 90],
    [38, 45, 89],
    [37, 45, 89],
    [37, 44, 88],
    [36, 44, 87],
    [36, 43, 87],
    [35, 42, 86],
    [35, 42, 85],
    [34, 41, 85],
    [34, 41, 84],
    [33, 40, 83],
    [33, 39, 82],
    [32, 39, 81],
    [32, 38, 81],
    [31, 38, 80],
    [31, 37, 79],
    [30, 37, 79],
    [30, 36, 78],
    [29, 36, 77],
    [29, 35, 77],
    [28, 35, 76],
    [28, 34, 75],
    [27, 34, 75],
    [27, 33, 74]
]


# Brush for erasing
# EVENT_BRUSH_ERASER = EVENT_FLAT_BRUSH.copy()
# EVENT_BRUSH_ERASER["paint_type"] = "ERASE"
# EVENT_BRUSH_ERASER["opacity"] = 100
# EVENT_BRUSH_ERASER["size"] = 70



#--------------------------------------------------
# Helper functions
#--------------------------------------------------
def generate_random_points(number) :
    points = []
    for _ in range(number) :
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(0, 2*CANVAS_HEIGHT/3)))
    return points

def generate_random_init_points(number) :
    points = []
    for _ in range(number) :
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(9*CANVAS_HEIGHT/10, CANVAS_HEIGHT)))
    return points

# def generate_random_stroke_length() :
#     ...

def generate_color(frame_number) :
    rOffset = random.randint(-5, 5)
    gOffset = random.randint(-2, 2)
    bOffset = random.randint(-2, 2)
    return Color( COLORS_GRADIENT[ int(frame_number/5) ][0] + rOffset,
                  COLORS_GRADIENT[ int(frame_number/5) ][1] + gOffset,
                  COLORS_GRADIENT[ int(frame_number/5) ][2] + bOffset)

def create_press_event(stroke) :
    press_event = {
        "event_type": "POINTER_PRESS",
        "stroke_id": stroke.id,
        "pos": {
            "x": stroke.cur_pos.x,
            "y": stroke.cur_pos.y
        }
        # extra bits
        # "pen_tilt": {   # pen tilt in relation to drawing tablet’s x and y axis in degrees, optional
        #     "x": 60,
        #     "y": -45
        # },
        # "rotation": 45.0,   # pen rotation in degrees, optional
        # "pressure": 0.6 # pen pressure, 0.0-1.0, optional
        }
    return press_event

def create_move_event(stroke) :
    move_event = {
        "event_type": "POINTER_MOVE",
        "stroke_id": stroke.id,
        "pos": {
            "x": stroke.cur_pos.x,
            "y": stroke.cur_pos.y
        }
        # extra bits
        # "pen_tilt": {   # pen tilt in relation to drawing tablet’s x and y axis in degrees, optional
        #     "x": 60,
        #     "y": -45
        # },
        # "rotation": 45.0,   # pen rotation in degrees, optional
        # "pressure": 0.6 # pen pressure, 0.0-1.0, optional
    }
    return move_event

def create_release_event(stroke) :
    release_event = {
        "event_type": "POINTER_RELEASE",
        "stroke_id": stroke.id,
        "pos": {
            "x": stroke.cur_pos.x,
            "y": stroke.cur_pos.y
        }
        # extra bits
        # "pen_tilt": {   # pen tilt in relation to drawing tablet’s x and y axis in degrees, optional
        #     "x": 60,
        #     "y": -45
        # },
        # "rotation": 45.0,   # pen rotation in degrees, optional
        # "pressure": 0.6 # pen pressure, 0.0-1.0, optional
    }
    return release_event

def create_color_event(stroke) :
    color_event = {
        "event_type": "SET_BRUSH_COLOR",
        "color": {"r": stroke.color.r, "g": stroke.color.g, "b": stroke.color.b}
    }
    return color_event

def create_change_brush_size_event(stroke) :
    brush_size_event = {
        "event_type": "SET_BRUSH_PARAMS",
        "size": stroke.brush_size
    }
    return brush_size_event

#--------------------------------------------------
# Main part
#--------------------------------------------------
# Generate JSON object
def generate_animation():
    frames = []
    # pressed = False
    # current_position = [0, 0]
    # stroke_speed = 0
    current_color_event = { "r": 11, "g": 24, "b": 56 }
    current_strokes = []
    strokesNum = 2
    strokeCount = 0

    # Points along the SVG path
    initial_stroke_points = generate_random_init_points(50)

    for frame_index in range(NUM_FRAMES):
        frame_events = []

        # Add INIT_EVENTS in the first frame
        if frame_index == 0:
            frame_events += INIT_EVENTS

            frame_events += [EVENT_FILBERT_DRY_BRUSH]
            brush_size_event = {
                "event_type": "SET_BRUSH_PARAMS",
                "size": 500
            }
            frame_events += brush_size_event

            # generate initial painting
            for (x, y) in initial_stroke_points:

                # frame_events += [EVENT_FILBERT_DRY_BRUSH]
                # brush_size_event = {
                #     "event_type": "SET_BRUSH_PARAMS",
                #     "size": 500
                # }
                # frame_events += brush_size_event

                press_event = {
                    "event_type": "POINTER_PRESS",
                    "pos": {
                        "x": float(x),
                        "y": float(y)
                    }
                }
                frame_events.append(press_event)

                move_event = {
                    "event_type": "POINTER_MOVE",
                    "pos": {
                        "x": float(x),
                        "y": float(0)
                    }
                }
                release_event = move_event.copy()
                release_event["event_type"] = "POINTER_RELEASE"

                frame_events.append(move_event)
                frame_events.append(release_event)
        else :

            new_brush_event = EVENT_FILBERT_DRY_BRUSH.copy()
            frame_events += [new_brush_event]

            # update max number of strokes
            if frame_index > 620 :
                strokesNum = 50
            else :
                strokesNum = int(frame_index * 48 / 649 + 2)

            if len(current_strokes) > 0 :
                for stroke in current_strokes :
                    delete_stroke = False

                    # set color
                    color_event = create_color_event(stroke)
                    frame_events.append(color_event)
                    # set brush size
                    brush_size_event = create_change_brush_size_event(stroke)
                    frame_events.append(brush_size_event)
                    #set current position
                    press_event = create_press_event(stroke)
                    frame_events.append(press_event)

                    # update current stroke
                    # update current position
                    stroke.cur_pos = Point(stroke.cur_pos.x, stroke.cur_pos.y + stroke.stroke_speed)
                    stroke.steps = stroke.steps + 1

                    if stroke.steps > 20 :
                        delete_stroke = True

                    # check current position for edges
                    if stroke.cur_pos.y <= 0 :
                        stroke.cur_pos = Point(stroke.cur_pos.x, 0)
                        delete_stroke = True
                    elif stroke.cur_pos.y >= CANVAS_HEIGHT :
                        stroke.cur_pos = Point(stroke.cur_pos.x, CANVAS_HEIGHT)
                        delete_stroke = True

                    # format events
                    move_event = create_move_event(stroke)
                    release_event = create_release_event(stroke)

                    # add events to instructions
                    frame_events.append(move_event)
                    frame_events.append(release_event)

                    if delete_stroke == True :
                        current_strokes.remove(stroke)


            # generate new stroke(s)
            if len(current_strokes) < strokesNum  and  frame_index < 705 :
                for i in range(strokesNum-len(current_strokes)) :
                    # id
                    new_id = strokeCount
                    strokeCount += 1

                    # positioning
                    (x, y) = generate_random_points(1)[0]
                    new_cur_pos = Point(x, y)
                    new_final_pos = Point(x, y)
                    new_stroke_speed = (CANVAS_HEIGHT - y)/(frame_index/5)

                    # color
                    new_color = generate_color(frame_index)

                    # brush_size
                    brush_size = 200 - 100*(frame_index/705)

                    # add new stroke
                    current_strokes.append(Stroke(new_id, new_cur_pos, new_final_pos, new_stroke_speed, new_color, brush_size, 0))

        # Add a few simulation steps
        frame_events += [{"event_type": "SIMULATION", "repeats": 6}]

        # Add the events to the frame
        frame = {"events": frame_events}
        frames.append(frame)

    return {"frames": frames}


# Generate the animation
animation = generate_animation()

# Save the animation to a JSON file
output_file = sys.argv[1]
with open(output_file+".json", "w") as json_file:
    json.dump(animation, json_file, indent=4)