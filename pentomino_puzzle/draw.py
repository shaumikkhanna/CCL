from PIL import Image, ImageDraw, ImageFont


def create_grid_image(grid, cell_size=100, border_thickness=4, overall_border=1, output_file="grid.png"):
    """
    Create an image of a grid based on a 2D array input.

    :param grid: 2D array, where each element is a dictionary with the following keys:
                 - 'fill_color': (R, G, B) color tuple for the cell background.
                 - 'text': Text to display in the cell.
                 - 'text_color': (R, G, B) color tuple for the text (optional, default is black).
                 - 'dark_borders': List of borders to darken, e.g., ['top', 'right'].
    :param cell_size: Size of each cell (pixels).
    :param border_thickness: Thickness of the darkened borders.
    :param overall_border: Thickness of the border around the entire image.
    :param output_file: Name of the output image file.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Create the image canvas
    img_width = cols * cell_size
    img_height = rows * cell_size
    total_width = img_width + 2 * overall_border
    total_height = img_height + 2 * overall_border
    image = Image.new("RGB", (total_width, total_height), color="white")
    draw = ImageDraw.Draw(image)

    # Add an overall border
    draw.rectangle(
        [0, 0, total_width - 1, total_height - 1],
        outline="yellow",
        width=overall_border
    )

    # Try loading a font
    try:
        font = ImageFont.truetype("/Users/shaumikkhanna/Library/Fonts/Helvetica/Helvetica.ttf", int(cell_size * 0.3))
    except:
        print("Unable to load font. Using default.")
        font = ImageFont.load_default()

    # Draw grid cells
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            x1 = col * cell_size + overall_border
            y1 = row * cell_size + overall_border
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Draw cell background
            fill_color = cell.get("fill_color", (255, 255, 255))
            draw.rectangle([x1, y1, x2, y2], fill=fill_color)

            # Add text to the cell
            text = cell.get("text", "")
            text_color = cell.get("text_color", "black")
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x1 + (cell_size - text_width) / 2
            text_y = y1 + (cell_size - text_height) / 2 - 5
            draw.text((text_x, text_y), text, fill=text_color, font=font)

            # Draw darkened borders
            dark_borders = cell.get("dark_borders", [])
            border_color = "#07155b" # BORDER COLOR
            if "top" in dark_borders:
                draw.rectangle([x1, y1, x2, y1 + border_thickness], fill=border_color)
            if "right" in dark_borders:
                draw.rectangle([x2 - border_thickness, y1, x2, y2], fill=border_color)
            if "bottom" in dark_borders:
                draw.rectangle([x1, y2 - border_thickness, x2, y2], fill=border_color)
            if "left" in dark_borders:
                draw.rectangle([x1, y1, x1 + border_thickness, y2], fill=border_color)

    # Save the image
    image.save(output_file)
    print(f"Grid image saved as {output_file}")


def process_input(input_):
    lines = input_.strip().split("\n")
    out = dict()

    for line in lines:
        parts = line.split(" --- ")
        piece_number = int(parts[0].split()[-1])
        for x in parts[1].split():
            out[int(x)] = piece_number

    return out


def build_grid(piece_mapping):
    grid = []
    for row_number in range(4):
        row = []
        for column_number in range(7):
            if (7*row_number + column_number + 1) % 2 == 0:
                row.append({"value": 0, "fill_color": 'white', "text": "", "text_color": 'black', "dark_borders": []})
            else:
                row.append({"value": 0, "fill_color": 'gray', "text": "", "text_color": 'white', "dark_borders": []})
        grid.append(row)

    last_row = [{"value": -1, "fill_color": '#07155b', "text": "", "text_color": 'white', "dark_borders": []} for _ in range(4)]
    last_row.extend([
        {"value": 0, "fill_color": 'gray', "text": "", "text_color": 'white', "dark_borders": []},
        {"value": 0, "fill_color": 'white', "text": "", "text_color": 'black', "dark_borders": []},
        {"value": 0, "fill_color": 'gray', "text": "", "text_color": 'white', "dark_borders": []},
        ])
    
    grid.append(last_row)

    for date in range(1, 32):
        row, col = divmod(date - 1, 7)
        if row == 4:
            col = col + 4

        try:
            grid[row][col]["value"] = piece_mapping[date]
        except KeyError:
            grid[row][col]["fill_color"] = '#07155b'
            grid[row][col]["text"] = f'{date}'
            grid[row][col]["text_color"] = 'white'
            grid[row][col]["dark_borders"] = ['top', 'right', 'bottom', 'left']

    return grid


def create_sections(grid):
    """
    Adds a border between any 2 cells that do not have the same value.
    """
    for row in range(5):
        for col in range(7):
            if col < 6 and grid[row][col]["value"] != grid[row][col + 1]["value"]:
                grid[row][col]["dark_borders"].append("right")
                grid[row][col + 1]["dark_borders"].append("left")
            if row < 4 and grid[row][col]["value"] != grid[row + 1][col]["value"]:
                grid[row][col]["dark_borders"].append("bottom")
                grid[row + 1][col]["dark_borders"].append("top")
    
    return grid


# Example input
results = [
"""
Piece number = 1 --- 4 5 6 7 13 
Piece number = 2 --- 10 11 12 18 25 
Piece number = 3 --- 19 20 26 27 29 
Piece number = 4 --- 2 3 9 16 17 
Piece number = 5 --- 8 15 22 23 24 
Piece number = 7 --- 14 21 28 30 31
""",
"""
Piece number = 0 --- 7 12 13 14 19 
Piece number = 1 --- 24 25 26 27 29 
Piece number = 3 --- 3 9 10 16 17 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 5 --- 4 5 6 11 18 
Piece number = 7 --- 1 8 15 22 23
""",
"""
Piece number = 0 --- 7 12 13 14 19 
Piece number = 1 --- 24 25 26 27 29 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 5 --- 2 9 16 17 18 
Piece number = 6 --- 4 5 6 10 11 
Piece number = 7 --- 1 8 15 22 23
""",
"""
Piece number = 1 --- 18 19 20 21 27 
Piece number = 2 --- 3 10 11 12 17 
Piece number = 3 --- 5 6 7 13 14 
Piece number = 4 --- 26 28 29 30 31 
Piece number = 5 --- 9 16 23 24 25 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 1 --- 24 25 26 27 29 
Piece number = 2 --- 4 11 17 18 19 
Piece number = 3 --- 6 7 12 13 14 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 5 --- 1 2 3 8 15
""",
"""
Piece number = 0 --- 7 12 13 14 19 
Piece number = 1 --- 24 25 26 27 29 
Piece number = 2 --- 3 4 5 11 18 
Piece number = 3 --- 2 9 10 16 17 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 7 --- 1 8 15 22 23
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 2 --- 4 5 6 12 19 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 5 --- 1 2 3 8 15 
Piece number = 6 --- 13 20 26 27 29 
Piece number = 7 --- 14 21 28 30 31
""",
"""
Piece number = 1 --- 10 11 12 13 18 
Piece number = 2 --- 1 2 3 9 16 
Piece number = 3 --- 19 20 21 27 28 
Piece number = 4 --- 15 17 22 23 24 
Piece number = 6 --- 25 26 29 30 31 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 1 --- 24 25 26 27 29 
Piece number = 3 --- 8 15 16 22 23 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 5 --- 1 2 3 10 17 
Piece number = 6 --- 12 13 14 18 19 
Piece number = 7 --- 4 5 6 7 11
""",
"""
Piece number = 0 --- 1 2 9 16 17 
Piece number = 3 --- 5 6 12 13 19 
Piece number = 4 --- 26 28 29 30 31 
Piece number = 5 --- 8 15 22 23 24 
Piece number = 6 --- 7 14 20 21 27 
Piece number = 7 --- 3 4 11 18 25
""",
"""
Piece number = 1 --- 18 23 24 25 26 
Piece number = 2 --- 4 5 6 12 19 
Piece number = 3 --- 3 9 10 16 17 
Piece number = 5 --- 21 28 29 30 31 
Piece number = 6 --- 7 13 14 20 27 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 1 --- 1 8 9 15 22 
Piece number = 3 --- 21 27 28 30 31 
Piece number = 4 --- 2 3 10 16 17 
Piece number = 5 --- 11 18 23 24 25 
Piece number = 6 --- 13 19 20 26 29 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 2 --- 4 5 6 12 19 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 4 --- 26 28 29 30 31 
Piece number = 5 --- 1 2 3 8 15 
Piece number = 6 --- 7 14 20 21 27
""",
"""
Piece number = 1 --- 12 18 19 26 29 
Piece number = 2 --- 5 6 7 13 20 
Piece number = 3 --- 21 27 28 30 31 
Piece number = 4 --- 10 11 17 24 25 
Piece number = 5 --- 2 3 4 9 16 
Piece number = 7 --- 1 8 15 22 23
""",
"""
Piece number = 2 --- 9 16 22 23 24 
Piece number = 3 --- 11 12 13 19 20 
Piece number = 4 --- 1 2 3 8 10 
Piece number = 5 --- 21 28 29 30 31 
Piece number = 6 --- 17 18 25 26 27 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 0 --- 11 12 18 24 25 
Piece number = 1 --- 4 5 6 7 13 
Piece number = 3 --- 19 20 26 27 29 
Piece number = 4 --- 8 9 15 22 23 
Piece number = 5 --- 1 2 3 10 17 
Piece number = 7 --- 14 21 28 30 31
""",
"""
Piece number = 0 --- 11 12 18 24 25 
Piece number = 1 --- 4 5 6 7 13 
Piece number = 2 --- 14 19 20 21 28 
Piece number = 3 --- 26 27 29 30 31 
Piece number = 6 --- 3 9 10 16 23 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 1 --- 1 8 9 15 22 
Piece number = 3 --- 4 5 6 11 12 
Piece number = 4 --- 2 3 10 16 17 
Piece number = 5 --- 21 28 29 30 31 
Piece number = 6 --- 7 13 14 20 27 
Piece number = 7 --- 19 23 24 25 26
""",
"""
Piece number = 0 --- 13 14 20 26 27 
Piece number = 1 --- 4 5 6 7 12 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 5 --- 21 28 29 30 31 
Piece number = 6 --- 3 9 10 16 23 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 1 --- 4 5 6 7 12 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 4 --- 13 14 21 27 28 
Piece number = 5 --- 19 26 29 30 31 
Piece number = 6 --- 3 9 10 16 23 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 2 --- 4 5 6 12 19 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 4 --- 26 28 29 30 31 
Piece number = 5 --- 1 2 3 8 15 
Piece number = 6 --- 7 13 14 20 27
""",
"""
Piece number = 0 --- 7 12 13 14 19 
Piece number = 1 --- 24 25 26 27 29 
Piece number = 3 --- 1 2 8 9 15 
Piece number = 4 --- 20 21 28 30 31 
Piece number = 5 --- 4 5 6 11 18 
Piece number = 6 --- 3 10 16 17 23
""",
"""
Piece number = 0 --- 11 12 18 24 25 
Piece number = 1 --- 1 8 9 15 22 
Piece number = 3 --- 21 27 28 30 31 
Piece number = 4 --- 2 3 10 16 17 
Piece number = 6 --- 13 19 20 26 29 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 1 --- 4 11 17 18 25 
Piece number = 3 --- 9 15 16 22 23 
Piece number = 4 --- 1 2 3 8 10 
Piece number = 5 --- 5 6 7 12 19 
Piece number = 6 --- 13 20 26 27 29 
Piece number = 7 --- 14 21 28 30 31
""",
"""
Piece number = 1 --- 3 9 10 11 12 
Piece number = 3 --- 13 19 20 26 27 
Piece number = 4 --- 1 2 8 15 16 
Piece number = 5 --- 21 28 29 30 31 
Piece number = 6 --- 17 18 22 23 24 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 1 --- 4 5 6 7 12 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 4 --- 19 20 27 29 30 
Piece number = 5 --- 1 2 3 8 15 
Piece number = 7 --- 13 14 21 28 31
""",
"""
Piece number = 0 --- 9 10 16 22 23 
Piece number = 1 --- 4 5 6 7 12 
Piece number = 3 --- 11 17 18 24 25 
Piece number = 4 --- 19 20 26 29 30 
Piece number = 5 --- 1 2 3 8 15 
Piece number = 7 --- 13 14 21 28 31
""",
"""
Piece number = 2 --- 20 27 29 30 31 
Piece number = 3 --- 17 18 19 25 26 
Piece number = 4 --- 9 10 16 23 24 
Piece number = 5 --- 5 6 7 14 21 
Piece number = 6 --- 3 4 11 12 13 
Piece number = 7 --- 1 2 8 15 22
""",
"""
Piece number = 0 --- 12 19 20 21 28 
Piece number = 1 --- 1 8 15 16 22 
Piece number = 3 --- 5 6 7 13 14 
Piece number = 4 --- 9 10 17 23 24 
Piece number = 5 --- 2 3 4 11 18 
Piece number = 6 --- 25 26 27 30 31
""",
"""
Piece number = 1 --- 16 17 18 19 25 
Piece number = 3 --- 1 2 3 9 10 
Piece number = 4 --- 26 27 28 29 31 
Piece number = 5 --- 8 15 22 23 24 
Piece number = 6 --- 11 12 13 20 21 
Piece number = 7 --- 4 5 6 7 14
""",
"""
Piece number = 1 --- 13 20 27 28 30 
Piece number = 2 --- 19 24 25 26 29 
Piece number = 3 --- 2 3 4 9 10 
Piece number = 5 --- 5 6 7 14 21 
Piece number = 6 --- 11 12 16 17 18 
Piece number = 7 --- 1 8 15 22 23
"""
]

result_grids = []

for i, result in enumerate(results):
    piece_mapping = process_input(result)
    grid = create_sections(build_grid(piece_mapping))
    result_grids.append(grid)
    create_grid_image(grid, output_file=f"final_images/grid_{i+1}.png")

