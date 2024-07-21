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
NUM_FRAMES = 340 # Number of animation frames
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
    [132, 151, 224],
    [126, 145, 216],
    [129, 148, 220],
    [127, 146, 217],
    [129, 148, 220],
    [132, 151, 224],
    [193, 159, 172],
    [149, 138, 161],
    [193, 159, 172],
    [149, 138, 161],
    [193, 159, 172],
    [149, 138, 161]
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
    "size_px" : 200,
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
    "size_px" : 600,
    "paint_type": "PAINT_BLEND",
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


#--------------------------------------------------
# Helper functions
#--------------------------------------------------
def generate_random_points(number) :
    points = []
    for _ in range(number) :
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT/3)))
    return points

def generate_random_init_points(number) :
    points = []
    for _ in range(number) :
        points.append((random.randint(0, CANVAS_WIDTH), random.randint(2*CANVAS_HEIGHT/3, CANVAS_HEIGHT)))
    return points

# def generate_random_stroke_length() :
#     ...

def generate_color(num_of_options) :
    rOffset = random.randint(-10, 10)
    gOffset = random.randint(-3, 3)
    bOffset = random.randint(-3, 3)
    color = COLORS_GRADIENT[ random.randint(0, num_of_options) ]
    return Color( color[0] + rOffset,
                  color[1] + gOffset,
                  color[2] + bOffset)

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
    initial_stroke_points = generate_random_init_points(20)
    initial_stroke_points_texture = generate_random_init_points(30)

    for frame_index in range(NUM_FRAMES):
        frame_events = []

        # Add INIT_EVENTS in the first frame
        if frame_index == 0:
            frame_events += INIT_EVENTS

            # frame_events += [EVENT_FILBERT_DRY_BRUSH]


            # generate initial painting
            for (x, y) in initial_stroke_points:

                # color_event = generate_color_event(6)
                # frame_events += [color_event]

                # brush_size_event = {
                #     "event_type": "SET_BRUSH_PARAMS",
                #     "size": 400
                # }
                # frame_events += [brush_size_event]

                new_color = generate_color(11)
                new_brush_event = EVENT_FILBERT_DRY_BRUSH.copy()
                new_brush_event["color"] = {"r": new_color.r, "g": new_color.g, "b": new_color.b }
                new_brush_event["size_pxs"] = 1300
                frame_events += [new_brush_event]

                press_event = {
                    "event_type": "POINTER_PRESS",
                    "pos": {
                        "x": float(x),
                        "y": float(CANVAS_HEIGHT)
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

        elif frame_index == 1:
            for (x, y) in initial_stroke_points_texture:

                new_color = generate_color(11)
                new_brush_event = EVENT_FILBERT_DRY_BRUSH.copy()
                new_brush_event["color"] = {"r": new_color.r, "g": new_color.g, "b": new_color.b }
                new_brush_event["size_px"] = 600
                frame_events += [new_brush_event]

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
            strokesNum = 2

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

                    # if stroke.steps > 20 :
                    #     delete_stroke = True

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
            if len(current_strokes) < strokesNum :
                for i in range(strokesNum-len(current_strokes)) :
                    # id
                    new_id = strokeCount
                    strokeCount += 1

                    # positioning
                    (x, y) = generate_random_points(1)[0]
                    new_cur_pos = Point(x, y)
                    new_final_pos = Point(x, y)
                    new_stroke_speed = (CANVAS_HEIGHT - y)/random.randint(10, 25)

                    # color
                    new_color = generate_color(5)

                    # brush_size
                    brush_size = random.randint(600, 1200)

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