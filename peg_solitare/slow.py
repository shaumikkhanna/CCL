from collections import deque




def generate_moves(rows, cols):
	moves = []
	for r in range(rows):
		for c in range(cols):
			from_idx = r * cols + c
			# Move Up
			if r >= 2:
				over_idx = (r - 1) * cols + c
				to_idx = (r - 2) * cols + c
				moves.append((from_idx, over_idx, to_idx))
			# Move Down
			if r <= rows - 3:
				over_idx = (r + 1) * cols + c
				to_idx = (r + 2) * cols + c
				moves.append((from_idx, over_idx, to_idx))
			# Move Left
			if c >= 2:
				over_idx = r * cols + (c - 1)
				to_idx = r * cols + (c - 2)
				moves.append((from_idx, over_idx, to_idx))
			# Move Right
			if c <= cols - 3:
				over_idx = r * cols + (c + 1)
				to_idx = r * cols + (c + 2)
				moves.append((from_idx, over_idx, to_idx))
	return moves


def serialize_state(state):
	# Convert the list of bits to an integer
	result = 0
	for bit in state:
		result = (result << 1) | bit
	return result


def deserialize_state(num, size):
	# Convert integer back to list of bits
	state = []
	for _ in range(size):
		state.append(num & 1)
		num >>= 1
	return list(reversed(state))


def is_reachable(start_state, end_state):
	rows, cols = 7, 5
	total_positions = rows * cols
	moves = generate_moves(rows, cols)
	visited = set()
	queue = deque()

	start_num = serialize_state(start_state)
	end_num = serialize_state(end_state)

	queue.append(start_num)
	visited.add(start_num)

	while queue:
		current = queue.popleft()
		if current == end_num:
			return True

		# For each possible move
		for from_idx, over_idx, to_idx in moves:
			# Check if move is valid
			# Extract bits
			from_bit = (current >> (total_positions - 1 - from_idx)) & 1
			over_bit = (current >> (total_positions - 1 - over_idx)) & 1
			to_bit = (current >> (total_positions - 1 - to_idx)) & 1

			if from_bit == 1 and over_bit == 1 and to_bit == 0:
				# Make the move
				new_state = current
				# Remove peg from 'from' position
				new_state &= ~(1 << (total_positions - 1 - from_idx))
				# Remove peg from 'over' position
				new_state &= ~(1 << (total_positions - 1 - over_idx))
				# Place peg at 'to' position
				new_state |= (1 << (total_positions - 1 - to_idx))

				if new_state not in visited:
					visited.add(new_state)
					queue.append(new_state)
	return False

# Example usage:
# Define starting state and ending state as lists of 35 bits (0 or 1)
# For simplicity, let's assume the starting state has all positions filled except the center
# and the ending state has only one peg at the center.

# Starting state: all ones except center position (position index 17)
start_state = [1] * 35
start_state[17] = 0

# Ending state: only one peg at center position
end_state = [0] * 35
end_state[17] = 1

# Check if the ending state is reachable from the starting state
reachable = is_reachable(start_state, end_state)
print("Reachable:", reachable)