import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.lib.units import inch
from reportlab.lib.colors import black


PAGE_TYPE = (9*inch, 8*inch)


def draw_n_pointed_star(node_states, node_labels=None):
	"""
	Draws an n pointed star and saves it as starnim_pdfs/output.svg as an svg file.
	"""
	n = len(node_states)
	theta = np.linspace(0, 2*np.pi, n, endpoint=False)  # Angles for the vertices of a circled
	
	# Points for the star
	star_points = np.array([np.cos(theta), np.sin(theta)]).T
	
	# Define a scaling factor to position nodes further out
	scale_factor = 1.035  # Adjust this value to control how far out the nodes go

	# Scaled points for the nodes
	node_points = scale_factor * np.array([np.cos(theta), np.sin(theta)]).T  
	
	plt.figure(figsize=(9,9))
	
	# Draw connections first so they appear behind the nodes
	for i in range(n):
		first_target = (i + n//2) % n
		second_target = (i - n//2) % n
		plt.plot([star_points[i, 0], star_points[first_target, 0]], [star_points[i, 1], star_points[first_target, 1]], 'k-', linewidth=1)
		plt.plot([star_points[i, 0], star_points[second_target, 0]], [star_points[i, 1], star_points[second_target, 1]], 'k-', linewidth=1)
	
	# Draw nodes
	for i in range(n):
		if not node_states[i]:
			plt.plot(node_points[i, 0], node_points[i, 1], 'o', markersize=25, markerfacecolor='white', markeredgewidth=1, markeredgecolor='black')
			# plt.text(node_points[i, 0], node_points[i, 1], str(node_labels[i]), color='black', ha='center', va='center', fontsize=10)
	
	plt.axis('equal')
	plt.axis('off')
	plt.gca().set_facecolor('white')
	plt.savefig('starnim_pdfs/output.png', format='png')
	plt.close()


def create_pdf_with_svg(output_pdf_path, page_number, text_segments):
	# Set up the PDF canvas
	c = canvas.Canvas(output_pdf_path, pagesize=PAGE_TYPE)
	width, height = PAGE_TYPE

	# Load the SVG
	drawing = svg2rlg("starnim_pdfs/output.svg")

	# Determine maximum dimensions for the SVG on the page
	max_width = width - 2 * inch  # Assuming 1 inch margin on each side
	max_height = (height / 1.25)  # Allocating half of the page height to the SVG

	# Calculate scale factors for both dimensions
	scale_width = max_width / drawing.width
	scale_height = max_height / drawing.height

	# Use the smaller scale factor to ensure the SVG fits within the page
	scale_factor = min(scale_width, scale_height)
	drawing.width *= scale_factor
	drawing.height *= scale_factor
	drawing.scale(scale_factor, scale_factor)

	# Position the SVG centered horizontally, and adjusted from the top
	x_position = (width - drawing.width) / 2
	y_position = height - drawing.height - 0.1 * inch  # 1 inch from the top

	# Draw the SVG
	drawing.drawOn(c, x_position, y_position)

   # Text at the bottom of the page
	c.setFillColor(black)  # Set text color to black
	c.setFont("Helvetica-Bold", 12)  # Set font to Helvetica
	text_x = inch
	text_y = 1.2 * inch
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

	# Add custom page number
	c.setFont("Courier-Bold", 14)
	c.drawRightString(width / 2 + 0.7 * inch, 0.5 * inch, f"---{page_number}---")

	# Save the PDF
	c.showPage()
	c.save()



# Example usage
if __name__ == "__main__":
	svg_file = "output.svg"
	output_pdf = "output.pdf"

	my_text = [
		("Turn to page ", "regular"),
		("123\n", "bold"),
		("Okay. ", "regular"),
	]

	page_number = 123
	draw_n_pointed_star([0, 0, 0, 0, 0, 0, 0, 0, 0], list(range(10, 19)))
	# create_pdf_with_svg(output_pdf, 123, my_text)

