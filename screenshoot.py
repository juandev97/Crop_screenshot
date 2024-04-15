import os 
#import PyPDF2
#import webbrowser
from PIL import Image, ImageGrab
import time



import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes
import pyautogui
import random



        
class Scene:
    def __init__(self, window: tk.Tk, screen_instance):
        self.screen_instance = screen_instance
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas(
            window, 
            width=self.screen_width,
            height=self.screen_height, 
            highlightthickness=0,  
            bg='white'
        )
        self.capture = tk.Button(window, text="Tomar Screenshot", command=self.takeScreenshot)
        self.center = tk.Button(window, text="Centrar navegador", command=self.early_stop)
        self.close = tk.Button(window, text="¡Cerrar!", command=self.early_stop)
        
        self.capture.place(x=100,y=410)
        self.center.place(x=100,y=450)
        self.close.place(x=100,y=490)
        self.canvas.pack()
        self.x1, self.y1, self.x2, self.y2 = 500, 500, 900, 900

    def clear_canvas(self):
        self.canvas.delete('all')

    def update(self):
        self.clear_canvas()
        self.rectangulo = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,  # Coordenadas del rectángulo (x1, y1, x2, y2)
            outline='red',  # Color del borde
            fill='',  # Sin relleno
            width=10
    )
        selected_side = None

        # Asociar los eventos de clic y arrastre del mouse con las funciones correspondientes
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)


    def on_canvas_click(self, event):
        global selected_side

        #print("On click", type(self).__name__)
        # Obtener las coordenadas del rectángulo
        self.x1, self.y1, self.x2, self.y2 = self.canvas.coords(self.rectangulo)

        # Determinar qué lado del rectángulo fue clicado
        margin = 5  # Margen para considerar un clic en el borde
        if abs(event.x - self.x1) <= margin:  # Clic cerca de la línea izquierda
            selected_side = 'left'
        elif abs(event.x - self.x2) <= margin:  # Clic cerca de la línea derecha
            selected_side = 'right'
        elif abs(event.y - self.y1) <= margin:  # Clic cerca de la línea superior
            selected_side = 'top'
        elif abs(event.y - self.y2) <= margin:  # Clic cerca de la línea inferior
            selected_side = 'bottom'
        else:
            selected_side = None

    # Función para manejar el evento de movimiento del mouse
    def on_canvas_drag(self,event):
        global selected_side

        self.canvas.config(cursor='fleur')
        #print("On canvas drag ",type(self).__name__)
        # Obtener las coordenadas actuales del rectángulo
        self.x1, self.y1, self.x2, self.y2 = self.canvas.coords(self.rectangulo)

        # Ajustar la coordenada del rectángulo según la cara seleccionada
        if selected_side == 'left':
            self.x1 = event.x  # Mover la línea izquierda
        elif selected_side == 'right':
            self.x2 = event.x  # Mover la línea derecha
        elif selected_side == 'top':
            self.y1 = event.y  # Mover la línea superior
        elif selected_side == 'bottom':
            self.y2 = event.y  # Mover la línea inferior

        # Actualizar las coordenadas del rectángulo en el canvas
        self.canvas.coords(self.rectangulo,self.x1, self.y1, self.x2, self.y2)


    def on_canvas_release(self,event):
        global selected_side

        # Restablecer el cursor a su valor predeterminado
        self.canvas.config(cursor='')

        # Restablecer la variable selected_side
        selected_side = None
    
    def takeScreenshot(self):
        img = ImageGrab.grab()
        #izqu, arriba, derecha, abajo
        #box = (460, 215, 1330, 570)
        box = (self.x1, self.y1, self.x2, self.y2)
        area = img.crop(box)
        area.save(os.getcwd()+'\\New.png', 'png')


    def early_stop(self):
        self.screen_instance.window.destroy()

class Screen:
    def __init__(self):
        self.window = self.create_window()
        self.apply_click_through(self.window)
        self.scene = Scene(self.window, self)

    def update(self):
        self.scene.update()
        self.window.after(5, self.update)

    def create_window(self):
        window = tk.Tk()
        window.wm_attributes("-topmost", True)
        window.attributes("-fullscreen", True) 
        window.overrideredirect(True)
        # Transparencia
        window.attributes('-transparentcolor', 'white')
        window.config(bg='white')
        return window

    def apply_click_through(self, window):
        # Constantes API windows
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20

        # Obtener el identificador de ventana (HWND)
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        # Obtener los estilos actuales de la ventana
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        # Establecer nuevo estilo
        style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def start(self):
        self.update()
        self.window.mainloop()

screen = Screen()
screen.start()
