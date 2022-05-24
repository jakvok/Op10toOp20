#!/usr/bin/python3
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
    
    
    def read_input(self, input_file):
        self.input_file = input_file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                for e in f.readlines():
                    self.inputNC.append(e.strip())
            return True
        except FileNotFoundError:
            print('Input file not found.')
            return False


    def convert(self):
        print('Converting...')
        for n in self.inputNC:
            for m in self.changes:
                if m[0] in n:
                    n = n.replace(m[0],m[1])
                    self.appearance[m[0]] += 1

            n = self._prog_nr(n)
            n = self._cycle97x(n)
            
            self.outputNC.append(n)
        print('Converted items:')
        for n in self.appearance.keys():
            print('{0} : {1}'.format(n, self.appearance[n]))
        
            
    def write_output(self, output_file='converted_'):
        if output_file == 'converted_':
            output_file += self.input_file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for n in self.outputNC:
                    f.write(n + '\n')
            print('Output file <{}> wrote successfuly.'.format(output_file))
        except:
            print('Write to output file failed.')
            return False
        return True


    def _prog_nr(self, text):
        if '%_N_' in text:
            prog_nr = ''
            x = text.index('%_N_') + 4
            for n in text[(x):(x+4)]:
                if n.isdigit(): prog_nr += n
            prog_nr = int(prog_nr) + 1
            print('Prog number changed...')
            return text[:(x)] + str(prog_nr) + text[(x+len(str(prog_nr))):]
        return text


    def _cycle97x(self, text):
        if 'CYCLE97' in text:
            data = ''
            x = text.index('CYCLE97') + 9
            while 1:
                if text[x] == ')': break
                data += text[x]
                x += 1
            data_new = data.split(',')
            data_new[1] = str(int(data_new[1])+2)
            data_new = ','.join(data_new)
            print('CYCLE97x replaced...')
            return text.replace(data, data_new)

        return text   


print(' +------------------------------+\n',
    '| Grob G350 NC prog conversion |\n',
    '|        Op.10 to Op.20        |\n',
    '|        by jakvok 2022        |\n',
    '+------------------------------+\n')

while 1:
    print()

    x = Op10to20()
    x.read_changes('changes.csv')

    while 1:
            input_file = input('Set file for conversion: ')
            if x.read_input(input_file): break

    x.convert()

    while 1:
            output_file = input('Set output file: ')
            if output_file:
                if x.write_output(output_file): break
            else:
                if x.write_output(): break

    print()
    if input('Continue? [Y/N]: ') in 'Nn': break