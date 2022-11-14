import tkinter as tk
from tkinter import ttk


class MyProgram:
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    marks = [['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'q3', 'q5', 'q7', 'q8'],
            ['golf', 'polo', 'passat', 'tiguan', 'touareg']]
    emissions = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1']]
    brands = [['audi'], ['volkswagen']]
    brands_lst = ['audi', 'volkswagen']
    shortsBrands = [['ауди', 'aud', 'auid'], ['vk', 'volkwagen', 'vlokswagen', 'wagen', 'volks']]
    shortsMarks = [['а2', 'а3', 'а4', 'а5', 'а6', 'а7', 'а8'], ['гольф', 'голф', 'поло', 'полик', 'пассат']]
    dicCars = {}
    dicEmis = {}
    mark_from_user = ''
    brand_from_user = ''
    model_from_user = ''
    wait_var = tk.IntVar()

    def __init__(self):
        self.window.title('Тест')
        self.window.geometry(f'{self.screen_width}x{self.screen_height}')
        app_width = 700
        app_height = 400
        x = (self.screen_width / 2) - (app_width / 2)
        y = (self.screen_height / 2) - (app_height / 2)
        self.window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.combo_box_brand = ttk.Combobox(self.window)
        self.combo_box_mark = ttk.Combobox(self.window)
        self.update_dic()
        self.make_main_buttons()

    @staticmethod
    def start():
        MyProgram.window.mainloop()

    def update_dic(self):
        for i in range(len(self.brands)):
            self.dicCars.update(dict.fromkeys(self.brands[i], self.marks[i]))
            self.dicEmis.update(dict.fromkeys(self.marks[i], self.emissions[i][i]))

    def make_main_buttons(self):
        # lbl = tk.Label(self.window, text=(', '.join(map(str, self.dic['audi']))))
        # lbl.grid(row=0, column=0)
        brand_label = tk.Label(self.window, text='Напишите бренд Вашей машины: ')
        brand_label.grid(row=0, column=0)
        self.combo_box_brand['values'] = self.brands
        self.combo_box_brand.bind('<KeyRelease>', self.check_input_brand)
        self.combo_box_brand.grid(row=0, column=1)
        brand_label = tk.Label(self.window, text='Напишите марку Вашей машины: ', state='disabled')
        brand_label.grid(row=1, column=0)
        self.combo_box_mark.configure(state='disabled')
        self.window.wait_variable(self.wait_var)
        brand_label.configure(state='active')
        self.combo_box_mark.configure(state='active')
        self.combo_box_mark['values'] = self.dicCars[self.brand_from_user]
        self.combo_box_mark.bind('<KeyRelease>', self.check_input_mark)
        self.combo_box_mark.grid(row=1, column=1)
        # brand_entry = tk.Entry(self.window)
        # brand_entry.grid(row=0, column=1)
        # wait_var = tk.IntVar()
        # self.window.bind("<Return>", lambda event: wait_var.set(1))
        # self.window.wait_variable(wait_var)
        # self.window.unbind("<Return>")
        # self.brand_from_user = self.get_brand(brand_entry.get())
        # if self.mark_from_user != '':
        #     self.check_car()
        # else:
        #     brand_label.configure(state='disabled')
        #     mark_label = tk.Label(self.window, text='Напишите марку Вашей машины: ')
        #     mark_label.grid(row=1, column=0)
        #     mark_entry = tk.Entry(self.window)
        #     mark_entry.grid(row=1, column=1)
        #     temp_var = tk.IntVar()
        #     self.window.bind("<Return>", lambda event: temp_var.set(1))
        #     self.window.wait_variable(temp_var)
        #     self.window.unbind("<Return>")
        #     self.mark_from_user = self.get_mark(mark_entry.get())
        #     if self.mark_from_user != '':
        #         mark_label.configure(state='disabled')
        #         self.check_car()

    def check_input_brand(self, event):
        value = event.widget.get()
        if value == '':
            self.combo_box_brand['values'] = self.brands_lst
        else:
            data = []
            for item in self.brands_lst:
                if value.lower() in item.lower():
                    data.append(item)

            self.combo_box_brand['values'] = data
        if self.get_brand(self.combo_box_brand.get()) != '':
            self.brand_from_user = self.get_brand(self.combo_box_brand.get())
            if self.brand_from_user != '' and self.brand_from_user is not None:
                self.wait_var.set(1)

    def check_input_mark(self, event):
        value = event.widget.get()
        if value == '':
            self.combo_box_mark['values'] = self.dicCars[self.brand_from_user]
        else:
            data = []
            for item in self.dicCars[self.brand_from_user]:
                if value.lower() in item.lower():
                    data.append(item)

            self.combo_box_mark['values'] = data
        if self.get_mark(self.combo_box_mark.get()) != '':
            self.mark_from_user = self.get_mark(self.combo_box_mark.get())
            if self.mark_from_user != '' and self.mark_from_user is not None:
                self.check_car()

    def get_brand(self, arg):
        if ' ' in arg.lower(): #если пробел, чтобы считать и марку, и модель
            for i, val in enumerate(arg.lower()):
                if val == ' ' and i != len(arg.lower()):
                    self.mark_from_user = self.get_mark(arg.lower()[i+1:])
                    arg = arg.lower()[:i]
        for i in range(len(self.brands)): #проверка бренд без опечаток
            if arg.lower() in self.brands[i]:
                return arg
        for i in range(len(self.shortsBrands)): #проверка на опечатку
            if arg.lower() in self.shortsBrands[i]:
                return self.brands[i][0]

    def get_mark(self, arg):
        for i in range(len(self.marks)): #проверка модели без опечаток
            if arg.lower() in self.marks[i]:
                return arg
        for i in range(len(self.shortsMarks)): #проверка на опечатку не сделана
            if arg.lower() in self.shortsMarks[i]:
                return self.marks[i][0]

    def check_car(self):
        self.combo_box_brand.unbind('<KeyRelease>')
        self.combo_box_mark.unbind('<KeyRelease>')
        temp = tk.IntVar()
        check_win = tk.Toplevel(self.window)
        check_win.wm_title('Проверка')
        check_win.resizable(False, False)
        app_width = 250
        app_height = 125
        x = (self.screen_width / 2) - (app_width / 2)
        y = (self.screen_height / 2) - (app_height / 2)
        check_win.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        tk.Label(check_win, text=self.brand_from_user + ' ' + self.mark_from_user + ' - это Ваша машина?').grid(row=0, column=0)
        yes_btn = tk.Button(check_win, text='Да', command=lambda: temp.set(1))
        yes_btn.grid(row=1, column=0)
        no_btn = tk.Button(check_win, text='Нет', command=lambda: temp.set(2))
        no_btn.grid(row=1, column=1)
        check_win.wait_variable(temp)
        if temp.get() == 1:
            check_win.destroy()
            self.show_info()
        else:
            temp = tk.IntVar()
            no_win = tk.Toplevel(check_win)
            no_win.wm_title('Проверка')
            no_win.resizable(False, False)
            app_width = 250
            app_height = 75
            x = (self.screen_width / 2) - (app_width / 2)
            y = (self.screen_height / 2) - (app_height / 2)
            no_win.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
            tk.Label(no_win, text='Введите название Вашей машины еще раз').grid(row=0, column=0)
            tk.Button(no_win, text='Ок', command=lambda: temp.set(1)).grid(row=1, column=0)
            no_win.wait_variable(temp)
            no_win.destroy()
            check_win.destroy()
            self.make_main_buttons()


    def show_info(self):
        self.combo_box_brand.configure(state='disabled')
        self.combo_box_mark.configure(state='disabled')
        tk.Label(self.window, text=self.dicEmis[str(self.mark_from_user)]).grid(row=2, column=0)


program = MyProgram()
program.start()


