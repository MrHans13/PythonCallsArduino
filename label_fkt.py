import tkinter as tk


def lSmall(self, t, fon, b, f, r, c):
    tk.Label(self, text=t,
             font=fon,
             bg=b, fg=f).grid(row=r, column=c)


def lTitel(self, t, fon, b, f):
    tk.Label(self, text=t,
             font=fon,
             bg=b, fg=f).grid(row=0, column=1, padx=2, pady=2, sticky='W')


def lPic(self, img, r, c):
    tk.Label(self, image=img).grid(row=r, column=c)
