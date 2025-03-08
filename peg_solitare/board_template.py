from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_circle_grid_pdf(filename, fill_list):
    """
    Create a PDF with a 5x4 grid of circles, some filled based on fill_list.
    
    :param filename: Name of the PDF file to create
    :param fill_list: A 5x4 list of boolean values where True means the circle is filled
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Grid properties
    rows = 5
    cols = 4
    circle_diameter = 50
    padding = 55  # space between circles

    # Starting position
    x_start = (width - (cols * circle_diameter + (cols - 1) * padding)) / 2 + 25
    y_start = height - 180

    for row in range(rows):
        for col in range(cols):
            # Calculate the position of each circle
            x = x_start + col * (circle_diameter + padding)
            y = y_start - row * (circle_diameter + padding)

            # Draw the circle (filled if specified in fill_list)
            if fill_list[row][col]:
                c.setFillColorRGB(0, 0, 0)  # Black color for filled circles
            else:
                c.setFillColorRGB(1, 1, 1)  # White color for empty circles

            # Draw circle with or without fill
            c.circle(x, y, circle_diameter / 2, fill=1 if fill_list[row][col] else 0)

            # Draw the border
            c.setStrokeColorRGB(0, 0, 0)
            c.circle(x, y, circle_diameter / 2, fill=0)

    # Save the PDF
    c.save()

# Example usage
# 5x4 grid where True means the circle should be filled
fill_list = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
]

create_circle_grid_pdf("starting_grid.pdf", fill_list)