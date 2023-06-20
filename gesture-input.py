# gesture input program for first task

import math
import tkinter as tk
import recognizer

TITLE = "$1 Unistroke Recognizer"
LABEL_INIT = "Waiting to draw"
LABEL_START_DRAW = "Recording unistroke"
LABEL_RESULT = "Result"
BUTTON_TEXT = "Clear canvas"
BG_COLOR = "#ad33ff"
CANVAS_SIZE = 400

drawing_app = None

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
            resampled_points = recognizer.resample(points, 64)
            rotated_points = recognizer.rotate_to_zero(resampled_points)  
            scaled_points = recognizer.scale_to_square(rotated_points, CANVAS_SIZE)
            transfered_points = recognizer.translate_to_origin(scaled_points)
            print("HIER")
            best_result, score = recognizer.recognize(transfered_points, recognizer.templates, CANVAS_SIZE)
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