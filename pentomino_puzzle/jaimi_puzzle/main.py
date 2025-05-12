from dlx import DancingLinks
import pickle
import numpy as np
import itertools


with open('main_dict_full.pickle', 'rb') as f:
    main_dict = pickle.load(f)


def create_matrix(piece_numbers, m_triple):
    dancing_links_matrix = []

    # Rows that correspond to the holes
    rows_holes = [[0 for _ in range(63)] for _ in range(3)]
    rows_holes[0][m_triple[0] - 1] = 1
    rows_holes[1][m_triple[1] - 1] = 1
    rows_holes[2][m_triple[2] - 1] = 1
    dancing_links_matrix.extend(rows_holes)

    # For a given piece number, add the rows that correspond to what cells can be filled
    for shift, piece_number in enumerate(piece_numbers):
        for cells_filled in my_dict[piece_number]:

            # 63 columns for ---
            # 31 dates + 12 months + 7 days +
            # 3 always filled cells +
            # 10 for one hot encoding for piece numbers
            new_row = [0 for _ in range(53 + len(piece_numbers))]

            for cell in cells_filled:
                new_row[cell - 1] = 1

            new_row[53 + shift] = 1
            dancing_links_matrix.append(new_row)


    dancing_links_matrix = np.array(dancing_links_matrix)
    return dancing_links_matrix


def main(piece_numbers, m_triple, multi_solution_flag=False):
    dancing_links_matrix = create_matrix(piece_numbers, m_triple)
    dl = DancingLinks(dancing_links_matrix)

    if multi_solution_flag:
        dl.search(multi_solution_flag=True)
        return dl.no_of_solutions

    solution = dl.solve()

    # Show the solution
    if solution:
        for mtx_ind in solution:
            print(dancing_links_matrix[mtx_ind])
                    
        return True
    else:
        print('No solution')
        return False




my_m_triple = (6, 39, 48)
my_dict = main_dict[my_m_triple]

piece_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11]

# print(main(piece_numbers, my_m_triple, multi_solution_flag=True))

for my_m_triple, my_dict in main_dict.items():
    print(my_m_triple)
    print(main(piece_numbers, my_m_triple, multi_solution_flag=False))
    print('-'*40+'\n\n')



# Using only 6 / 8 pentominos
# for date in range(1, 32):
#     print(f'Date = {date}')
#     my_date = date
#     my_dict = main_dict[my_date]

#     no_of_solutions = 0
#     for combination in itertools.combinations(range(8), 6):
#         no_of_solutions += main(combination, my_date, multi_solution_flag=False)

    # print(f'Solution count for date {my_date} = {no_of_solutions}')
