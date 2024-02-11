from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
import tkinter as tk
from tkinter import PhotoImage, OptionMenu, Button, filedialog
 
class CaptchaGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Captcha Generator")
 
        self.available_fonts = ['Arial_Bold_Italic', 'Arial_Italic', 'Arial', 'Courier_New', 'Montserrat-Italic-VariableFont_wght', 'Montserrat-VariableFont_wght', 'Oswald-VariableFont_wght', 'ProtestGuerrilla-Regular', 'Raleway-Italic-VariableFont_wght', 'Raleway-VariableFont_wght', 'Verdana_Bold', 'Verdana_Italic', 'Verdana']  # Example font files
        
        # Generate captcha with default font
        self.selected_font = self.available_fonts[0]  # Default font
        self.generate_captcha()
 
        # Display captcha image
        self.captcha_image = PhotoImage(file=self.image_path)
        self.captcha_label = tk.Label(master, image=self.captcha_image)
        self.captcha_label.pack(side="left")
 
        # Font selection dropdown
        self.font_selection = OptionMenu(master, tk.StringVar(master, self.available_fonts[0]), *self.available_fonts, command=self.on_font_select)
        self.font_selection.pack(side="right")
 
        # GO button
        self.go_button = Button(master, text="GO", command=self.on_go_click)
        self.go_button.pack(side="right")
 
        # Save button
        self.save_button = Button(master, text="Save", command=self.on_save_click)
        self.save_button.pack(side="right")
 
    def on_font_select(self, selected_font):
        self.selected_font = selected_font
 
    def on_go_click(self):
        # Regenerate captcha with the selected font
        self.generate_captcha()
 
        # Update displayed image
        self.captcha_image = PhotoImage(file=self.image_path)
        self.captcha_label.config(image=self.captcha_image)
 
    def on_save_click(self):
        # Ask user to select a directory to save the captcha
        save_path = filedialog.askdirectory()
        if save_path:
            # Generate captcha image
            self.generate_captcha()
 
            # Ask user for file name
            file_name = tk.simpledialog.askstring("Input", "Enter file name:", parent=self.master)
            if file_name:
                # Save the captcha image to the selected directory with user-defined file name
                image_path = os.path.join(save_path, file_name + '.png')
                image = Image.open('temp_captcha.png')  # Open the temporary captcha image
                image.save(image_path)  # Save the image to the selected directory
 
                # Display saved image
                self.image_path = image_path
                self.captcha_image = PhotoImage(file=self.image_path)
                self.captcha_label.config(image=self.captcha_image)
 
    def generate_captcha(self, size=(200, 100), font_size=40, length=6):
        # Generate random string for captcha
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
 
        # Create an image captcha
        image = self.generate_image(size, captcha_text)
 
        # Save the captcha image temporarily
        self.image_path = 'temp_captcha.png'
        image.save(self.image_path)
 
    def generate_image(self, size, captcha_text):
    # Create a blank image
     image = Image.new('RGB', size, color='white')
     draw = ImageDraw.Draw(image)
 
    # Load selected font
     font_folder = '/Users/saishivaniaahwanikamaddilakshmi/Documents/fonts'  # Change this to the correct path where your fonts are located
     font_path = os.path.join(font_folder, self.selected_font + '.ttf')  # Adding .ttf extension
     font_size = 40
     font = ImageFont.truetype(font_path, size=font_size)
 
    # Calculate text position
     text_bbox = draw.textbbox((0, 0), captcha_text, font)
     x = (size[0] - text_bbox[2]) / 2
     y = (size[1] - text_bbox[3]) / 2
 
    # Generate random color for text
     text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
 
    # Draw text on the image
     draw.text((x, y), captcha_text, font=font, fill=text_color)
 
    # Add noise (optional)
     self.add_noise(draw, size)
 
     return image
 
 
    def add_noise(self, draw, size, num_points=100):
        for _ in range(num_points):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            draw.point((x, y), fill='black')
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaGeneratorGUI(root)
    root.mainloop()
