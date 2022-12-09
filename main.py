import csv
import tkinter as tk
from tkinter import ttk
import random


class MyProgram:
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    wait_var = tk.IntVar()
    brands = []
    dicCars = {}
    dicEmis = {}
    mark_from_user = ''
    brand_from_user = ''
    fuel = ''
    engine_size = 0
    avg_km_per_year = 20000
    norm_of_co2 = 130

    def __init__(self):
        self.window.title('БЖД')
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
        with open("CO2_Emissions.csv", mode="r") as file:
            reader = list(csv.reader(file))
            temp = []
            flag = len(reader) - 1
            i = 1 #7-11
            while flag:
                j = i
                temp = []
                while reader[i][0] == reader[j][0]:
                    self.brands.append(reader[i][0])
                    if reader[j][1] not in temp and "HYBRID" not in reader[j][1].upper():
                        temp.append(reader[j][1])
                    flag -= 1
                    j += 1
                    if not flag:
                        break
                self.dicCars[reader[i][0]] = temp
                i = j
            self.brands = (list(dict.fromkeys(self.brands)))

    def get_emissions(self):
        lst = []
        with open("CO2_Emissions.csv", mode="r") as file:
            reader = list(csv.reader(file))
            for i in range(len(reader)):
                if reader[i][0].lower() == self.brand_from_user.lower() and reader[i][1].lower() == self.mark_from_user.lower() and reader[i][3].lower() == self.engine_size:
                    lst.append(reader[i][7])
                    lst.append(reader[i][8])
                    lst.append(reader[i][9])
                    lst.append(reader[i][10])
                    lst.append(reader[i][11])
                    return lst

    def get_fuel_type(self):
        with open("CO2_Emissions.csv", mode="r") as file:
            reader = list(csv.reader(file))
            for i in range(len(reader)):
                if reader[i][0].lower() == self.brand_from_user.lower() and reader[i][1].lower() == self.mark_from_user.lower() and reader[i][3].lower() == self.engine_size:
                    return reader[i][6]

    def co2_anually(self, fuel, avg):
        if fuel == "D":
            if float(avg) > 12:
                coef = random.randint(25, 29)
            else:
                coef = random.randint(24, 28)
        else:
            if float(avg) > 12:
                coef = random.randint(21, 24)
            else:
                coef = random.randint(20, 23)
        return (coef + random.random()) / 10

    def make_main_buttons(self):
        self.engine_size = 0
        brand_label = tk.Label(self.window, text='Напишите бренд Вашей машины: ')
        brand_label.grid(row=0, column=0)
        self.combo_box_brand['values'] = self.brands
        self.combo_box_brand.bind('<KeyRelease>', self.check_input_brand)
        self.combo_box_brand.grid(row=0, column=1)
        brand_label = tk.Label(self.window, text='Напишите марку Вашей машины: ', state='disabled')
        brand_label.grid(row=1, column=0)
        self.combo_box_mark.configure(state='disabled')
        self.window.wait_variable(self.wait_var)
        self.combo_box_brand.unbind('<KeyRelease>')
        brand_label.configure(state='active')
        self.combo_box_mark.configure(state='active')
        self.combo_box_mark['values'] = self.dicCars[self.brand_from_user]
        self.combo_box_mark.bind('<KeyRelease>', self.check_input_mark)
        self.combo_box_mark.grid(row=1, column=1)

    def check_input_brand(self, event):
        value = event.widget.get()
        if value == '':
            self.combo_box_brand['values'] = self.brands
        else:
            data = []
            for item in self.brands:
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
        for i in range(len(self.brands)): #проверка бренд без опечаток
            if arg.lower() in self.brands[i].lower():
                return arg

    def get_mark(self, arg):
        for i in range(len(self.dicCars[self.brand_from_user])): #проверка модели без опечаток
            if arg.lower() in self.dicCars[self.brand_from_user][i].lower():
                return arg

    def check_car(self):
        self.combo_box_brand.unbind('<KeyRelease>')
        self.combo_box_mark.unbind('<KeyRelease>')
        engines = self.check_several_engines()
        temp = tk.IntVar()
        wait = tk.IntVar()
        check_win = tk.Toplevel(self.window)
        check_win.wm_title('Проверка')
        check_win.resizable(False, False)
        app_width = 550
        app_height = 125
        x = (self.screen_width / 2) - (app_width / 2)
        y = (self.screen_height / 2) - (app_height / 2)
        check_win.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        if len(engines) > 1:
            tk.Label(check_win, text='Выберите объем двигателя:').grid(
                row=0, column=0)
            variableObj = tk.StringVar(check_win)
            variableObj.set(engines[0])
            objectMenu = tk.OptionMenu(check_win, variableObj, *engines)
            objectMenu.grid(row=0, column=1)
            check_win.bind('<KeyRelease>', lambda event: wait.set(1))
            check_win.wait_variable(wait)
            check_win.unbind('<KeyRelease>')
            self.engine_size = variableObj.get()

        if not self.engine_size:
            self.engine_size = engines[0]
        tk.Label(check_win, text=self.brand_from_user + ' ' + self.mark_from_user + ' ' + str(self.engine_size) + ' Л' +  ' - это Ваша машина?').grid(row=1, column=0)
        yes_btn = tk.Button(check_win, text='Да', command=lambda: temp.set(1))
        yes_btn.grid(row=2, column=0)
        no_btn = tk.Button(check_win, text='Нет', command=lambda: temp.set(2))
        no_btn.grid(row=2, column=1)
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

    def check_several_engines(self):
        lst = []
        with open("CO2_Emissions.csv", mode="r") as file:
            reader = list(csv.reader(file))
            for i in range(len(reader)):
                if reader[i][0].lower() == self.brand_from_user.lower() and reader[i][
                    1].lower() == self.mark_from_user.lower():
                    lst.append(reader[i][3])
        return list(dict.fromkeys(lst))

    def count(self, avg):
        coef = 0
        if self.get_fuel_type() == "D":
            coef = 43.02 * 19.98
        else:
            coef = 44.21 * 19.13
        return (self.avg_km_per_year / (2500000*float(avg))) * 0.995 * coef * (44/12)

    def get_hydrocarbons(self, fuel_type, engine_size):
        print(engine_size)
        lst = []
        nox = 0 #оксиды азота
        brakes = 0 #тормоза
        tires = 0 #шины
        if fuel_type == 'D':
            if float(engine_size) > 2.5:
                nox = 1.141
                brakes = 0.003
                tires = 0.001
            else:
                nox = 0.244
                brakes = 0.003
                tires = 0.001
        else:
            if float(engine_size) > 2.5:
                nox = 0.674
                brakes = 0.003
                tires = 0.001
            else:
                nox = 0.331
                brakes = 0.005
                tires = 0.001
        lst.append(nox)
        lst.append(brakes)
        lst.append(tires)
        return lst

    def show_info(self):
        self.combo_box_brand.configure(state='disabled')
        self.combo_box_mark.configure(state='disabled')
        temp = self.get_emissions()
        tk.Label(self.window, text='Средний расход в городе: ' + temp[0]).grid(row=4, column=0)
        tk.Label(self.window, text='Средний расход на трассе: ' + temp[1]).grid(row=5, column=0)
        tk.Label(self.window, text='Средний расход смешанный: ' + temp[2]).grid(row=6, column=0)
        tk.Label(self.window, text='Среднее количество выбросов СО2: ' + temp[4] + ' г/км').grid(row=7, column=0)
        if int(temp[4]) - self.norm_of_co2 > 0:
            tk.Label(self.window, text='Превышение выбросов СО2 на: ' + str(int(temp[4]) - self.norm_of_co2)).grid(row=8, column=0)
        co2_anually = self.co2_anually(self.get_fuel_type(), temp[2])
        self.count(temp[2])
        tk.Label(self.window, text='Среднее количество выбросов СО2: ' + str(round(co2_anually, 1)) + ' кг/л').grid(row=9, column=0)
        km_anually = self.norm_of_co2 * self.avg_km_per_year / int(temp[4])
        emis_lst = self.get_hydrocarbons(self.get_fuel_type(), self.engine_size)
        tk.Label(self.window, text='Среднее количество выбросов оксидов азота: ' + str(emis_lst[0]) + ' г/м').grid(row=10, column=0)
        tk.Label(self.window, text='Среднее количество выбросов от тормозов ' + str(emis_lst[1]) + ' г/м').grid(row=11, column=0)
        tk.Label(self.window, text='Среднее количество выбросов от шин ' + str(emis_lst[2]) + ' г/м').grid(row=12, column=0)
        tk.Label(self.window, text='Безопасное количество километров в год: ' + str(round(km_anually, 1))).grid(row=13, column=0)
        tk.Label(self.window, text='Класс опасности топлива: ' + str(4)).grid(row=14, column=0)
        tk.Button(self.window, text='Сброс', command=self.clear_all).grid(row=15, column=1)

    def clear_all(self):
        self.dicCars.clear()
        self.brands.clear()
        self.brand_from_user = ''
        self.mark_from_user = ''
        self.engine_size = 0
        self.wait_var.set(0)
        for widget in self.window.winfo_children():
            widget.destroy()
        self.combo_box_brand = ttk.Combobox(self.window)
        self.combo_box_mark = ttk.Combobox(self.window)
        self.update_dic()
        self.make_main_buttons()


program = MyProgram()
program.start()


