import tkinter as tk
import tkinter.ttk as ttk
from time import sleep

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class Slot():

    st = {'□': None, '0': 0, '1': 1}
    sc = {'□': 'red', '0': 'yellow', '1': 'blue'}
    ts = {None: '□', 0: '0', 1: '1'}
    tc = {None: 'red', 0: 'yellow', 1: 'blue'}
    cs = {'red': '□', 'yellow': '0', 'blue': '1'}
    ct = {'red': None, 'yellow': 0, 'blue': 1}

    def __init__(self, vs = 0, vt = 0, vc = 0):
        # valueString valueType valueColor

        if vs != 0:
            self.vs = vs
            self.vt = Slot.st[vs]
            self.vc = Slot.sc[vs]

        elif vt != 0:
            self.vs = Slot.ts[vt]
            self.vt = vt
            self.vc = Slot.tc[vt]

        elif vc != 0:
            self.vs = Slot.cs[vc]
            self.vt = Slot.ct[vc]
            self.vc = vc

        else:
            raise AttributeError

        return

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

slotsNb = 20
slots = [Slot(vt = None) for _ in range(slotsNb)]

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class TextCase(tk.Label):

    def __init__(self, master, slot, row, col):

        self.master = master
        self.content = slot
        self.text = slot.vt
        tk.Label.__init__(self, master, text = self.text, width = 3, highlightbackground = 'black', highlightthickness = 1)
        self.grid(row = row, column = col)

        return

    def changeContent(self, newContent):

        self.content = newContent
        self.text = newContent.vs
        self.config(text = self.text)
        self.content = Slot(vs = self.text)

        return

class ChoiceCase(tk.Frame):

    colors = ('red', 'yellow', 'blue')

    def __init__(self, master, row, col, slot = Slot(vc = 'red')):

        self.master = master
        self.color = slot.vc
        tk.Frame.__init__(self, master, width = 20, height = 20, highlightbackground = 'black', highlightthickness = 1, bg = self.color)
        self.bind('<Button-1>', self.nextColor)
        self.grid(row = row, column = col)

        return

    def nextColor(self, event = None):

        self.color = ChoiceCase.colors[(ChoiceCase.colors.index(self.color) + 1) % len(ChoiceCase.colors)]
        self.config(bg = self.color)

        return

    def getValue(self):

        return Slot(vc = self.color)

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
            [TextCase(self, Slot(vs = '□'), 0, 0), ChoiceCase(self, 0, 1), ArrowCase(self, 0, 2), ttk.Entry(self)],
            [TextCase(self, Slot(vs = '0'), 1, 0), ChoiceCase(self, 1, 1), ArrowCase(self, 1, 2), ttk.Entry(self)],
            [TextCase(self, Slot(vs = '1'), 2, 0), ChoiceCase(self, 2, 1), ArrowCase(self, 2, 2), ttk.Entry(self)]
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
    if row[cursor].vt == {l[i]}:
        row[cursor] = Slot(vs = '{self.cont[i][1].getValue().vs}')
        cursor {dirSign[i]}= 1
        return row, cursor, {nextFunc[i]}"""

        return t

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

def start():
    
    startBut.destroy()
    sts.quit()

    for i in range(slotsNb):
        slots[i] = Slot(vc = inputs[0][i].color)
        inputs[0][i] = TextCase(res, slots[i], 0, i)
    
    return

def refresh():

    for i in range(slotsNb):
        inputs[- 1][i].changeContent(slots[i])
    res.update()

    return

def addState(name_ = ''):
    
    global stateLine

    name = name_
    """if name == '':
        temp = tk.Tk()
        temp.title("State name")
        ent = ttk.Entry(temp, width = 100)
        ent.grid()
        ent.bind('<Return>', lambda e: e.widget.master.destroy())
        temp.mainloop()"""
    if name == '': name = input('State name: ')
    states.append(State(name, stateLine))
    stateLine += 1
    
    return

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

sts = tk.Tk()
res = tk.Tk()
sts.title('States')
res.title('Output')

inputs = [[ChoiceCase(res, 0, i) for i in range(slotsNb)]]
startBut = ttk.Button(res, text = 'Start', command = start)
startBut.grid(row = 0, column = slotsNb + 1)

states = list()
addStateBut = ttk.Button(sts, text = 'Add button', command = addState)
addStateBut.grid(row = 0, column = 0)
stateLine = 1
addState('init')

sts.mainloop()

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

def puits(row, cursor):
    return row, cursor, puits

def vrai(row, cursor):
    print('End')
    sts.destroy()
    while True:
        res.update()
    return row, cursor, vrai

"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

for s in states:
    exec(s.genFunc())

cursor = 0
for s in range(slotsNb):
    if slots[s].vt is not None:
        cursor = s
        break

func = init

while True:
    slots, cursor, func = func(slots, cursor)
    if cursor >= slotsNb: break
    inputs.append([TextCase(res, Slot(vt = None), len(inputs) - 1, i) for i in range(slotsNb)])
    refresh()
    sleep(1)

res.mainloop()
try:
    res.destroy()
    sts.destroy()
except:
    pass
