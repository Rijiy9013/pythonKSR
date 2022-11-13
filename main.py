import tkinter as tk


class MyProgram:
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    cars = [['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'q3', 'q5', 'q7', 'q8'],
            ['golf', 'polo', 'passat', 'tiguan', 'touareg', 'superb']]
    brands = [['audi'], ['volkswagen']]
    shortsBrands = [['ауди', 'aud', 'auid'], ['vk', 'volkwagen', 'vlokswagen', 'wagen', 'volks']]
    shortsMarks = [['а2', 'а3', 'а4', 'а5', 'а6', 'а7', 'а8'], ['гольф', 'голф', 'поло', 'полик', 'пассат']]
    dic = {}
    mark_from_user = ''
    model_from_user = ''

    def __init__(self):
        self.window.title('Тест')
        self.window.geometry(f'{self.screen_width}x{self.screen_height}')
        app_width = 700
        app_height = 400
        x = (self.screen_width / 2) - (app_width / 2)
        y = (self.screen_height / 2) - (app_height / 2)
        self.window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.update_dic()
        self.make_main_buttons()

    @staticmethod
    def start():
        MyProgram.window.mainloop()

    def update_dic(self):
        for i in range(len(self.brands)):
            self.dic.update(dict.fromkeys(self.brands[i], self.cars[i]))

    def make_main_buttons(self):
        # lbl = tk.Label(self.window, text=(', '.join(map(str, self.dic['audi']))))
        # lbl.grid(row=0, column=0)
        tk.Label(self.window, text='Напишите марку машины: ').grid(row=0, column=0)
        mark_entry = tk.Entry(self.window)
        mark_entry.grid(row=0, column=1)
        wait_var = tk.IntVar()
        self.window.bind("<Return>", lambda event: wait_var.set(1))
        self.window.wait_variable(wait_var)
        self.window.unbind("<Return>")
        self.mark_from_user = self.get_mark(mark_entry.get())
        print(self.mark_from_user)

    def get_mark(self, arg):
        if ' ' in arg: #если пробел, чтобы считать и марку, и модель. добавить проверку на символ после пробела
            pass
        for i in range(len(self.brands)): #проверка бренд без опечаток
            if arg.lower() in self.brands[i]:
                return arg
        for i in range(len(self.brands)): #проверка на опечатку
            if arg.lower() in self.brands[i]:
                return arg



program = MyProgram()
program.start()


