# $1 gesture recognizer
# APPENDIX A – $1 GESTURE RECOGNIZER: https://depts.washington.edu/acelab/proj/dollar/dollar.pdf

import math
import tkinter as tk

# Templates
# Raw points for the three example gestures. Quelle: https://github.com/sebaram/onedollar_python/blob/master/recognizer_demo.py#L18
circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142), (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212), (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226), (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217), (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158), (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121), (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109), (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107), (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105), (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101), (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201), (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264), (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267), (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255), (361, 253), (375, 253), (385, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248), (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204), (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122), (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108), (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105), (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119), (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125), (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129), (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130), (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133), (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162), (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166), (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160), (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156), (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (372, 147), (371, 145), (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115), (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98), (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87), (294, 87), (293, 87), (293, 87)]
SPoints = [(-108.2048359740283, 5.684341886080802e-14), (-105.8271462602467, 13.393322143501848), (-104.36316619430576, 24.626996011529286), (-100.83145244240478, 32.370281719118395), (-97.09338061892768, 42.67685540626002), (-94.28510165340401, 50.050756053836324), (-89.07649904939186, 57.33428666136342), (-83.46694717451754, 66.2681035198724), (-80.57226977793124, 73.56827679924902), (-73.50124523359548, 83.0917140188231), (-67.63596632775489, 94.15465347824284), (-60.94944663014499, 106.70527339551052), (-54.51438878597935, 117.64514789810454), (-45.31677977543319, 129.94665255804534), (-37.00956512777361, 134.741666804025), (-26.31242036112357, 139.96787832420023), (-14.579544304978015, 141.05509036738442), (-2.3260410275221943, 142.6730249965833), (10.037994271998684, 140.61642179201857), (18.215210875652645, 136.1800457644411), (27.381540780583066, 125.83751957006194), (35.85538479632339, 112.8409521122939), (44.32922881206372, 99.84438465452581), (49.98898959095021, 86.67784748375487), (52.21654117976385, 71.9218622193792), (52.4638589730705, 58.41688367969442), (50.60996507177822, 42.56481315110483), (46.40516136236448, 29.485828081877344), (39.067324079605726, 17.365413539340864), (31.545860901725234, 5.082035050075433), (22.432852603612332, -4.851075670367152), (16.210164025471784, -17.703284469297586), (9.792447173927258, -31.91970865525451), (5.116230507947307, -43.65145778626419), (0.9734111749374961, -56.7604468817938), (-2.226745366402554, -69.4399796234091), (-5.5661752019768755, -83.8919430689694), (-4.014545615754059, -99.76676802632628), (0.5782589573889823, -114.96951622662561), (6.653857128210916, -126.58901057608347), (14.255399065378072, -141.12685048957002), (23.18040647969889, -148.31249024825965), (33.314467280947156, -156.541165978859), (44.34877009139399, -165.07400650803922), (57.023830040397286, -168.35872087346814), (69.00927648817748, -167.910082322654), (79.90220840116154, -166.98469795512375), (89.68808177523476, -161.1344136512151), (99.157022095662, -157.98659230977455), (108.27167556374673, -150.23942539989008), (119.6482433544208, -143.89235053297054)]
VPoints = [(-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498524, -4.547473508864641e-13), (-11.799410029498517, -3.979039320256561e-13), (-11.799410029498517, -4.547473508864641e-13), (-11.79941002949851, -3.979039320256561e-13), (-11.799410029498503, -4.547473508864641e-13), (-11.799410029498475, -4.547473508864641e-13), (-11.799410029498429, -4.547473508864641e-13), (-11.799410029498336, -4.547473508864641e-13), (-11.799410029498151, -4.547473508864641e-13), (-11.799410029497782, -4.547473508864641e-13), (-11.799410029497036, -4.547473508864641e-13), (-11.799410029495547, -4.547473508864641e-13), (-11.799410029492574, -4.547473508864641e-13), (-11.79941002948662, -4.547473508864641e-13), (-11.799410029474714, -4.547473508864641e-13), (-11.799410029450904, -4.547473508864641e-13), (-11.79941002940328, -3.979039320256561e-13), (-11.799410029308039, -4.547473508864641e-13), (-11.799410029117556, -4.547473508864641e-13), (-11.799410028736588, -4.547473508864641e-13), (-11.799410027974652, -4.547473508864641e-13), (-11.799410026450776, -4.547473508864641e-13), (-11.79941002340303, -3.979039320256561e-13), (-11.79941001730754, -4.547473508864641e-13), (-11.799410005116552, -4.547473508864641e-13), (-11.799409980734584, -4.547473508864641e-13), (-11.799409931970644, -4.547473508864641e-13), (-11.799409834442763, -4.547473508864641e-13), (-11.799409639387004, -4.547473508864641e-13), (-11.799409249275481, -4.547473508864641e-13), (-11.799408469052441, -4.547473508864641e-13), (-11.799406908606358, -4.547473508864641e-13), (-11.799403787714187, -4.547473508864641e-13), (-11.799397545929853, -4.547473508864641e-13), (-11.799385062361186, -4.547473508864641e-13), (-11.799360095223847, -4.547473508864641e-13), (-11.799310160949165, -4.547473508864641e-13), (-11.799210292399806, -4.547473508864641e-13), (-11.799010555301091, -4.547473508864641e-13), (-11.798611081103658, -4.547473508864641e-13), (-11.797812132708792, -4.547473508864641e-13), (-11.79621423591906, -4.547473508864641e-13), (-11.793018442339598, -4.547473508864641e-13), (-11.786626855180678, -4.547473508864641e-13), (-11.773843680862829, -4.547473508864641e-13), (-11.748277332227136, -4.547473508864641e-13), (-11.697144634955752, -4.547473508864641e-13), (-11.594879240412979, -4.547473508864641e-13), (-11.39034845132743, -4.547473508864641e-13), (-10.981286873156343, -4.547473508864641e-13), (-10.163163716814157, -4.547473508864641e-13), (-8.526917404129794, -4.547473508864641e-13), (-5.25442477876106, -4.547473508864641e-13), (1.290560471976403, -5.115907697472721e-13), (14.380530973451327, -6.252776074688882e-13), (40.56047197640118, -6.821210263296962e-13), (92.92035398230088, -1.1937117960769683e-12), (197.64011799410025, -1.1937117960769683e-12), (407.07964601769913, -3.353761712787673e-12)]
templates = {
    'circle' : circlePoints,
    'square' : squarePoints,
    'triangle' : trianglePoints,
    's_point' : SPoints,
    'v_point' : VPoints
}

