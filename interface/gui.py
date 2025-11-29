import tkinter as tk
from PIL import Image, ImageTk

def launch_main_gui():
    # Now it's safe to import heavy modules
    import platform
    if platform.system() == "Windows":
        import interface.gui_windows as gui
    else:
        import interface.gui_linux as gui

    gui.run_gui()

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("960x540+500+250")
    splash.configure(bg="white")

    img = Image.open("Splash.png")  # Use your actual image file
    img = img.resize((960, 540))         # Resize if needed
    photo = ImageTk.PhotoImage(img)

    # Display image
    img_label = tk.Label(splash, image=photo, bg="white")
    img_label.image = photo  # Keep reference to avoid garbage collection
    img_label.pack()


    # Schedule main GUI launch after splash delay
    splash.after(4000, lambda: (splash.destroy(), launch_main_gui()))
    splash.mainloop()

def run_gui(): show_splash()
