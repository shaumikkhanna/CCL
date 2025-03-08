import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def draw_board(board_str, index, ax):
    """
    Draws a Tic-Tac-Toe board from a string representation on a matplotlib axis.
    """
    # Draw grid
    for i in range(1, 3):
        ax.plot([i, i], [0, 3], color="black", linewidth=2)
        ax.plot([0, 3], [i, i], color="black", linewidth=2)
    
    # Place Xs and Os
    for i, cell in enumerate(board_str):
        row, col = divmod(i, 3)
        if cell == 'X':
            ax.text(col + 0.5, 2.5 - row, 'X', ha='center', va='center', fontsize=20, color="blue")
        elif cell == 'O':
            ax.text(col + 0.5, 2.5 - row, 'O', ha='center', va='center', fontsize=20, color="red")
    
    # Display the index below the board
    ax.text(1.5, -0.5, f"Board {index}", ha='center', va='center', fontsize=12, color="black")
    ax.axis("off")


def generate_tictactoe_pdf(board_list, output_pdf="tictactoe_boards.pdf"):
    """
    Generates a multi-page PDF of Tic-Tac-Toe boards.
    Each board in `board_list` is represented by a string of length 9.
    """
    with PdfPages(output_pdf) as pdf:
        # Parameters for layout
        boards_per_page = 12  # 4x3 layout for each page
        fig, axs = plt.subplots(4, 3, figsize=(8.5, 11))  # Standard Letter size for easy cutting
        plt.subplots_adjust(wspace=0.5, hspace=1.0)  # Increase space between boards
        
        for idx, board_str in enumerate(board_list):
            row = (idx % boards_per_page) // 3
            col = (idx % boards_per_page) % 3
            ax = axs[row, col]
            draw_board(board_str, idx, ax)
            
            # Save page after filling up boards_per_page
            if (idx + 1) % boards_per_page == 0 or (idx + 1) == len(board_list):
                # Hide any remaining empty subplots on the last page
                for empty_idx in range((idx % boards_per_page) + 1, boards_per_page):
                    fig.delaxes(axs[empty_idx // 3, empty_idx % 3])
                
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)
                fig, axs = plt.subplots(4, 3, figsize=(8.5, 11))  # Reset for a new page
                plt.subplots_adjust(wspace=0.5, hspace=1.0)  # Apply spacing again



with open('all_boards.pkl', 'rb') as f:
    all_boards = pickle.load(f)

generate_tictactoe_pdf(all_boards)
