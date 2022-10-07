#!/usr/bin/python3
'''
GUI extension for convert CNC prog to use from clamping palette1 (OP10) to clamping palette2 (OP20) at Grob350 with Siemens 840D control system.
-change offsets,
-change links to offsets in probing cycles,
-change subroutine calls in order to clamping palette
-change variable values in order to clamping palette
'''

import tkinter
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import sys, os, io
import Op10toOp20

class MainWindow(tkinter.Tk):
    
    def __init__(self):
        super().__init__()
        self.resizable(False, False) # not resizable main window
        self.title('Convert NC program from OP10 to OP20')# name of app
        
        # init variables, styles, widgets and geometry
        self.create_variables()
        self.create_styles()
        self.create_widgets()
        self.create_geometry()        


    def create_variables(self):
        '''
        Creates all global variables
        
        Returns
        -------
        None.

        '''
        self.input_file = tkinter.StringVar(self)   # path to file for convert
        self.input_file.set('File not selected yet.')
        self.output_file = tkinter.StringVar(self)  # path to converted file
        self.output_file.set('...')
        self.text_output = tkinter.StringVar(self)  # text output
        self.text_output.set('...\n')
        
        self.initial_dir = os.getenv('HOME')    # initial directory
    
    
    def create_styles(self):
        '''
        Define ttk widgets styles
        
        Returns
        -------
        None.

        '''
        style = ttk.Style()
        style.configure('input.TEntry', background='white', font=('Sans','9'))
    
    
    def create_widgets(self):
        '''
        Defines all widgwts

        Returns
        -------
        None.

        '''
        # Entry field for input file path
        self.entry_input_file = ttk.Entry(self, justify='right', textvariable=self.input_file, style='input.TEntry')
        # Button for run input file function
        self.choose_button = ttk.Button(self, text='Choose file', command=self.choose_file)
        # Button for run file conversion
        self.convert_button = ttk.Button(self, text='Convert file', command=self.convert_file)
        # Entry field for output file path
        self.entry_output_file = ttk.Entry(self, justify='right', textvariable=self.output_file, style='input.TEntry')
        # Button for save as file function
        self.save_as_button = ttk.Button(self, text='Save as', command=self.save_as_file)
        # Button for save file function
        self.save_button = ttk.Button(self, text=' Save ', command=self.save_file)
        # Text area for output logs
        self.text_area = ScrolledText(self, height=30, width=60, font=('Sans','10'))
        self.text_area.insert('1.0', self.text_output.get())
        # Exit app button
        self.button_exit = ttk.Button(self, text='EXIT', command=lambda: sys.exit(0))

    
    def create_geometry(self):
        '''
        Define app geometry

        Returns
        -------
        None.

        '''
        self.entry_input_file.grid(column=0, row=0, sticky='we', padx=7, pady=(7,7))
        self.choose_button.grid(column=1, row=0, sticky='e', padx=7, pady=(7,7))
        self.convert_button.grid(column=1, row=1, sticky='es', padx=7, pady=(0,14))
        self.entry_output_file.grid(column=0, row=2, sticky='we', padx=7, pady=(7,0))
        self.save_as_button.grid(column=1, row=2, sticky='e', padx=7, pady=(7,0))
        self.save_button.grid(column=1, row=3, sticky='e', padx=7, pady=(7,10))
        self.button_exit.grid(column=1, row=4, sticky='e', padx=7, pady=(7,10))
        self.text_area.grid(column=0, row=1, padx=7)


    def choose_file(self):
        '''
        Dialog to select file for conversion

        Returns
        -------
        None.

        '''
        filetypes = (('Siemens NC files', '*.MPF'),('All files', '*.*')) # define type of files for dialog window
        # raise tkinter file-selecting dialog window, returns filename path
        inputfile = filedialog.askopenfilename(title='Choose file to convert', initialdir=self.initial_dir, filetypes=filetypes)
        if inputfile != '':
            # if any filename path selected:
            inputfile = self.__path_os_sep(inputfile) # replace correct os file separator in filepath
            self.input_file.set(inputfile) # set the path to tkinter variable
            self.initial_dir = os.path.split(inputfile)[0] # extract directory from the path
            # set default output file path
            self.output_file.set(os.path.join(self.initial_dir, 'converted_' + os.path.split(inputfile)[1]))
                                 
        
    def convert_file(self):
        '''
        Perform the input file conversion

        Returns
        -------
        None.

        '''
        stdout_real = sys.stdout # set aside standard output
        stdout_buffer = io.StringIO() # make object for stdout storage
        try:
            sys.stdout = stdout_buffer # redirect stdout to storage
            self.conversion = Op10toOp20.Op10to20() # make conversion object
            self.conversion.read_changes('changes.csv') # read changes list
            if self.conversion.read_input(self.input_file.get()): # if input file reading success:
                self.conversion.convert() # do conversion
        finally:
            sys.stdout = stdout_real # stdout redirect back
            self.text_area.insert(tkinter.INSERT, stdout_buffer.getvalue()) # stdout storage into text area
            stdout_buffer.close() # close stdout storage object


    def save_as_file(self):
        '''
        Dialog to save as the converted file

        Returns
        -------
        None.

        '''
        
        filetypes = (('Siemens NC files', '*.MPF'),('All files', '*.*')) # define type of files for dialog window
        # raise tkinter save-as dialog, returns output file path
        savefile = self.__path_os_sep(filedialog.asksaveasfilename(title='Choose file to save', filetypes=filetypes))
        if savefile != '': # if any filepath selected:
            self.output_file.set(savefile) # set file path to tkinter variable
            self.save_file() # call save function

    def save_file(self):
        '''
        Saves output file

        Returns
        -------
        None.

        '''
        stdout_real = sys.stdout # set aside standard output
        stdout_buffer = io.StringIO() # make object for stdout storage
        try:
            sys.stdout = stdout_buffer # redirect stdout to storage
            self.conversion.write_output(self.output_file.get()) # call write function at conversion object
        except AttributeError:
            print('File not converted yet.') # when conversion object do not exist ( convert_file() function not called yet)
        finally:
            sys.stdout = stdout_real # stdout redirect back
            self.text_area.insert(tkinter.INSERT, stdout_buffer.getvalue()) # stdout storage into text area
            stdout_buffer.close() # close stdout storage object

   
    def __path_os_sep(self,path_string):
        '''
        Splits file path into particular components and joints them by correct os file separator again.

        Parameters
        ----------
        path_string : STRING
            Raw file path.

        Returns
        -------
        path : STRING
            File path with replaced correct os filepath separator.

        '''
        drive = os.path.splitdrive(path_string)[0] + os.sep # sepatated drive from path, if included; (for ex. C:/ in windows)
        path = os.path.splitdrive(path_string)[1] # separated path without drive
        path_components = [] # list for store path components
        while True: # create list of path component
            a = os.path.split(path)
            if a[1] == '':
                break
            path_components.append(a[1])
            path = a[0]
        path_components.reverse()            
        path = ''
        for b in path_components: # join all path components
            path = os.path.join(path, b)
        if path: path = os.path.join(drive, path) # if any path string created, add drive at the begin
        
        return path

    
if __name__ == '__main__':
    x = MainWindow()
    x.mainloop()
