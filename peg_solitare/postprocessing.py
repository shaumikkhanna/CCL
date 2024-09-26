
def convert(num):
    pattern = f'{bin(num)[2:]:0>20}'
    pattern = ''.join('\u25cf' if p=='1' else '\u25ef' for p in pattern)

    out = ''
    for i in range(5):
        out += pattern[4*i:4*(i+1)] + '\n'
    return out


mylist = [
(1,634281),
(1,631977),
(2,633889),
(2,76969),
(2,601129),
(2,535721),
(2,633896),
(2,637993),
(2,601273),
]



final = {
    'K': [631977]
}



for i in mylist:
    print(f'H = {i[0]}')
    print(convert(i[1]))
    print()

# with open('patterns_5x4.txt', 'w') as g:
#     with open('file.txt', 'r') as f:
#         for line in f.readlines():

#             num = int(line.strip())
#             g.write(f'{num}\n')
            
#             pattern = f'{bin(num)[2:]:0>20}'
#             g.write(f'{pattern}\n')
            
#             for i in range(5):
#                 g.write(f'{pattern[4*i:4*(i+1)]}\n')
            
#             g.write('\n')

