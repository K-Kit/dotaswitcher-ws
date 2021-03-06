import sys
import time
import mmap
import logging
import time
logging.basicConfig(level=logging.INFO)
sys.path.append('../')
from obswebsocket import obsws, requests
from Tkinter import *
from ttk import *



class opm:

    def __init__(self, master, label):
        self.lable = label
        self.scene = "none"
        optionsV = StringVar()
        optionsV.set(None)
        options = ["none", "none"]
        for s in scenes.getScenes():
            name = s['name']
            options.append(name)
        frame = Frame(master)
        frame.pack()
        left = Frame(frame)
        left.pack(side=LEFT)
        right = Frame(frame)
        right.pack(side=RIGHT)
        self.addlabel = Label(left, text=label, anchor=W, justify=LEFT, background="white")
        self.addmenu = OptionMenu(right, optionsV, *options, command=self.func)
        # self.addlabel.pack(side = LEFT)
        # self.addmenu.pack(side = RIGHT)
        self.addlabel.grid(column = 0)
        self.addmenu.grid(pady = 5)

    def func(self, value):
        self.scene = value
        print (value)
    def getlable(self):
        return self.addlabel.cget("text")



# from ttk import *
host = "localhost"
port = 4444
password = "secret"
global path
path = ""
ws = obsws(host, port, password)
ws.connect()
scenes = ws.call(requests.GetSceneList())
root = Tk()
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)
theLabel = Label(topFrame, text= "Dota Scene Switcher")
theLabel.grid(row=0)
label_Path = Label(topFrame, text = "path to console.log")
entry_Path = Entry(topFrame)
label_Path.grid(row=1)
entry_Path.grid(row=1, column=1)


def quit(self):
    self.root.destroy
def on_change(e):
    global path
    path = entry_Path.get()
entry_Path.bind("<Return>", on_change)
optionsV = StringVar()
optionsV.set(None)
options = ["none"]
for s in scenes.getScenes():
    name = s['name']
    options.append(name)
dashboard = opm(root, "DOTA_GAME_UI_STATE_DASHBOARD")
init = opm(root, "INIT")
loading = opm(root, "WAIT_FOR_PLAYERS_TO_LOAD")
setup = opm(root, "CUSTOM_GAME_SETUP")
heroSel = opm(root, "HERO_SELECTION")
strategy = opm(root, "STRATEGY_TIME")
teamshowcase = opm(root, "TEAM_SHOWCASE")
pregame = opm(root, "PRE_GAME")
gameinprogress = opm(root, "GAME_IN_PROGRESS")
postgame = opm(root, "POST_GAME")
disconnect = opm(root, "DISCONNECT")


def getState():
    with open(path, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        gamerules = mm.rfind("Gamerules: entering state")
        ChangeGame = mm.rfind("ChangeGameUIState: ")
        curLine = 0
        if (gamerules > ChangeGame):
            cur = gamerules
        else:
            cur = ChangeGame
        # print(cur)
        mm.seek(cur)
        line = mm.readline()
        # mm.rfind(" ")
        # print(line)
        # print(line.rsplit(None, 1)[-1])
        mm.close()
        return line.rsplit(None, 1)[-1]
def switch():
    cur = getState()
    if (cur == "DOTA_GAME_UI_STATE_DASHBOARD" and dashboard.scene != "none"):
        cs = dashboard.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_INIT'" and init.scene != "none"):
        cs = init.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD'" and loading.scene != "none"):
        cs = loading.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP'" and setup.scene != "none"):
        cs = setup.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_HERO_SELECTION'" and heroSel.scene != "none"):
        cs = heroSel.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_STRATEGY_TIME'" and strategy.scene != "none"):
        cs = strategy.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_TEAM_SHOWCASE'" and teamshowcase.scene != "none"):
        cs = teamshowcase.scene
        ws.call(requests.SetCurrentScene(cs))

    if (cur == "'DOTA_GAMERULES_STATE_PRE_GAME'" and pregame.scene != "none"):
        print("working")
        cs = pregame.scene
        ws.call(requests.SetCurrentScene(cs))
    if (cur == "'DOTA_GAMERULES_STATE_GAME_IN_PROGRESS'" and gameinprogress.scene != "none"):
        cs = gameinprogress.scene
        ws.call(requests.SetCurrentScene(cs))
    if (cur == "'DOTA_GAMERULES_STATE_POST_GAME'" and postgame.scene != "none"):
        cs = postgame.scene
        ws.call(requests.SetCurrentScene(cs))
    if (cur == "'DOTA_GAMERULES_STATE_DISCONNECT'" and disconnect.scene != "none"):
        cs = disconnect.scene
        ws.call(requests.SetCurrentScene(cs))

    # ws.call(requests.SetCurrentScene(name))

def run():
    global path
    path=entry_Path.get()
    root.destroy()
    cur = getState()
    switch()
    while (1>0):
        # print getState()
        new = getState()
        if (cur!= new):
            cur = new
            switch()
        time.sleep(1)
b = Button(bottomFrame, text="run", command=run)
b.pack()
root.mainloop()
print(scenes.getScenes())


