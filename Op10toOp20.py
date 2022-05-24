# -*- coding: utf-8 -*-
"""
Script to convert NC prog from OP10 to OP20 at Grob350
"""

class Op10to20:
    
    
    def __init__(self):
        self.changes = []
        self.inputNC = []
        self.outputNC = []
        self.appearance = dict()


    def read_changes(self, filename):
        try:
            with open(filename,'r',encoding='utf-8') as f:
                for a in f.readlines():
                    b, c = a.strip().split(',')
                    self.changes.append([b,c])
                    self.appearance[b]=0
        except FileNotFoundError:
            print('File with changes list not found.')
    
    
    def read_input(self):
        while 1:
            try:
                self.input_file = input('Set file for conversion: ')
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    for e in f.readlines():
                        self.inputNC.append(e.strip())
                break
            except FileNotFoundError:
                print('Input file not found.')


    def convert(self):
        for n in self.inputNC:
            for m in self.changes:
                if m[0] in n:
                    n = n.replace(m[0],m[1])
                    self.appearance[m[0]] += 1
            self.outputNC.append(n)
        
            
    def write_output(self, output_file='converted_'):
        if output_file == 'converted_':
            output_file += self.input_file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for n in self.outputNC:
                    f.write(n + '\n')
        except:
            print('Write to output file failed.')
        
        print('Converted items:')
        for n in self.appearance.keys():
            print('{0} : {1}'.format(n, self.appearance[n]))

    def _prog_nr(self, text):
        if '%_N_' in text:
            x = text.index('%_N_')


x = Op10to20()
x.read_changes('changes.csv')
x.read_input()
x.convert()
x.write_output('0030.MPF')


print('changes.csv:\n', x.changes)
