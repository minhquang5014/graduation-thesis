import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class FullscreenWindow:
    def __init__(self, *args, **kwargs):
        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.root.title("Color Detection")
        self.root.configure(bg="black")

        self.frame = ctk.CTkFrame(master=self.root, fg_color="#ffd7b5")
        self.frame.pack(fill="both", expand=True)

        self.root.update()
        self.root.attributes('-fullscreen', True)

    def exit_fullscreen(self, event):
        self.root.destroy()

class CreateWindow():
    def __init__(self, window_width = 1250, window_height = 650, *args, **kwargs):
        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.title("Color Detection")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg="black")

        self.frame = ctk.CTkFrame(master=self.root, fg_color="#ffd7b5")
        self.frame.pack(fill="both", expand=True)

        self.root.update()

    def exit_fullscreen(self, event):
        self.root.destroy()
