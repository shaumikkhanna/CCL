from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black


PAGE_TYPE = (9*inch, 7*inch)

def create_pdf(output_pdf_path, circles_per_row, text_segments):
	# Create a canvas object
	c = canvas.Canvas(output_pdf_path, pagesize=PAGE_TYPE)
	width, height = PAGE_TYPE

	# Set white background
	c.setFillColorRGB(1, 1, 1)
	c.rect(0, 0, width, height, fill=1)

	# Rectangle dimensions and position
	rect_width = 6.5 * inch
	rect_height = 4 * inch
	rect_x = (width - rect_width) / 2
	rect_y = (height - rect_height) / 2 + 75

	# Draw the rectangle
	c.setStrokeColorRGB(0, 0, 0)
	c.setFillColorRGB(1, 1, 1)
	c.rect(rect_x, rect_y, rect_width, rect_height, fill=0)

	# Circle properties
	circle_radius = 0.5 * inch
	padding = 0.25 * inch
	start_x = rect_x + padding + circle_radius
	start_y = rect_y + rect_height - padding - circle_radius

	# Draw circles in specified rows
	for row, num_circles in enumerate(circles_per_row):
		for col in range(num_circles):
			x = start_x + col * (2 * circle_radius + padding)
			y = start_y - row * (2 * circle_radius + padding)
			c.circle(x, y, circle_radius)

	# Text at the bottom of the page
	c.setFillColor(black)  # Set text color to black
	c.setFont("Helvetica-Bold", 12)  # Set font to Helvetica
	text_x = inch
	text_y = 1.4 * inch  # Adjusted Y position to be slightly higher
	line_height = 0.1 * inch
	
	for line in text_segments:
		text, style = line
		if "\n" in text:
			text_parts = text.split('\n')
			for part in text_parts:
				if style == "regular":
					c.setFont("Helvetica", 12)
				elif style == "bold":
					c.setFont("Helvetica-Bold", 12)
				elif style == "italic":
					c.setFont("Helvetica-Oblique", 12)
				elif style == "bold_italic":
					c.setFont("Helvetica-BoldOblique", 12)

				c.drawString(text_x, text_y, part)
				text_y -= line_height
				text_x = inch  # Reset x to start of the line for new line
		else:
			if style == "regular":
				c.setFont("Helvetica", 12)
			elif style == "bold":
				c.setFont("Helvetica-Bold", 12)
			elif style == "italic":
				c.setFont("Helvetica-Oblique", 12)
			elif style == "bold_italic":
				c.setFont("Helvetica-BoldOblique", 12)

			c.drawString(text_x, text_y, text)
			text_x += c.stringWidth(text, "Helvetica", 12)  # Move x for next segment


	# Custom page number
	page_number_text = f"--- {''.join(str(x) for x in sorted(circles_per_row))} ---"
	c.setFont("Courier-Bold", 14)
	c.drawCentredString(width / 2, 0.75 * inch, page_number_text)

	# Save the PDF
	c.showPage()
	c.save()


def main(pile):
	circles_per_row = pile  # Specify the number of circles in each row

	my_text = [
		("Turn to page ", "regular"),
		("123\n", "bold"),
		("Or otherwise at the ", "regular"),
		("bottom of the page.\n", "italic"),
		("This text looks ", "regular"),
		("so good.", "bold_italic"),
	]

	create_pdf("output.pdf", circles_per_row, my_text)

if __name__ == "__main__":
	main([5, 5, 5])

