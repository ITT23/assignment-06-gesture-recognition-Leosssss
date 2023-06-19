# $1 gesture recognizer
# APPENDIX A – $1 GESTURE RECOGNIZER: https://depts.washington.edu/acelab/proj/dollar/dollar.pdf

import math
import tkinter as tk

TITLE = "$1 Unistroke Recognizer"
LABEL_INIT = "Waiting to draw"
LABEL_START_DRAW = "Recording unistroke"
LABEL_RESULT = "Result"
BUTTON_TEXT = "Clear canvas"
BG_COLOR = "#ad33ff"
CANVAS_SIZE = 400

drawing_app = None

# Templates
# Raw points for the three example gestures. Quelle: https://github.com/sebaram/onedollar_python/blob/master/recognizer_demo.py#L18
circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201), (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264), (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267), (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255), (361, 253), (375, 253), (385, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248), (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204), (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122), (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108), (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105), (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119), (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125), (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129), (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130), (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133), (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162), (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166), (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160), (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156), (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (372, 147), (371, 145), (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115), (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98), (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87), (294, 87), (293, 87), (293, 87)]

templates = {
    'circle' : circlePoints,
    'square' : squarePoints,
    'triangle' : trianglePoints
}

# Step 1. Resample a points path into n evenly spaced points.    
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def path_length(points):
    d = 0
    for i in range(1, len(points)):
        d += distance(points[i - 2], points[i-1])
    return d

def resample(points, n):
    global path_length
    path_length = path_length(points) / (n - 1)
    d = 0
    new_points = [points[0]]

    for i in range(1, len(points)):
        d += distance(points[i - 1], points[i])

        if d >= path_length:
            qx = points[i - 1][0] + ((path_length - d) / distance(points[i - 1], points[i])) * (points[i][0] - points[i - 1][0])
            qy = points[i - 1][1] + ((path_length - d) / distance(points[i - 1], points[i])) * (points[i][1] - points[i - 1][1])
            new_points.append((qx, qy))
            points.insert(i, (qx, qy))
            d = 0

    return new_points

# Step 2. Rotate points so that their indicative angle is at 0°
def rotate_to_zero(points):
    centroid = calculate_centroid(points)
    theta = math.atan2(centroid[1] - points[0][1], centroid[0] - points[0][0])
    new_points = rotate_by(points, -theta)
    return new_points

def rotate_by(points, theta):
    centroid = calculate_centroid(points)
    new_points = []
    for point in points:
        qx = (point[0] - centroid[0]) * math.cos(theta) - (point[1] - centroid[1]) * math.sin(theta) + centroid[0]
        qy = (point[0] - centroid[0]) * math.sin(theta) + (point[1] - centroid[1]) * math.cos(theta) + centroid[1]
        new_points.append((qx, qy))
    return new_points

def calculate_centroid(points):
    num_points = len(points)
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)
    return sum_x / num_points, sum_y / num_points

# Step 3. Scale points so that the resulting bounding box will be of size^2 dimension; then translate points to the origin. BOUNDINGBOX returns a rectangle according to (minx, miny), (maxx, maxy). For gestures serving as templates, Steps 1-3 should be carried out once on the raw input points. For candidates, Steps 1-4 should be used just after the candidate is articulated. 
def scale_to_square(points, size):
    bounding_box = calculate_bounding_box(points)
    new_points = []
    for point in points:
        qx = point[0] * (size / bounding_box[2])
        qy = point[1] * (size / bounding_box[3])
        new_points.append((qx, qy))
    return new_points

def calculate_bounding_box(points):
    min_x = min(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)
    return min_x, min_y, max_x, max_y

def translate_to_origin(points):
    centroid = calculate_centroid(points)
    new_points = []
    for point in points:
        qx = point[0] - centroid[0]
        qy = point[1] - centroid[1]
        new_points.append((qx, qy))
    return new_points

# Step 4. Match points against a set of templates. The size variable on line 7 of RECOGNIZE refers to the size passed to SCALE-TOSQUARE in Step 3. The symbol ϕ equals ½(-1 + √5). We use θ=±45° and θ∆=2° on line 3 of RECOGNIZE. Due to using RESAMPLE, we can assume that A and B in PATH-DISTANCE contain the same number of points, i.e., |A|=|B|. 
def recognize(points, templates, size):
    best_distance = float("inf")
    best_template = None

    for template in templates:
        distance = distance_at_best_angle(points, template, -45, 45, 2)
        if distance < best_distance:
            best_distance = distance
            best_template = template

    score = 1 - best_distance / (0.5 * math.sqrt(size ** 2 + size ** 2))
    return best_template, score

