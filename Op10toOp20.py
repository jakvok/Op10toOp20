#!/usr/bin/python3

class Op10to20:
    '''
    Class represents CNC program at Grob350 with Siemens 840D control system.
    Convert NC prog to use from clamping palette1 (OP10) to clamping palette2 (OP20):
    -change offsets,
    -change links to offsets in probing cycles,
    -change subroutine calls in order to clamping palette
    -change variable values in order to clamping palette
    '''
    
    
    def __init__(self):
        self.changes = []   # list of substituting values, old value -> new value
        self.inputNC = []   # list of source NC prog lines
        self.outputNC = []  # list of converted NC prog lines
        self.appearance = dict()    # numbers of converted items


    def read_changes(self, filename):
        '''
        reads pairs of old-new values for replacing from file,
        file has each pair at it's own new line, values separated by comma
        '''
        try:
            with open(filename,'r',encoding='utf-8') as f:
                for a in f.readlines():
                    b, c = a.strip().split(',')
                    self.changes.append([b,c])
                    self.appearance[b]=0
        except FileNotFoundError:
            print('File with changes list not found.')
    
    
    def read_input(self, input_file):
        '''
        reads CNC program and saves each line to new list item,
        returns True when success, False when not
        '''
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
        '''
        converts NC programm
        '''
        print('Converting...')
        # goes thru all NC prog lines and searches strings to substitute
        for n in self.inputNC:
            for m in self.changes:
                if m[0] in n:
                    n = n.replace(m[0],m[1])
                    self.appearance[m[0]] += 1

            n = self._prog_nr(n)    # change NC prog number
            n = self._cycle97x(n)   # change probing cycles
            
            self.outputNC.append(n) # add converted line to output NC prog
        # print numbers of converted items
        print('Converted items:')
        for n in self.appearance.keys():
            print('{0} : {1}'.format(n, self.appearance[n]))
        
            
    def write_output(self, output_file='converted_'):
        '''
        writes converted NC prog to file,
        returns True when success, False when not
        '''
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
        '''
        increases NC prog nr. in header by 1,
        input is NC prog line string,
        returns changed line string when NC prog nr inside,
        or returns not changed string
        '''
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
        '''
        changes link to G-offset in probing cycles,
        input is NC prog line string,
        returns changed line string when probing cycle inside,
        or returns not changed string
        '''
        if 'CYCLE97' in text:
            data = ''
            x = text.index('CYCLE97') + 9
            while 1:
                if text[x] == ')': break
                data += text[x]
                x += 1
            data_new = data.split(',')
            try:
                data_new[1] = str(int(data_new[1])+2)
                print('CYCLE97x replaced...')
            except:
                print('Probing without Z.P. moving detected...')
            data_new = ','.join(data_new)
            return text.replace(data, data_new)
        return text



if __name__ == '__main__':
    print(' +------------------------------+\n',
        '| Grob G350 NC prog conversion |\n',
        '|     Op.10 to Op.20  v0.1.3   |\n',
        '|        by jakvok 2022        |\n',
        '+------------------------------+\n')
    
    while 1:    # main loop
        print()
    
        x = Op10to20()
        x.read_changes('changes.csv')   # read list of changing values
    
        while 1:    # input file for conversion
                input_file = input('Set file for conversion: ')
                if x.read_input(input_file): break
    
        x.convert() # do conversion
    
        while 1:    # input file to write changed NC prog to
                output_file = input('Set output file: ')
                if output_file:
                    if x.write_output(output_file): break
                else:
                    if x.write_output(): break
    
        print()
        if input('Continue? [Y/N]: ') in 'Nn': break