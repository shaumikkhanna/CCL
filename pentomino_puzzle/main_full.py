from dlx import DancingLinks
import pickle
import numpy as np
import itertools


with open('main_dict_full.pickle', 'rb') as f:
    main_dict = pickle.load(f)


def create_matrix(piece_numbers, m_triple):
    dancing_links_matrix = []
    for shift, piece_number in enumerate(piece_numbers):
        for cells_filled in my_dict[piece_number]:

            # 50 columns for the 31 dates + 12 months + 7 days and one hot encoding for piece numbers
            new_row = [0 for _ in range(50 + len(piece_numbers))]

            for cell in cells_filled:
                new_row[cell + 11] = 1

            new_row[50 + shift] = 1
            dancing_links_matrix.append(new_row)


    dancing_links_matrix = np.array(dancing_links_matrix)

    # Remove columns with all zeros which are holes
    dancing_links_matrix = np.delete(dancing_links_matrix, my_mtriple[0] + 11, axis=1)
    dancing_links_matrix = np.delete(dancing_links_matrix, my_mtriple[1] + 11, axis=1)
    dancing_links_matrix = np.delete(dancing_links_matrix, my_mtriple[2] + 11, axis=1)

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
        for mtx_ind, piece_number in zip(solution, piece_numbers):
            print(f'\nPiece number = {piece_number} ---', end = ' ')
            # for ind, cell in enumerate(dancing_links_matrix[mtx_ind][:47]):
            #     pass
            print(dancing_links_matrix[mtx_ind][:47])
                    
        return True
    else:
        print('No solution')
        return False




my_mtriple = (-1, 15, 36)
my_dict = main_dict[my_mtriple]





# Using only 6 / 8 pentominos
# for date in range(1, 32):
#     print(f'Date = {date}')
#     my_date = date
#     my_dict = main_dict[my_date]

#     no_of_solutions = 0
#     for combination in itertools.combinations(range(8), 6):
#         no_of_solutions += main(combination, my_date, multi_solution_flag=False)

    # print(f'Solution count for date {my_date} = {no_of_solutions}')
