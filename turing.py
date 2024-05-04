import tkinter as tk
import tkinter.ttk as ttk
from time import sleep

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

slotsNb = 20
slots = [None for _ in range(slotsNb)]

symbsCor = {'□': None, '0': 0, '1': 1}
symbsMir = {None: '□', 0: '0', 1: '1'}

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class TextCase(tk.Label):

    def __init__(self, master, content, row, col):

        self.master = master
        self.content = content
        self.text = self.content
        tk.Label.__init__(self, master, text = self.text, width = 3, highlightbackground = 'black', highlightthickness = 1)
        self.grid(row = row, column = col)

        return

    def changeText(self, newText):

        self.text = newText
        self.config(text = self.text)

        return

class ChoiceCase(tk.Frame):

    colors = ['red', 'yellow', 'blue']
    colorsDict = {'red': '□', 'yellow': '0', 'blue': '1'}

    def __init__(self, master, row, col, color = 'red'):

        self.master = master
        self.color = color
        tk.Frame.__init__(self, master, width = 20, height = 20, highlightbackground = 'black', highlightthickness = 1, bg = color)
        self.bind('<Button-1>', self.nextColor)
        self.grid(row = row, column = col)

        return

    def nextColor(self, event = None):

        self.color = ChoiceCase.colors[(ChoiceCase.colors.index(self.color) + 1) % len(ChoiceCase.colors)]
        self.config(bg = self.color)

        return

    def getValue(self):

        return ChoiceCase.colorsDict[self.color]

class ArrowCase(tk.Label):

    def __init__(self, master, row, col, default = '→'):

        self.master = master
        self.direct = default
        tk.Label.__init__(self, master, text = self.direct, width = 3)
        self.bind('<Button-1>', self.click)
        self.grid(row = row, column = col)

        return

    def click(self, event = None):

        if self.direct == '←': self.direct = '→'
        else: self.direct = '←'
        self.config(text = self.direct)

        return

    def getDirect(self):

        if self.direct == '←': return 'l'
        return 'r'

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class State(ttk.LabelFrame):

    def __init__(self, name, row):

        self.name = name
        ttk.LabelFrame.__init__(self, sts, text = self.name)

        self.cont = [
            [TextCase(self, '□', 0, 0), ChoiceCase(self, 0, 1), ArrowCase(self, 0, 2), ttk.Entry(self)],
            [TextCase(self, '0', 1, 0), ChoiceCase(self, 1, 1), ArrowCase(self, 1, 2), ttk.Entry(self)],
            [TextCase(self, '1', 2, 0), ChoiceCase(self, 2, 1), ArrowCase(self, 2, 2), ttk.Entry(self)]
        ]
        for w in range(len(self.cont)): self.cont[w][- 1].grid(row = w, column = 3)
        
        self.grid(row = row, column = 0)

        return

    def genFunc(self):

        t = f"def {self.name}(row, cursor):"
        l = [None, 0, 1]
        dirSign, nextFunc = list(), list()
        for i in self.cont:
            if i[2].getDirect() == 'l': dirSign.append('-')
            else: dirSign.append('+')
            nextFunc.append(i[3].get())
        for i in range(3):
            t += f"""
    if row[cursor] == {l[i]}:
        row[cursor] = {symbsCor[self.cont[i][1].getValue()]}
        cursor {dirSign[i]}= 1
        return row, cursor, {nextFunc[i]}"""

        return t

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

def start():
    
    startBut.destroy()
    sts.quit()

    for i in range(slotsNb):
        slots[i] = ChoiceCase.colorsDict[inputs[i].color]
        inputs[i].destroy()
        inputs[i] = TextCase(res, slots[i], 0, i)
        slots[i] = symbsCor[slots[i]]
    
    return

def refresh():

    for i in range(slotsNb):
        inputs[i].changeText(slots[i])

    return

def addState(name_ = ''):
    
    global stateLine

    name = name_
    if name == '': name = input('State name: ')
    states.append(State(name, stateLine))
    stateLine += 1
    
    return

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

sts = tk.Tk()
res = tk.Tk()
sts.title('States')
res.title('Output')

inputs = [ChoiceCase(res, 0, i) for i in range(slotsNb)]
startBut = ttk.Button(res, text = 'Start', command = start)
startBut.grid(row = 0, column = slotsNb + 1)

states = list()
addStateBut = ttk.Button(sts, text = 'Add button', command = addState)
addStateBut.grid(row = 0, column = 0)
stateLine = 1
addState('init')

sts.mainloop()

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

for s in states:
    exec(s.genFunc())

cursor = 0
func = init
print(slots)
while True:
    slots, cursor, func = func(slots, cursor)
    for i in range(slotsNb):
        slots[i] = symbsMir[slots[i]]
    if cursor >= slotsNb: break
    refresh()
    for i in range(slotsNb):
        slots[i] = symbsCor[slots[i]]
    res.update()
    sleep(1)

res.mainloop()
