import numpy as np


class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self

        self.column = None
        self.row = None

        self.coord = None


class ColumnHeader(Node):
    def __init__(self, name=None):
        super().__init__()
        self.size = 0  # Number of nodes in the item
        self.name = name  # Column identifying name
        self.column = self

    def __str__(self):
        return f'{self.name} - {id(self)}'


class DancingLinks:
    def __init__(self, matrix: np.ndarray):
        self.solution = []
        self.no_of_solutions = 0
        self.all_solutions = []

        self.h = ColumnHeader("h")
        self.first_row_nodes = []


        # Create all column headers
        previous_column_nodes = []
        previous_column_header = self.h

        for i in range(len(matrix[0])):
            column_header = ColumnHeader(f'Item {i}')
            previous_column_nodes.append(column_header)

            previous_column_header.right = column_header # Link the previous column header to the current one
            column_header.left = previous_column_header # Link the current column header to the previous one
            previous_column_header = column_header

        previous_column_header.right = self.h # Link the last column header to the head
        self.h.left = previous_column_header # Link the head to the last column header


        # Create the nodes
        for row_ind, row in enumerate(matrix):
            previous_row_node = None
            first_row_node = None

            for ind, element in enumerate(row):
                if element == 0:
                    continue

                node = Node()
                node.coord = (row_ind, ind)
                column_header = previous_column_nodes[ind].column # Find column header
                
                node.column = column_header
                column_header.size += 1

                # Remember the first node in the row
                if first_row_node is None:
                    self.first_row_nodes.append(node)
                    first_row_node = node

                # Connect node with previous node in row
                if previous_row_node is not None:
                    previous_row_node.right = node
                    node.left = previous_row_node
                previous_row_node = node

                # Connect node with previous node in column
                previous_column_nodes[ind].down = node
                node.up = previous_column_nodes[ind]
                previous_column_nodes[ind] = node
        
            if previous_row_node is None: # If row has no nodes
                continue

            previous_row_node.right = first_row_node # Link first row node to last row node
            first_row_node.left = previous_row_node # Link last row node to first row node


        # Loop the columns 
        current_column = self.h.right
        for col_num in range(len(matrix[0])):            
            previous_column_nodes[col_num].down = current_column
            current_column.up = previous_column_nodes[col_num]

            current_column = current_column.right


    def cover(self, column_header: ColumnHeader):
        # Cover the column_header header
        column_header.right.left = column_header.left
        column_header.left.right = column_header.right

        # Cover all options in this column (for this item)
        current_node = column_header.down
        while current_node != column_header:

            # Cover this option
            row_node = current_node.right
            while row_node != current_node:
                row_node.column.size -= 1
                row_node.up.down = row_node.down
                row_node.down.up = row_node.up
                row_node = row_node.right

            current_node = current_node.down


    def uncover(self, column_header: ColumnHeader):
        # Uncover all options in this column (for this item)
        current_node = column_header.up
        while current_node != column_header:

            # Uncover this option
            row_node = current_node.left
            while row_node != current_node:
                row_node.up.down = row_node
                row_node.down.up = row_node
                row_node.column.size += 1
                row_node = row_node.left

            current_node = current_node.up

        # Uncover the column_header
        column_header.left.right = column_header
        column_header.right.left = column_header

    
    def choose_column(self):
        chosen_column = self.h.right

        current_column_header = self.h.right.right
        while current_column_header != self.h:

            # Check if this column has lesser nodes
            if current_column_header.size < chosen_column.size:
                chosen_column = current_column_header

            current_column_header = current_column_header.right

        return chosen_column
    

    def print_solution(self):
        for node in self.solution:
            print(f'Option {node.coord[0]}')


    def search(self, k=0, multi_solution_flag=False, pre_solution=None):
        if pre_solution is not None and k == 0:
            for row_index in pre_solution:
                row_node = self.first_row_nodes[row_index]
                self.solution.append(row_node)

                # Covering all items / columns that have been fulfilled
                current_node = row_node
                while True:
                    self.cover(current_node.column)
                    current_node = current_node.right
                    if current_node == row_node:
                        break


        # Solution found if there are no items (columns) left
        if self.h.right == self.h:
            if multi_solution_flag:
                self.no_of_solutions += 1
                self.all_solutions.append([node.coord[0] for node in self.solution])
                return False
            else:
                return True
        
        chosen_column = self.choose_column()
        self.cover(chosen_column)

        # Cycle through options of this column and include in partial solution
        current_node = chosen_column.down
        while current_node != chosen_column:

            # Including the option / row containing current_node in partial solution
            self.solution.append(current_node)

            # Covering all items / columns that have been fulfilled
            row_node = current_node.right
            while row_node != current_node:
                self.cover(row_node.column)
                row_node = row_node.right

            # Reduction to a smaller DLX problem
            if self.search(k+1, multi_solution_flag=multi_solution_flag):
                return True
            
            # Current option doesn't work - Backtrack.
            self.solution.pop()
            row_node = current_node.left
            while row_node != current_node:
                self.uncover(row_node.column)
                row_node = row_node.left

            # Try the next option for partial solution
            current_node = current_node.down

        self.uncover(chosen_column)
        return False
    

    def solve(self, pre_solution=None):
        if self.search(pre_solution=pre_solution):
            return sorted([node.coord[0] for node in self.solution])
        else:
            return False



if __name__ == '__main__':

    M = np.array([
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
    ])


    test_matrices = [
        np.array([
            [1],
        ]),
        np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]),
        np.array([
            [1, 0, 1],
            [1, 1, 0],
            [0, 1, 1],
        ]),
        np.array([
            [1, 0, 1],
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 1],
        ]),
        np.eye(10, dtype=int),
        np.array([
            [1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 1],
        ]),
        np.array([
            [1, 1],
            [1, 1],
            [0, 1],
        ]),
        np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ]),
        np.array([
            [1, 1],
            [0, 0],
            [1, 0],
            [0, 1],
            [1, 1],
        ]),
        np.array([
            [0, 0],
            [1, 0],
            [0, 1],
        ]),
    ]


    # for test_no, mtx in enumerate(test_matrices):
    #     print(f'Test {test_no}')
    #     print(mtx)
    #     dlx = DancingLinks(mtx)
    #     dlx.solve()
    #     print()
