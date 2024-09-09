import cv2
import numpy as np
import random

def generate_maze(grid_size, contours, cell_size=10, wall_thickness=3):
    # Create a blank canvas for the maze
    maze = np.zeros(grid_size, dtype=np.uint8)

    # Define the grid dimensions based on cell size
    rows, cols = grid_size[0] // cell_size, grid_size[1] // cell_size

    def carve_passages(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                x, y = cx * cell_size, cy * cell_size
                nx, ny = nx * cell_size, ny * cell_size
                mid_x, mid_y = (x + nx) // 2, (y + ny) // 2

                if cv2.pointPolygonTest(contours, (mid_x, mid_y), False) >= 0 and maze[mid_y, mid_x] == 0:
                    cv2.line(maze, (x, y), (nx, ny), 255, thickness=wall_thickness)
                    carve_passages(nx // cell_size, ny // cell_size)

    # Start maze generation from a random point inside the object
    start_x, start_y = np.random.randint(0, cols) * cell_size, np.random.randint(0, rows) * cell_size
    carve_passages(start_x // cell_size, start_y // cell_size)

    return maze

def create_maze_from_image(image_path, cell_size=10, wall_thickness=3):
    # Load image and convert to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges to find contours
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour which we assume is the object
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a blank canvas for the maze
    grid_size = gray.shape
    maze = generate_maze(grid_size, largest_contour, cell_size, wall_thickness)

    # Mask the maze to fit inside the object
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    maze = cv2.bitwise_and(maze, mask)

    # Combine the maze with the original object's contour for a final effect
    final_maze = cv2.bitwise_or(edges, maze)

    # Return or save the resulting image
    return final_maze

# Example usage:
output_maze = create_maze_from_image('bstock.jpg', cell_size=200, wall_thickness=5)
cv2.imwrite('output.jpg', output_maze)