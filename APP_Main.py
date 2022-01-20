import tkinter as tk
from tkinter import PhotoImage

import button_fkt as buf
import font_fkt as fonf
import label_fkt as labf
import raster_fkt as rasf
import wifi_fkt as wifi
import color_fkt as colf
import serial_fkt as serf

bgCount = 0
fgCount = 0


class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.configure(bg=background)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self.configure(bg=background)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=background)
        rasf.rStand(self, bgCount)

        labf.lTitel(self, 'Hauptmenü:', titelfont, background, foregrond)
        buf.bSite(self, master, 'Steckdosen', buttonfont, background, foregrond, Steckdosen, 8, 1)
        buf.bSite(self, master, 'Daten', buttonfont, background, foregrond, DataPage, 7, 1)
        buf.bSetting(self, master, buttonfont, background, foregrond, Einstellungen)


class DataPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=background)
        rasf.rStand(self, bgCount)

        labf.lTitel(self, "Daten:", titelfont, background, foregrond)
        labf.lSmall(self, "Daten auslesen:", labelfont, background, foregrond, 1, 2)
        labf.lSmall(self, "Daten löschen:", labelfont, background, foregrond, 1, 3)
        labf.lSmall(self, "W-LAN:", labelfont, background, foregrond, 2, 1)
        labf.lSmall(self, "Seriell:", labelfont, background, foregrond, 4, 1)
        buf.bFunc(self, "Data -> Wifi", buttonfont, background, foregrond, wifi.steckdosenDataW, 2, 2)
        buf.bFunc(self, "Data clear", buttonfont, background, foregrond, wifi.wDatenLoeschen, 2, 3)
        buf.bFunc(self, "Data Serial", buttonfont, background, foregrond, serf.serialData, 4, 2)
        buf.bFunc(self, "Data clear", buttonfont, background, foregrond, wifi.wDatenLoeschen, 4, 3)

        buf.bBack(self, master, buttonfont, background, foregrond, StartPage)


class Einstellungen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=background)

        rasf.rStand(self, bgCount)
        labf.lTitel(self, 'Einstellungen:', titelfont, background, foregrond)
        buf.bFunc(self, "Bg schwarz", buttonfont, background, foregrond, bgChange(0), 2, 1)
        buf.bFunc(self, "Bg rot", buttonfont, background, foregrond, bgChange(1), 3, 1)
        buf.bFunc(self, "Bg grau", buttonfont, background, foregrond, bgChange(2), 4, 1)
        buf.bFunc(self, "Bg dunkelgrau", buttonfont, background, foregrond, bgChange(3), 5, 1)

        buf.bBack(self, master, buttonfont, background, foregrond, StartPage)


class Steckdosen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=background)

        rasf.rStand(self, bgCount)
        labf.lTitel(self, 'Steckdosen:', titelfont, background, foregrond)

        labf.lSmall(self, 'Steckdose 1:', labelfont, background, foregrond, 1, 2)
        labf.lSmall(self, 'Steckdose 2:', labelfont, background, foregrond, 4, 2)
        labf.lSmall(self, 'Steckdose 3:', labelfont, background, foregrond, 7, 2)

        buf.bFunc(self, 'Manuell:', buttonfont, background, foregrond, wifi.steckdoseEins, 2, 2)
        buf.bFunc(self, 'Manuell:', buttonfont, background, foregrond, wifi.steckdoseZwei, 5, 2)
        buf.bFunc(self, 'Manuell:', buttonfont, background, foregrond, wifi.steckdoseDrei, 8, 2)
        buf.bFunc(self, 'Alles aus:', buttonfont, background, foregrond, wifi.steckdosenAlle, 8, 1)
        labf.lPic(self, statePicOff, 2, 3)
        labf.lPic(self, statePicOn, 2, 3)
        labf.lPic(self, statePicOff, 5, 3)
        labf.lPic(self, statePicOff, 8, 3)

        buf.bBack(self, master, buttonfont, background, foregrond, StartPage)


def bgChange(x):
    global bgCount
    bgCount = x


if __name__ == "__main__":
    titelfont = fonf.font20(0)
    buttonfont = fonf.buttonFont(0)
    labelfont = fonf.labelFont(0)
    background = colf.backGround(bgCount)
    foregrond = colf.foreGround(fgCount)

    app = SampleApp()
    app.resizable(width=False, height=False)
    app.title('standBy Goodbye!!!')
    app.geometry('840x390')
    SteckdosenBild: PhotoImage = tk.PhotoImage(file="SteckdosenBild.png")
    statePicOn: PhotoImage = tk.PhotoImage(file='signalGreen.png')
    statePicOff: PhotoImage = tk.PhotoImage(file='signalRed.png')
    #    app.configure(bg=background)

    app.mainloop()
