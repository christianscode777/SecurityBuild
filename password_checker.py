from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk  # For nicer visual elements 


def check_password_strength(password):
    length_score, variety_score, common_word_penalty = 0, 0, 0

    if len(password) >= 8:
        length_score = 20
    
    variety_score += 15 * any(char.isupper() for char in password)
    variety_score += 15 * any(char.islower() for char in password)
    variety_score += 15 * any(char.isdigit() for char in password)
    variety_score += 15 * any(char in "!@#$%^&*()" for char in password)

    try:
        with open('txt/common_words.txt', 'r') as f:
            common_words = f.read().splitlines()
        if password.lower() in common_words:
            common_word_penalty = 30
    except FileNotFoundError:
        print("Common words file not found. Skipping common words check.")

    return length_score + variety_score - common_word_penalty

def check_strength(password, result_label):
    strength_score = check_password_strength(password)
    result_label.config(text=f"Password strength score: {strength_score}")

def start_gui():
    window = tk.Tk()
    window.title("Password Strength Checker")

    style = ttk.Style()
    style.configure("TEntry", foreground="#333", padding=10)
    style.map("TEntry",
              fieldbackground=[("active", "purple")],
              highlightthickness=[("focus", "1")],
              highlightcolor=[("focus", "purple")],
              highlightbackground=[("focus", "purple")])

    # Set up the canvas with the background image
    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack(fill="both", expand=True)

    try:
        # Load the image using PIL
        image = Image.open('images/reflect.png').resize((600, 400), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(image)  # Convert the PIL image to a PhotoImage
        # Use the image in the canvas
        canvas.create_image(0, 0, image=background_image, anchor="nw")
        # Keep a reference to avoid garbage collection
        canvas.image = background_image
    except Exception as e:
        print(f"Error loading background image: {e}")

    # Input area
    input_label = tk.Label(window, text="Enter Password:", background="#ffffff")
    password_entry = ttk.Entry(window, style="TEntry")  # Using ttk.Entry for styling

    # Output area
    result_label = tk.Label(window, text="", background="#ffffff")

    # Button to check strength
    check_button = ttk.Button(window, text="Check Strength", command=lambda: check_strength(password_entry.get(), result_label))

    # Position the input label and entry field
    input_label.place(relx=0.35, rely=0.4, anchor="e")
    password_entry.place(relx=0.5, rely=0.4, anchor="w", width=200, height=30)  # Adjusted width and height

    # Position the result label and check button
    result_label.place(relx=0.5, rely=0.5, anchor="center")
    check_button.place(relx=0.5, rely=0.6, anchor="center")

    window.mainloop()

if __name__ == "__main__":
    start_gui()
