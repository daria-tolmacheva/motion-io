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

    def __init__(self, _id, _cur_pos, _final_pos, _stroke_speed, _color, _size):
        self.id = _id
        self.cur_pos = _cur_pos
        self.final_pos = _final_pos
        self.stroke_speed = _stroke_speed
        self.color = _color
        self.brush_size = _size


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


# Brush for painting
EVENT_THICK_HAIRY_BRUSH = {
    "event_type": "SET_BRUSH",
    "tool": "OIL_AND_ACRYLIC",
    "preset": "Round/Thick Hairy",
    "size" : 200,
    "paint_type": "PAINT",
    "color": { "r": 106, "g": 127, "b": 168 }
}

# EVENT_SCATTER_TWO_BRUSH = {
#     "event_type": "SET_BRUSH",
#     "tool": "OIL_AND_ACRYLIC",
#     "preset": "Grunge/Scatter 2",
#     "size" : 200,
#     "water": 55,
#     "opacity": 4,
#     "paint_type": "PAINT",
#     "color": { "r": 26, "g": 48, "b": 89 }
# }

DARK_BLUE = Color(16, 36, 60) # { "r": 16, "g": 36, "b": 60 }
ORIGINAL_BLUE = Color(106, 127, 168) # { "r": 106, "g": 127, "b": 168 }

COLORS_GRADIENT = [
    [106, 127, 168],
    [104, 125, 165],
    [102, 123, 163],
    [100, 121, 160],
    [98, 119, 158],
    [96, 117, 156],
    [94, 115, 153],
    [92, 113, 151],
    [90, 111, 149],
    [88, 109, 146],
    [86, 107, 144],
    [84, 105, 142],
    [82, 103, 139],
    [80, 101, 137],
    [78, 99, 135],
    [76, 97, 132],
    [74, 95, 130],
    [72, 93, 128],
    [70, 91, 125],
    [68, 89, 123],
    [66, 87, 121],
    [64, 85, 118],
    [62, 83, 116],
    [61, 81, 114],
    [59, 79, 111],
    [57, 77, 109],
    [55, 75, 106],
    [53, 73, 104],
    [51, 71, 102],
    [49, 69, 99],
    [47, 67, 97],
    [45, 65, 95],
    [43, 63, 92],
    [41, 61, 90],
    [39, 59, 88],
    [37, 57, 85],
    [35, 55, 83],
    [33, 53, 81],
    [31, 51, 78],
    [29, 49, 76],
    [27, 47, 74],
    [25, 45, 71],
    [23, 43, 69],
    [21, 41, 67],
    [19, 39, 64],
    [17, 37, 62],
    [16, 36, 59]
]


# Brush for erasing
EVENT_BRUSH_ERASER = EVENT_THICK_HAIRY_BRUSH.copy()
EVENT_BRUSH_ERASER["paint_type"] = "ERASE"
EVENT_BRUSH_ERASER["opacity"] = 100
EVENT_BRUSH_ERASER["size"] = 70



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
                frame_events += [EVENT_THICK_HAIRY_BRUSH]
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

            new_brush_event = EVENT_THICK_HAIRY_BRUSH.copy()
            frame_events += [new_brush_event]

            # update max number of strokes
            if frame_index > 150 :
                strokesNum = 20
            else :
                strokesNum = int (frame_index * 18 / 179 + 2)

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
                    new_stroke_speed = (CANVAS_HEIGHT/2 - y)/random.randint(10, 20)

                    # color
                    new_color = generate_color(frame_index)

                    # brush_size
                    brush_size = 200 - 180*(frame_index/235)

                    # add new stroke
                    current_strokes.append(Stroke(new_id, new_cur_pos, new_final_pos, new_stroke_speed, new_color, brush_size))




            # if pressed == False :
            #     rOffset = random.randint(-15, 15)
            #     gOffset = random.randint(-15, 15)
            #     bOffset = random.randint(-15, 15)
            #     current_color_event = {"event_type": "SET_BRUSH_COLOR", "color": {"r": int(BLUE["r"]+rOffset), "g": int(BLUE["g"]+gOffset), "b": int(BLUE["b"]+bOffset)}}
            #     frame_events += [current_color_event]
            #
            #     (x, y) = generate_random_points(1)[0]
            #     current_position[0] = x
            #     current_position[1] = y
            #     # stroke_speed = (CANVAS_HEIGHT - y)/10 if y > CANVAS_HEIGHT/2 else stroke_speed = (y - CANVAS_HEIGHT)/10
            #     stroke_speed = (CANVAS_HEIGHT - y)/5
            #     pressed = True
            #
            # press_event = {
            #     "event_type": "POINTER_PRESS",
            #     "pos": {
            #         "x": float(current_position[0]),
            #         "y": float(current_position[1])
            #     }
            # }
            # frame_events.append(press_event)
            #
            # current_position[1] += stroke_speed
            #
            # if current_position[1] <= 0 :
            #     move_event = {
            #         "event_type": "POINTER_MOVE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(0)
            #         }
            #     }
            #     release_event = {
            #         "event_type": "POINTER_RELEASE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(0)
            #         }
            #     }
            #     current_position[0] = 0
            #     current_position[1] = 0
            #     stroke_speed = 0
            #     pressed = False
            #     frame_events.append(move_event)
            #     frame_events.append(release_event)
            #
            # elif current_position[1] >= CANVAS_HEIGHT :
            #     move_event = {
            #         "event_type": "POINTER_MOVE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(CANVAS_HEIGHT)
            #         }
            #     }
            #     release_event = {
            #         "event_type": "POINTER_RELEASE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(CANVAS_HEIGHT)
            #         }
            #     }
            #     current_position[0] = 0
            #     current_position[1] = 0
            #     stroke_speed = 0
            #     pressed = False
            #     frame_events.append(move_event)
            #     frame_events.append(release_event)
            #
            # else :
            #     move_event = {
            #         "event_type": "POINTER_MOVE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(current_position[1])
            #         }
            #     }
            #     release_event = {
            #         "event_type": "POINTER_RELEASE",
            #         "pos": {
            #             "x": float(current_position[0]),
            #             "y": float(current_position[1])
            #         }
            #     }
            #     frame_events.append(move_event)
            #     frame_events.append(release_event)

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