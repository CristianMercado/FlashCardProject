from tkinter import *
import pandas
from random import *

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
list_data = data.to_dict(orient="records")
random_entry = {}


# Obtain a random French word
def random_word():
    global random_entry, flip_timer
    window.after_cancel(flip_timer)
    random_entry = choice(list_data)

    canvas.itemconfig(actual_image, image=card_front)
    canvas.itemconfig(title_text, text="French")
    canvas.itemconfig(word_text, text=random_entry["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(word_text, text=random_entry["English"], fill="white")
    canvas.itemconfig(actual_image, image=card_back)


def save_word():
    global list_data
    list_data.remove(random_entry)
    new_entry = pandas.DataFrame(list_data)
    new_entry.to_csv("data/words_to_learn.csv", index=False)
    random_word()


# Setup Window
window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_card)

# Setup Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

actual_image = canvas.create_image(400, 263, image=card_front)

title_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)


# Setup Buttons
yes_image = PhotoImage(file="images/right.png")
right_button = Button(image=yes_image, highlightthickness=0, command=save_word)
right_button.grid(row=1, column=1)

no_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=no_image, highlightthickness=0, command=random_word)
wrong_button.grid(row=1, column=0)

random_word()


window.mainloop()
