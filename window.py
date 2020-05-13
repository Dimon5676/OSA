from tkinter import *


class Window:
    def __init__(self, width, height, title):
        self.window = Tk()
        self.window.title(title)
        self.window.resizable(False, False)
        self.canv = Canvas(self.window, width=width, height=height)
        self.configureButton = Button(self.window, text='Добавить уровень', command=self.configure)
        self.addButton = Button(self.window, text='Добавить связь', command=self.addConnection)
        self.calculateButton = Button(self.window, text='Вычислить', command=self.calculate)
        self.exitButton = Button(self.window, text='Выход', command=(lambda: self.window.destroy()))
        self.window.after(100, self.redraw)

        self.cellSize = 46
        self.matrix = []
        self.connections = []

    def run(self):
        self.window.mainloop()

    def draw(self):
        self.canv.grid(row=0, column=0, columnspan=2)
        self.configureButton.grid(row=1, column=0, sticky=W + E)
        self.addButton.grid(row=1, column=1, sticky=W + E)
        self.calculateButton.grid(row=2, column=0, sticky=W + E)
        self.exitButton.grid(row=2, column=1, sticky=W + E)

    def redraw(self):
        for i in range(len(self.matrix)):
            off = ((800 - (len(self.matrix[i]) * 2 - 1) * self.cellSize) / 2)
            for j in range(len(self.matrix[i])):
                self.canv.create_rectangle(j * 2 * self.cellSize + off, i * 2 * self.cellSize + self.cellSize,
                                           j * 2 * self.cellSize + off + self.cellSize,
                                           i * 2 * self.cellSize + 2 * self.cellSize)
                if self.matrix[i][j]:
                    self.canv.create_text(j * 2 * self.cellSize + off + 4, i * 2 * self.cellSize + self.cellSize + 6,
                                          text=round(self.matrix[i][j], 2), anchor=NW)

        no = 0
        for layer in self.connections:
            off1 = ((800 - (len(self.matrix[no]) * 2 - 1) * self.cellSize) / 2)
            off2 = ((800 - (len(self.matrix[no + 1]) * 2 - 1) * self.cellSize) / 2)
            for i in range(len(layer)):
                for j in range(len(layer[i])):
                    if layer[i][j]:
                        self.canv.create_line(i * 2 * self.cellSize + off2 + self.cellSize / 2,
                                              (no + 1) * 2 * self.cellSize + self.cellSize,
                                              j * 2 * self.cellSize + off1 + self.cellSize / 2,
                                              no * 2 * self.cellSize + 2 * self.cellSize)
            no += 1

    def configure(self):
        conf = Toplevel(self.window)
        conf.resizable(False, False)
        conf.focus_get()
        weights = Entry(conf, width=40)
        addButton = Button(conf, text="Добавить", command=(lambda: self.addLayer(weights)))
        closeButton = Button(conf, text="Закрыть", command=(lambda: conf.destroy()))

        Label(conf, text="Введите веса уровня через пробел (0 - если вес нужно вычислить)").grid(row=0, column=0,
                                                                                                 columnspan=2)
        weights.grid(row=1, column=0, columnspan=2)
        addButton.grid(row=2, column=0)
        closeButton.grid(row=2, column=1)

    def addLayer(self, entry):
        text = entry.get()
        weights = [x for x in str(text).split(' ') if x != '']
        weights_float = []
        try:
            for i in range(len(weights)):
                weights_float.append(float(weights[i].strip()))
        except ValueError:
            print("ValueError")
            return
        self.matrix.append(weights_float)
        entry.delete(0, END)
        self.window.after(100, self.redraw)

    def addConnection(self):
        if len(self.matrix) < 2:
            return
        wind = Toplevel(self.window)
        wind.resizable(False, False)
        wind.focus_get()
        l = Label(wind, text=f'Введите матрицу связей - {len(self.connections) + 1}')
        field = Text(wind, font="TimesNewRoman 20", width=40, height=1, highlightbackground='black')
        addButton = Button(wind, text="Добавить", command=(lambda: self.addCon(field, wind)))
        try:
            field.configure(height=len(self.matrix[len(self.connections) + 1]))
        except IndexError:
            l.configure(text="Добавьте ещё один слой!")
            field.configure(state=DISABLED)
            addButton.configure(state=DISABLED)
        closeButton = Button(wind, text="Закрыть", command=(lambda: wind.destroy()))

        l.grid(row=0, column=0, columnspan=2)
        field.grid(row=1, column=0, columnspan=2)
        addButton.grid(row=2, column=0)
        closeButton.grid(row=2, column=1)

    def addCon(self, t, wind):
        weights = []
        temp = []
        text = t.get('1.0', END)
        w_str = str(text).split('\n')
        w_str.pop(-1)
        for i in w_str:
            temp.clear()
            for j in i.split(' '):
                try:
                    temp.append(float(j))
                except ValueError:
                    print("ValueError")
            weights.append(list(temp))
        self.connections.append(weights)
        wind.destroy()
        self.window.after(100, self.redraw)

    def calculate(self):
        no = 0
        for layer in self.connections:
            for i in range(len(layer)):
                for j in range(len(layer[i])):
                    self.matrix[no + 1][i] += self.matrix[no][j] * layer[i][j]
            self.normalize(self.matrix[no + 1])
            no += 1
        self.window.after(100, self.redraw)

    def normalize(self, arr):
        summ = 0.0
        for i in arr:
            summ += i
        for i in range(len(arr)):
            arr[i] /= summ
