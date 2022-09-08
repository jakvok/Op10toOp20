#!/usr/bin/python3

import tkinter
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import sys, os
import Op10toOp20

class MainWindow(tkinter.Tk):
    
    def __init__(self):
        super().__init__()
        #self.minsize(510,210) # dimmensions of main window
        self.resizable(False, False) # not resizable main window
        self.title('Convert NC program from OP10 to OP20')# name of app
        
        # init variables, styles, widgets and geometry
        self.create_variables()
        self.create_styles()
        self.create_widgets()
        self.create_geometry()        


    def create_variables(self):
        self.input_file = tkinter.StringVar(self)
        self.input_file.set('File not selected yet.')
        self.output_file = tkinter.StringVar(self)
        self.output_file.set('...')
        self.text_output = tkinter.StringVar(self)
        self.text_output.set('...')
        
        self.initial_dir = os.getenv('HOME')
    
    
    def create_styles(self):
        style = ttk.Style()
        style.configure('input.TEntry', background='white', font=('Sans','9'))
    
    
    def create_widgets(self):
        self.entry_input_file = ttk.Entry(self, width=70, justify='left', textvariable=self.input_file, style='input.TEntry')
        #self.entry_input_file.xview_moveto(1)
        self.choose_button = ttk.Button(self, text='Choose file', command=self.choose_file)
        self.convert_button = ttk.Button(self, text='Convert file', command=self.convert_file)
        self.entry_output_file = ttk.Entry(self, width=70, justify='right', textvariable=self.output_file, style='input.TEntry')
        self.save_as_button = ttk.Button(self, text='Save as', command=self.save_as_file)
        self.save_button = ttk.Button(self, text=' Save ', command=self.save_file)
        self.text_area = ScrolledText(self, height=15, width=50)
        self.text_area.insert('1.0', self.text_output.get())
        self.text_area.insert('2.0', '\nooo')

    
    def create_geometry(self):
        self.entry_input_file.grid(column=0, row=0, sticky='w', padx=7, pady=(7,7))
        self.choose_button.grid(column=1, row=0, sticky='e', padx=10)
        self.convert_button.grid(column=1, row=1, sticky='s', padx=7, pady=(7,7))
        self.entry_output_file.grid(column=0, row=2, sticky='w', padx=7, pady=(7,0))
        self.save_as_button.grid(column=1, row=2, sticky='e', padx=7, pady=(7,0))
        self.save_button.grid(column=1, row=3, sticky='e', padx=7, pady=(7,10))
        self.text_area.grid(column=0, row=1, padx=7)
    
    def choose_file(self):
        filetypes = (('Siemens NC files', '*.MPF'),('All files', '*.*'))
        save_dir = self.input_file.get()
        self.input_file.set(filedialog.askopenfilename(title='Choose file to convert', initialdir=self.initial_dir, filetypes=filetypes))
        if self.input_file.get() == '':
            self.input_file.set(save_dir)
        else:
            path_components = []
            n = self.input_file.get()
            drive = os.path.splitdrive(n)[0] + os.sep
            n = os.path.splitdrive(n)[1]
            while True:
                a = os.path.split(n)
                if a[1] == '':
                    break
                path_components.append(a[1])
                n = a[0]
            #path_components.append(drive)
            path_components.reverse()
            print('_3_', path_components)
            
            path = ''
            for b in path_components:
                path = os.path.join(path, b)
                
            self.input_file.set(os.path.join(drive, path))
            self.initial_dir = os.path.split(self.input_file.get())[0]

            self.output_file.set(os.path.join(self.initial_dir, 'converted_' + os.path.split(self.input_file.get())[1]))
        
        
    def convert_file(self):
        pass


    def save_as_file(self):
        pass

    def save_file(self):
        pass



class uniPath():
    
    def __init__(self, input_path):
        self.input_path = input_path
        path_components = []
        n = self.input_path
        print('uniPath _input_path_: ', self.input_path)
        while n:
            a = os.path.split(n)
            print('uniPath _a_:', a )
            path_components.append(a[1])
            n = a[0]
        path_components.reverse()
        self.path = ''
        for b in path_components:
            self.path = os.path.join(self.path, b)
        
'''
a = uniPath('aaa/bbb/ccc/ghyrht.txt')
print(a.path)
'''

    

x = MainWindow()
x.mainloop()