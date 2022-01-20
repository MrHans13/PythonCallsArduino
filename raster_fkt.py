import tkinter as tk
import color_fkt as colf


def rStand(self, bgC):
    for i in range(1, 4):
        tk.Label(self, text=" ",
                 bg=colf.backGround(bgC),
                 width=32,
                 height=2).grid(row=0, column=i, pady=1, padx=1)
    for i in range(1, 10):
        tk.Label(self, text="",
                 bg=colf.backGround(bgC),
                 width=1,
                 height=2).grid(row=i, column=0)
        tk.Label(self, text="",
                 bg=colf.backGround(bgC),
                 width=32,
                 height=2).grid(row=i, column=1)
        tk.Label(self, text="",
                 bg=colf.backGround(bgC),
                 width=1,
                 height=2).grid(row=i, column=4)