def distance_at_best_angle(points, template, theta_a, theta_b, theta_delta):
    x1 = 0.5 * (-1 + math.sqrt(5)) * theta_a + (1 - 0.5 * (-1 + math.sqrt(5))) * theta_b
    f1 = distance_at_angle(points, template, x1)
    x2 = (1 - 0.5 * (-1 + math.sqrt(5))) * theta_a + 0.5 * (-1 + math.sqrt(5)) * theta_b
    f2 = distance_at_angle(points, template, x2)

    while abs(theta_b - theta_a) > theta_delta:
        if f1 < f2:
            theta_b = x2
            x2 = x1
            f2 = f1
            x1 = 0.5 * (-1 + math.sqrt(5)) * theta_a + (1 - 0.5 * (-1 + math.sqrt(5))) * theta_b
            f1 = distance_at_angle(points, template, x1)
        else:
            theta_a = x1
            x1 = x2
            f1 = f2
            x2 = (1 - 0.5 * (-1 + math.sqrt(5))) * theta_a + 0.5 * (-1 + math.sqrt(5)) * theta_b
            f2 = distance_at_angle(points, template, x2)

    return min(f1, f2)

def distance_at_angle(points, template, theta):
    new_points = rotate_by(points, theta)
    return path_distance(new_points, template)

def path_distance(points_a, points_b):
    distance_sum = 0
    num_points = len(points_a)
    for i in range(num_points):
        distance_sum += distance(points_a[i], points_b[i])
    return distance_sum / num_points

class DrawingApp:
    def __init__(self, root, callback=None):
        self.root = root
        root.configure(bg=BG_COLOR)
        self.root.title(TITLE)

        self.label_text = tk.StringVar()
        self.label_text.set(LABEL_INIT)
        self.label = tk.Label(self.root, textvariable=self.label_text, font=("Arial", 13, "bold"), bg=BG_COLOR, fg="white")
        self.label.pack(pady=10)
        
        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack()

        self.button = tk.Button(self.root, text=BUTTON_TEXT, command=self.clear_canvas)
        self.button.pack(side="top", pady=10)

        self.points = []
        self.drawing = False

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.callback = callback
        
    def update_callback(self):
        if self.callback:
            self.callback(self.drawing)

    def start_drawing(self, event):
        self.canvas.delete("all")
        self.points = []
        self.drawing = True
        self.label_text.set(LABEL_START_DRAW)
        self.update_callback()

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
            self.points.append((x,y))
            self.update_callback()

    def stop_drawing(self, event):
        self.drawing = False
        self.label_text.set(LABEL_RESULT)
        self.update_callback()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.label_text.set(LABEL_INIT)


def handle_drawing_update(drawing):
    if drawing:
        print("on drawing")
    else:
        print("stoped")
        points = getattr(drawing_app, 'points') 
        if(len(points)>0):
            resampled_points = resample(points, 30)
            rotated_points = rotate_to_zero(resampled_points)  
            scaled_points = scale_to_square(rotated_points, CANVAS_SIZE)
            transfered_points = translate_to_origin(scaled_points)
            print("HIER")
            best_result, score = recognize(transfered_points, templates, CANVAS_SIZE)
            print("best_result: "+best_result)
     
       
def main():
    global drawing_app
    root = tk.Tk()
    drawing_app = DrawingApp(root, callback=handle_drawing_update)
    # points = getattr(app, 'points')

    '''
    resampled_points = resample(points, 30)
    print("after: resampled_points")
    rotated_points = rotate_to_zero(resampled_points)  
    print("after rotated_points")
    scaled_points = scale_to_square(rotated_points, CANVAS_SIZE)
    print("after scaled_points")
    transfered_points = translate_to_origin(scaled_points)
    print("after transfered_points")
    best_result, score = recognize(transfered_points, templates, CANVAS_SIZE)
    print("best_result: "+best_result)
    '''
    root.mainloop()
    
if __name__ == "__main__":main()