'''
Unsolved Error
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Users\yuliu\AppData\Local\Programs\Python\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\gesture-input.py", line 64, in stop_drawing
    self.update_callback()
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\gesture-input.py", line 45, in update_callback
    self.callback(self.drawing)
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\gesture-input.py", line 83, in handle_drawing_update
    best_result, score = recognizer.recognize(transfered_points, recognizer.templates, CANVAS_SIZE)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\recognizer.py", line 109, in recognize
    distance = distance_at_best_angle(points, template, -45, 45, 2)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\recognizer.py", line 119, in distance_at_best_angle
    f1 = distance_at_angle(points, template, x1)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\recognizer.py", line 141, in distance_at_angle
    return path_distance(new_points, template)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\recognizer.py", line 147, in path_distance
    distance_sum += distance(points_a[i], points_b[i])
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\yuliu\Projects\noProject\assignment-06-gesture-recognition-Leosssss\recognizer.py", line 25, in distance
    x2, y2 = p2
    ^^^^^^
ValueError: not enough values to unpack (expected 2, got 1)
'''

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
    length = path_length(points) 
    interval = length / (n - 1)
    
    new_points = [points[0]] 
    d = 0
    print("length = "+str(len(points)))
    for i in range(1, len(points)):
        print("points["+str(i)+"] = "+str(points[i]))
        D = distance(points[i - 1], points[i])
        
        if (d + D) >= interval:
            qx = points[i - 1][0] + ((interval - d) / D) * (points[i][0] - points[i - 1][0])
            qy = points[i - 1][1] + ((interval - d) / D) * (points[i][1] - points[i - 1][1])
            new_points.append((qx, qy)) 
            points.insert(i, (qx, qy)) 
            d = 0 
        else:
            d += D
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
