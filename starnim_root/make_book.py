# from nim_logic import Board

# root = Board([3, 4, 5], split_allowed=False, limit=None)
# all_states = root.pages_required()


from starnim_logic import Starnim

root = Starnim(node_states=[0 for _ in range(9)])
all_states = root.pages_required()




for state in all_states:
    state.create_pdf()
