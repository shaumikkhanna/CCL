
def convert(num):
    pattern = f'{bin(num)[2:]:0>20}'
    pattern = ''.join('\u25cf' if p=='1' else '\u25ef' for p in pattern)

    out = ''
    for i in range(5):
        out += pattern[4*i:4*(i+1)] + '\n'
    return out


def backtrack():
    mylist = [
8736,
11296,
566304,
435232,
404640,
959648,
959392,
961952,
960996,
960995,
1030371,
1030642,
1030652,
1047996,
1047995,
1047039
    ]
    for i in mylist[::-1]:
        print(convert(i))
        print()


final = {
    'K': [631977],
    'H': [630425],
    '4': [630545],
    'h': [561049],
    'y': [630545],
    'd': [73630],
    'p': [499592],
    'E': [216643, 1035072],
    'Y': [630630],
    'V': [625046],
    'U': [629143],
    'L': [34958],
    'i': [8736],
    'A': [956313],
}


def find():
    mylist2 = [
(2,6038),
]


    for i in mylist2:
        print(f'H = {i[0]}, State = {i[1]}')
        print(convert(i[1]))
        print()




# find()
backtrack()



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

