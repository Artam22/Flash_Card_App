from tkinter import *
from random import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
#----------------------- FLASH CARDS -----------------------#
def next_card():
    global current_card, flip_timer
    current_card = choice(to_learn)
    window.after_cancel(flip_timer)
    canvas.itemconfig(flash_card, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{current_card['French']}")
    flip_timer = window.after(3000, func=flip_card)

def is_known():
    global current_card
    to_learn.remove(current_card)
    n_data = pandas.DataFrame(to_learn)
    n_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def flip_card():
    global current_card
    canvas.itemconfig(flash_card, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{current_card['English']}")

#----------------------- WINDOW -----------------------#
window = Tk()
window.title("Flashy", )
window.config(padx=50, pady=50,bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

#----------------------- CARD FRONT -----------------------#
canvas = Canvas(width=800,height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
flash_card = canvas.create_image(400,263, image=card_front)
canvas.grid(column=0,row=0,columnspan=2)
card_title = canvas.create_text(400, 150, text="",fill="black",font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 55, "bold"))

#----------------------- BUTTONS -----------------------#
r_button_logo = PhotoImage(file="./images/right.png")
r_button = Button(image=r_button_logo, bg=BACKGROUND_COLOR, highlightthickness=0,
                  command=is_known)
r_button.grid(column=1, row=1)

w_button_logo = PhotoImage(file="./images/wrong.png")
w_button = Button(image=w_button_logo, bg=BACKGROUND_COLOR, highlightthickness=0,
                  command=next_card)
w_button.grid(column=0, row=1)


next_card()



window.mainloop()
