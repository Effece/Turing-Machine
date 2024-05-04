import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as sdtk
import tkinter.filedialog as fdtk
from time import sleep

from default import *

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

class Slot():

    empty = ('o', None, 'red')
    zero  = ('0', 0, 'yellow')
    one   = ('1', 1, 'blue')

    def __init__(self, vs = - 1, vt = - 1, vc = - 1):
        # valueString valueType valueColor

        cont = None

        if vs != - 1:
            cont = Slot.find(vs)

        elif vt != - 1:
            cont = Slot.find(vt)

        elif vc != - 1:
            cont = Slot.find(vc)

        else:
            raise AttributeError

        self.vs, self.vt, self.vc = cont

        return

    @classmethod
    def find(cls, value):
        """
        Finds the tuple corresponding to value. Returns - 1 if it doesn't exist.
        """

        for e in (cls.empty, cls.zero, cls.one):
            if value in e: return e

        return - 1

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

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

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

class State(ttk.LabelFrame):

    def __init__(self, name, row):

        self.name = name
        ttk.LabelFrame.__init__(self, sts, text = self.name)

        c = ('o', '0', '1')
        self.cont = [
            [TextCase(self, Slot(vs = c[i]), i, 0), ChoiceCase(self, i, 1), ArrowCase(self, i, 2), ttk.Entry(self)] for i in range(len(c))
        ]

        for w in self.cont: w[3].insert(tk.END, 'undef')
        for w in range(len(self.cont)): self.cont[w][- 1].grid(row = w, column = 3)
        
        self.grid(row = row, column = 0)

        return

    def genFunc(self):

        t = f"def {self.name}(row, cursor):"
        l = (None, 0, 1)
        dirSign, nextFunc = list(), list()
        for i in self.cont:
            if i[2].getDirect() == 'l': dirSign.append('-')
            else: dirSign.append('+')
            nextFunc.append(i[3].get())
        for i in range(len(l)):
            t += f"""
    if row[cursor].vt == {l[i]}:
        row[cursor] = Slot(vs = '{self.cont[i][1].getValue().vs}')
        cursor {dirSign[i]}= 1
        return row, cursor, {nextFunc[i]}"""

        return t

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

def start():
    
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
    if name == '':
        name = sdtk.askstring(title = 'New state', prompt = 'Select the name of your new state.')

    # name verification
    for c in name:
        if not 0 <= ord(c) <= 127: raise ValueError
    
    states.append(State(name, stateLine))
    stateLine += 1
    
    return

def importStates():

    path = fdtk.askopenfilename() # filetypes = ("py", "txt")
    with open(path, mode = 'r') as f:
        try:
            exec(f.read())
        except Exception as e:
            print(e)
        f.close()

    return

def exportStates():

    f = fdtk.asksaveasfile(mode = 'w', defaultextension = '.py')
    for s in states:
        print(s.genFunc())
        f.write(s.genFunc())
        f.write('\n')
    f.close()

    return

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

sts = tk.Tk()
res = tk.Tk()
sts.title('States')
res.title('Output')

slotsNb = 20
slots = [Slot(vt = None) for _ in range(slotsNb)]
timeInter = 1

inputs = [[ChoiceCase(res, 0, i) for i in range(slotsNb)]]

states = list()
stateLine = 1
addState('init')

menu = tk.Menu(sts)
subMenu = tk.Menu(menu, tearoff = False)
sts.config(menu = menu)
menu.add_cascade(label = "Options", menu = subMenu)
subMenu.add_command(label = "Add state", command = addState)
subMenu.add_command(label = "Start", command = start)
subMenu.add_command(label = "Import", command = importStates)
subMenu.add_command(label = "Export", command = exportStates)

sts.mainloop()

"""------------------------------------------------------------------------------------------------------------------------------------------------------"""

functionTexts = [s.genFunc() for s in states]
for f in functionTexts:
    try:
        exec(f)
    except Exception as e:
        print(e)
        exit()

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
    sleep(timeInter)

for f in functionTexts: print(f)

try:
    res.mainloop()
except:
    try:
        res.destroy()
    except:
        pass
