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
NUM_FRAMES = 325 # Number of animation frames
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
            "preset": "Default/CA01 Canvas",
            "color": { "r": 106, "g": 127, "b": 168 },
            "deckled_edges": True,
            "paper_scale":  100
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
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_FLAT_OILY_2_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Oily 2",
    "size" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
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
    "color": { "r": 106, "g": 127, "b": 168}
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
    [106, 127, 168],
    [102, 123, 164],
    [99, 120, 160],
    [96, 117, 157],
    [93, 114, 153],
    [90, 111, 149],
    [87, 108, 146],
    [84, 105, 142],
    [81, 102, 138],
    [78, 99, 135],
    [75, 96, 131],
    [72, 93, 128],
    [69, 89, 124],
    [66, 86, 120],
    [63, 83, 117],
    [60, 80, 113],
    [57, 77, 109],
    [54, 74, 106],
    [51, 71, 102],
    [48, 68, 98],
    [45, 65, 95],
    [42, 62, 91],
    [39, 59, 88],
    [38, 58, 86],
    [37, 57, 85],
    [36, 56, 84],
    [35, 55, 83],
    [34, 54, 82],
    [33, 53, 81],
    [32, 52, 79],
    [31, 51, 78],
    [30, 50, 77],
    [29, 49, 76],
    [28, 48, 75],
    [27, 47, 74],
    [26, 46, 72],
    [25, 45, 71],
    [24, 44, 70],
    [23, 43, 69],
    [22, 42, 68],
    [21, 41, 67],
    [20, 40, 65],
    [19, 39, 64],
    [18, 38, 63],
    [17, 37, 62],
    [16, 36, 61],
    [16, 36, 60]
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
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT/2)))
    return points

# def generate_random_stroke_length() :
#     ...

def generate_color(frame_number) :
    return Color( COLORS_GRADIENT[ int(frame_number/5) ][0],
                  COLORS_GRADIENT[ int(frame_number/5) ][1],
                  COLORS_GRADIENT[ int(frame_number/5) ][2])

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
    initial_stroke_points = generate_random_points(20)

    for frame_index in range(NUM_FRAMES):
        frame_events = []

        # Add INIT_EVENTS in the first frame
        if frame_index == 0:
            frame_events += INIT_EVENTS

            # generate initial painting
            for (x, y) in initial_stroke_points:
                frame_events += [EVENT_FLAT_BRUSH]
                press_event = {
                    "event_type": "POINTER_PRESS",
                    "pos": {
                        "x": float(x),
                        "y": float(y)
                    }
                }
                frame_events.append(press_event)
                if y > CANVAS_HEIGHT/2 :
                    move_event = {
                        "event_type": "POINTER_MOVE",
                        "pos": {
                            "x": float(x),
                            "y": float(0)
                        }
                    }
                    release_event = move_event.copy()
                    release_event["event_type"] = "POINTER_RELEASE"
                else :
                    move_event = {
                        "event_type": "POINTER_MOVE",
                        "pos": {
                            "x": float(x),
                            "y": float(CANVAS_HEIGHT)
                        }
                    }
                    release_event = move_event.copy()
                    release_event["event_type"] = "POINTER_RELEASE"
                frame_events.append(move_event)
                frame_events.append(release_event)
        elif frame_index < 235:

            new_brush_event = EVENT_FILBERT_DRY_BRUSH.copy()
            frame_events += [new_brush_event]

            # update max number of strokes
            if frame_index > 150 :
                strokesNum = 30
            else :
                strokesNum = int(frame_index * 28 / 179 + 2)

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

                    if stroke.steps > 10 :
                        delete_stroke = True

                    # check current position for edges
                    if stroke.cur_pos.y <= 0 :
                        stroke.cur_pos = Point(stroke.cur_pos.x, 0)
                        delete_stroke = True
                    elif stroke.cur_pos.y >= CANVAS_HEIGHT/2 :
                        stroke.cur_pos = Point(stroke.cur_pos.x, CANVAS_HEIGHT/2)
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
            if len(current_strokes) < strokesNum :
                for i in range(strokesNum-len(current_strokes)) :
                    # id
                    new_id = strokeCount
                    strokeCount += 1

                    # positioning
                    (x, y) = generate_random_points(1)[0]
                    new_cur_pos = Point(x, y)
                    new_final_pos = Point(x, y)
                    new_stroke_speed = (CANVAS_HEIGHT/2 - y)/(frame_index/5)

                    # color
                    new_color = generate_color(frame_index)

                    # brush_size
                    brush_size = 200 - 180*(frame_index/235)

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