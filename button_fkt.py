import tkinter as tk

w = 16


def bFunc(self, t, fon, b, f, com, r, c):
    tk.Button(self, text=t,
              font=fon,
              bg=b, fg=f,
              width=w,
              command=com,
              relief='sunken').grid(row=r, column=c)


def bSite(self, master, t, fon, b, f, targetSite, r, c):
    tk.Button(self, text=t,
              font=fon,
              bg=b, fg=f,
              width=w,
              command=lambda: master.switch_frame(targetSite),
              relief='sunken').grid(row=r, column=c)


def bSetting(self, master, fon, b, f, targetSite):
    tk.Button(self, text='Einstellungen',
              font=fon,
              bg=b, fg=f,
              width=w,
              command=lambda: master.switch_frame(targetSite),
              relief='sunken').grid(row=9, column=1,
                                    padx=2, pady=2)


def bBack(self, master, fon, bgs, fgs, targetSite):
    tk.Button(self, text='zurück',
              font=fon,
              bg=bgs, fg=fgs,
              width=8, height=1,
              command=lambda: master.switch_frame(targetSite),
              relief='sunken').grid(row=9, column=1,
                                    padx=0, pady=0)


def bMainMenu(self, master, fon, bgs, fgs, targetSite):
    tk.Button(self, text='Hauptmenü',
              font=fon,
              bg=bgs, fg=fgs,
              width=8, height=1,
              command=lambda: master.switch_frame(targetSite),
              relief='sunken').grid(row=8, column=3,
                                    padx=0, pady=0)
