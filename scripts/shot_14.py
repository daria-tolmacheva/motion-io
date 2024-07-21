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
NUM_FRAMES = 100 # Number of animation frames
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

COLORS_GRADIENT = [
    [171, 100, 116],
    [173, 100, 115],
    [175, 100, 115],
    [178, 100, 114],
    [180, 100, 114],
    [183, 100, 114],
    [185, 100, 113],
    [188, 100, 113],
    [190, 100, 112],
    [193, 100, 112],
    [195, 100, 112],
    [198, 100, 111],
    [200, 100, 111],
    [203, 100, 110],
    [205, 100, 110],
    [208, 101, 110],
    [208, 102, 110],
    [209, 103, 110],
    [209, 104, 111],
    [210, 105, 111],
    [210, 106, 111],
    [211, 107, 111],
    [211, 108, 112],
    [212, 109, 112],
    [212, 110, 113],
    [213, 111, 113],
    [213, 112, 113],
    [214, 113, 113],
    [214, 114, 114],
    [215, 115, 114],
    [215, 116, 114],
    [216, 117, 115],
    [217, 121, 119],
    [219, 125, 124],
    [221, 129, 128],
    [223, 134, 133],
    [224, 138, 137],
    [226, 142, 142],
    [228, 146, 146],
    [230, 151, 151],
    [232, 155, 155],
    [233, 159, 160],
    [235, 164, 164],
    [237, 168, 169],
    [239, 172, 173],
    [240, 176, 178],
    [242, 181, 182],
    [244, 185, 187],
    [246, 189, 191],
    [248, 194, 196]
]


EVENT_FLAT_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 132, "g": 151, "b": 224}
}

EVENT_FLAT_OILY_2_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Oily 2",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 132, "g": 151, "b": 224}
}

EVENT_FLAT_DRY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Dry",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_FLAT_DRY_2_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Flat Dry 2",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_FILBERT_DRY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Flat/Filbert Dry",
    "size_px" : 600,
    "paint_type": "PAINT_BLEND",
    "color": { "r": 133, "g": 152, "b": 226}
}

EVENT_RAKE_OILY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Rake/Rake Oily",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

EVENT_RAKE_SHARP_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Rake/Rake Sharp",
    "size_px" : 200,
    "paint_type": "PAINT_MIX",
    "color": { "r": 106, "g": 127, "b": 168}
}

DARK_BLUE = Color(16, 36, 60) # { "r": 16, "g": 36, "b": 60 }
ORIGINAL_BLUE = Color(106, 127, 168) # { "r": 106, "g": 127, "b": 168 }


#--------------------------------------------------
# Helper functions
#--------------------------------------------------
def generate_random_points(number, frame) :
    points = []
    for _ in range(number) :
        points.append((random.randint(int(0.4*frame+400), int(0.4*frame+860)), random.randint(CANVAS_HEIGHT - 10, CANVAS_HEIGHT)))
    return points

def generate_random_init_points(number) :
    points = []
    for _ in range(number) :
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(2*CANVAS_HEIGHT/3, CANVAS_HEIGHT)))
    return points

# def generate_random_stroke_length() :
#     ...

def generate_color(frame_number) :
    rOffset = random.randint(-3, 3)
    gOffset = random.randint(-3, 3)
    bOffset = random.randint(-3, 3)
    return Color( COLORS_GRADIENT[ int((frame_number)/2) ][0] + rOffset,
                  COLORS_GRADIENT[ int((frame_number)/2) ][1] + gOffset,
                  COLORS_GRADIENT[ int((frame_number)/2) ][2] + bOffset)

def generate_color_event(num_of_options) :
    new_color = generate_color(num_of_options)
    color_event = {
        "event_type": "SET_BRUSH_COLOR",
        "color": {"r": new_color.r, "g": new_color.g, "b": new_color.b}
    }
    return color_event

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
        "size_px": stroke.brush_size
    }
    return brush_size_event

#--------------------------------------------------
# Main part
#--------------------------------------------------
# Generate JSON object
def generate_animation():
    frames = []
    current_strokes = []
    strokesNum = 2
    strokeCount = 0


    for frame_index in range(NUM_FRAMES):
        frame_events = []

        # Add INIT_EVENTS in the first frame
        if frame_index == 0:
            frame_events += INIT_EVENTS
        else :


            # update max number of strokes
            strokesNum = int(frame_index * 0.07 + 2.929)

            if len(current_strokes) > 0 :
                for stroke in current_strokes :
                    delete_stroke = False

                    # set color
                    # color_event = create_color_event(stroke)
                    # frame_events.append(color_event)
                    # set brush size
                    # brush_size_event = create_change_brush_size_event(stroke)
                    # frame_events.append(brush_size_event)

                    new_brush_event = EVENT_FILBERT_DRY_BRUSH.copy()
                    new_color = generate_color(frame_index)
                    new_brush_event["color"] = {"r": new_color.r, "g": new_color.g, "b": new_color.b }
                    new_brush_event["size_px"] = stroke.brush_size
                    frame_events += [new_brush_event]

                    #set current position
                    press_event = create_press_event(stroke)
                    frame_events.append(press_event)

                    # update current stroke
                    # update current position
                    stroke.cur_pos = Point(stroke.cur_pos.x, stroke.cur_pos.y - stroke.stroke_speed)
                    stroke.steps = stroke.steps + 1

                    if stroke.steps > 4 :
                        delete_stroke = True

                    # check current position for edges
                    if stroke.cur_pos.y <= 300 :
                        stroke.cur_pos = Point(stroke.cur_pos.x, random.randint(290, 320))
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
                    (x, y) = generate_random_points(1, frame_index)[0]
                    new_cur_pos = Point(x, y)
                    new_final_pos = Point(x, y)
                    new_stroke_speed = (y - 0)/random.randint(5, 10)

                    # color
                    new_color = generate_color(frame_index)

                    # brush_size
                    brush_size = 700 - 550*(frame_index/NUM_FRAMES)

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