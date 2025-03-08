from dlx import DancingLinks
import numpy as np


class Cube():
    CUBE_NUMBER = 0
    TOTAL_COLORS = ['R', 'B', 'G', 'Y']

    def __init__(self, map):
        #     4
        # 0   1   2   3
        #     5
        self.map = map
        self.number = Cube.CUBE_NUMBER
        Cube.CUBE_NUMBER += 1
        
        no_of_colors = len(set(map))
        if no_of_colors != len(Cube.TOTAL_COLORS):
            print(f"Invalid number of colors in the map. Expected {len(Cube.TOTAL_COLORS)}, got {no_of_colors}")


    def cube_rotations(self):
        """
        Generate all 24 possible rotations of the cube.
        
        Args:
        cube (list): A list of 6 elements representing cube faces 
                    in the order [left, front, right, back, top, bottom].

        Returns:
        list: A list of all 24 rotated versions of the cube.
        """
        # Helper function to rotate the cube around the "vertical axis"
        def rotate_around_vertical(cube, order):
            # Rotate the four side faces (left, front, right, back) in a given order
            return [cube[order[0]], cube[order[1]], cube[order[2]], cube[order[3]], cube[4], cube[5]]

        # All 24 rotations will be stored here
        rotations = []

        # For each face as the top, rearrange the cube:
        # Each entry represents the face that becomes [left, front, right, back, top, bottom].
        top_bottom_permutations = [
            # Top is 4, Bottom is 5
            [0, 1, 2, 3, 4, 5],
            # Top is 5, Bottom is 4
            [2, 1, 0, 3, 5, 4],
            # Top is 1, Bottom is 3
            [0, 4, 2, 5, 1, 3],
            # Top is 3, Bottom is 1
            [2, 5, 0, 4, 3, 1],
            # Top is 0, Bottom is 2
            [4, 1, 5, 3, 0, 2],
            # Top is 2, Bottom is 0
            [5, 1, 4, 3, 2, 0],
        ]

        # Define the rotation order of side faces [left, front, right, back] for 4 rotations
        side_rotation_orders = [
            [0, 1, 2, 3],  # 0 degrees
            [3, 0, 1, 2],  # 90 degrees
            [2, 3, 0, 1],  # 180 degrees
            [1, 2, 3, 0],  # 270 degrees
        ]

        # Generate all rotations
        for perm in top_bottom_permutations:
            # Rearrange the cube so the correct face is top/bottom
            reoriented_cube = [self.map[i] for i in perm]

            # Apply the four possible rotations to this configuration
            for order in side_rotation_orders:
                rotations.append(rotate_around_vertical(reoriented_cube, order))

        return rotations
    

    def __eq__(self, other):
        return any([self.map == rotation for rotation in other.cube_rotations()])


    def generate_matrix_row(self):
        out = []

        for rotation in self.cube_rotations():
            # Define new row
            row = [0 for _ in range(
                # 4 cubes identifiers +  
                # len(TOTAL_COLORS) colors, where each color has 4 tower side (west, south, east, north) required.
                4 + len(Cube.TOTAL_COLORS) * 4
            )]        
            
            # Set cube identifier
            row[self.number] = 1

            # Set color sides
            west, south, east, north = rotation[:4]
            for set_of_4_ind, color in enumerate(Cube.TOTAL_COLORS):
                if west == color:
                    row[4 + set_of_4_ind*4] = 1
                if south == color:
                    row[4 + set_of_4_ind*4 + 1] = 1
                if east == color:
                    row[4 + set_of_4_ind*4 + 2] = 1
                if north == color:
                    row[4 + set_of_4_ind*4 + 3] = 1

            out.append(row)
            # print(rotation); print(row); print()

        return np.array(out)
    

def print_solution(sol):
    for row_ind in sol:
        print(f'Cube number - {np.argmax(m[row_ind, :4]) + 1}')
        row = m[row_ind, 4:]

        row_description = [None for _ in range(4)]
        for i, color in enumerate(Cube.TOTAL_COLORS):
            if row[i*4]:
                row_description[0] = color
            if row[i*4 + 1]:
                row_description[1] = color
            if row[i*4 + 2]:
                row_description[2] = color
            if row[i*4 + 3]:
                row_description[3] = color

        print(f'{row_ind} - {row} - {row_description}')



# CUBES = [
#     Cube(['R', 'G', 'R', 'Y', 'B', 'B']),
#     Cube(['Y', 'B', 'Y', 'R', 'G', 'G']),
#     Cube(['G', 'R', 'G', 'B', 'Y', 'Y']),
#     Cube(['B', 'Y', 'B', 'G', 'R', 'R']),
# ]


CUBES = [
    Cube(list('RRBYGY')),
    Cube(list('RGGYBY')),
    Cube(list('BBYRGG')),
    Cube(list('RRRGBY')),
]


m = CUBES[0].generate_matrix_row()
for cube in CUBES[1:]:
    m = np.vstack((m, cube.generate_matrix_row()))


# Delete duplicate rows
print(f'Shape before: {m.shape}')
m = np.unique(m, axis=0)
print(f'Shape after: {m.shape}')


dl = DancingLinks(m)
dl.search(multi_solution_flag=True)
print(f'Number of solutions / 4: {dl.no_of_solutions / 4}')



