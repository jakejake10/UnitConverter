import tkinter as tk


MeasureOpts = {'Volume': {'Gallons': 0.0634013, 'US Fluid Ounces': 8, 'Pints': 0.50721, 'Quarts': 0.253605,
                          'Cups': 1, 'Tablespoons': 16, 'Teaspoons': 48,
                          'Liters': 0.24, 'Mililiters': 236.588, 'Cubic Feet': 0.00835503, 'Cubic Inches': 14.4375},
               'Length': {'Miles': 0.00018939399999999995561, 'Yards': 0.33333343999999998086,  'Feet': 1, 'Inches': 12,
                          'Kilometers': 0.000304800097536, 'Meters': 0.3048, 'Centimeters': 30.48, 'Millimeters': 304.8, 'Micrometers': 304800},
               'Mass': {'Pounds': 1, 'Ounces': 16, 'Kilograms': 0.453592, 'Grams': 453.592, 'Milligram': 453592},
               }


class unitApp(tk.Frame):
    inst_num = 0

    unit_type_vars = []
    unit_selection_vars = []

    pm_buttons = []
    eq_labels = []
    entry_widgets = []
    unit_type_menus = []
    unit_selection_menus = []

    def __init__(self):
        self.root = tk.Tk()
        tk.Frame.__init__(self, self.root)
        self.root.title("UnitConverter")
        self.root.minsize(200, 30)
        self.root.wm_attributes("-topmost", 1)
        self.root.resizable(width=False, height=False)
        self.grid(padx=4, pady=4)

        self.new_row()

    def new_row(self):
        i_num = self.inst_num
        if self.inst_num == 0:
            self.pm_buttons.append(tk.Button(self, text="+", command=self.new_row))
            self.pm_buttons[-1].grid(row=self.inst_num, column=0)
        else:
            self.pm_buttons.append(tk.Button(self, text="-", command=lambda: self.destroy_row(i_num)))
            self.pm_buttons[-1].grid(row=self.inst_num, column=0)

        self.create_unit_type_widget()
        self.create_unit_widget(2)
        self.create_entry_widget(3)
        self.create_equals()
        self.create_unit_widget(5)
        self.create_entry_widget(6)

        self.unit_type_vars[-1].set('Volume')  # default value

        self.inst_num += 1

    def destroy_row(self, i_num):
        self.pm_buttons[i_num].destroy()
        self.unit_type_menus[i_num].destroy()
        self.entry_widgets[i_num*2].destroy()
        self.unit_selection_menus[i_num*2].destroy()
        self.eq_labels[i_num].destroy()
        self.entry_widgets[i_num*2+1].destroy()
        self.unit_selection_menus[i_num*2+1].destroy()

    def create_unit_type_widget(self):
        self.unit_type_vars.append(tk.StringVar())
        self.unit_type_vars[-1].trace('w', lambda a,b,c,i_num=self.inst_num: self.update_options(i_num))

        self.unit_type_menus.append(tk.OptionMenu(self, self.unit_type_vars[-1], *MeasureOpts.keys()))
        self.unit_type_menus[-1].grid(row=self.inst_num, column=1)

    def create_unit_widget(self, colNum):
        self.unit_selection_vars.append(tk.StringVar())

        self.unit_selection_menus.append(tk.OptionMenu(self, self.unit_selection_vars[-1], ''))
        self.unit_selection_menus[-1].grid(row=self.inst_num, column=colNum)

    def create_entry_widget(self, colNum):
        e_num = len(self.entry_widgets)
        self.entry_widgets.append(tk.Entry(self, width=20))
        self.entry_widgets[-1].bind('<Return>', lambda event: self.hit_enter(self, e_num))
        self.entry_widgets[-1].grid(row=self.inst_num, column=colNum)

    def create_equals(self):
        self.eq_labels.append(tk.Label(self))
        self.eq_labels[-1].configure(text=' = ', font=(None, 15))
        self.eq_labels[-1].grid(row=self.inst_num, column=4)

    def update_options(self, i_num, *args):
        units = MeasureOpts[self.unit_type_vars[i_num].get()]
        u_num = i_num*2
        self.unit_selection_vars[u_num].set(next(iter(units)))
        self.unit_selection_vars[u_num+1].set(next(iter(units)))

        menu = self.unit_selection_menus[u_num]['menu']
        menu.delete(0, 'end')
        for k, v in units.items():
            menu.add_command(label=k, command=lambda newUnit=k: self.unit_selection_vars[u_num].set(newUnit))

        menu = self.unit_selection_menus[u_num+1]['menu']
        menu.delete(0, 'end')
        for k, v in units.items():
            menu.add_command(label=k, command=lambda newUnit=k: self.unit_selection_vars[u_num+1].set(newUnit))

    def hit_enter(self, event, active_entry):
        affected_entry = self.entry_widgets[self.opp(active_entry)]
        # print(active_entry)
        # print(len(self.unit_selections))

        val = self.entry_widgets[active_entry].get()
        calcVal = self.calc(val, active_entry)
        affected_entry.delete(0, tk.END)
        affected_entry.insert(0, calcVal)

    def calc(self, val_in, entry_index):
        if entry_index % 2 == 0:
            type_index = entry_index/2
        else:
            type_index = (entry_index-1)/2
        type_index = int(round(type_index))

        active_part = self.unit_selection_vars[entry_index].get()
        active_part = MeasureOpts[self.unit_type_vars[type_index].get()][active_part]
        goal_part = self.unit_selection_vars[self.opp(entry_index)].get()
        goal_part = MeasureOpts[self.unit_type_vars[type_index].get()][goal_part]

        val_out = (float(val_in) * goal_part)/active_part
        val_out = round(val_out, 2)
        return val_out

    def opp(self, val_in):
        if val_in % 2 == 0:
            val_out = val_in + 1
        else:
            val_out = val_in - 1
        return val_out

    def start(self):
        self.root.mainloop()


unitApp().start()
