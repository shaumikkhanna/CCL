#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


#define ROWS 5
#define COLS 4
#define MAX_SUCCESSORS 4*ROWS*COLS - 2*ROWS - 2*COLS
#define MAX_QUEUE_SIZE 1000000
#define TOLERANCE 2


// 35 bits to represent the board of the game
typedef uint64_t BoardState;

// Moves in the game using bit manipulation
#define SET_PEG(state, pos) ((state) |= ((uint64_t)1ULL << (pos)))
#define CLEAR_PEG(state, pos) ((state) &= ~((uint64_t)1ULL << (pos)))
#define IS_PEG(state, pos) (((state) >> (pos)) & 1ULL)

// Position mapping from 2D to 1D
#define POS(row, col) ((row) * COLS + (col))



// Node structure for the priority queue
typedef struct {
    BoardState state;
    int h; // Heuristic value
} Node;

// Priority Queue for open
typedef struct {
    Node *nodes;
    int size;
    int capacity;
} PriorityQueue;

// Hash Set for closed set
typedef struct {
    BoardState *states;
    int size;
    int capacity;
} HashSet;



// Function declarations
void init_priority_queue(PriorityQueue *pq, int capacity);
void insert_priority_queue(PriorityQueue *pq, Node node);
Node extract_min_priority_queue(PriorityQueue *pq);
int is_empty_priority_queue(PriorityQueue *pq);

void init_hash_set(HashSet *hs, int capacity);
int is_in_hash_set(HashSet *hs, BoardState state);
void insert_hash_set(HashSet *hs, BoardState state);

void generate_successors(BoardState current_state, BoardState successors[], int *num_successors);
int heuristic(BoardState current_state, BoardState goal_state);
int compare_board_states(BoardState state1, BoardState state2);

int greedy_best_first_search(BoardState start_state, BoardState goal_state);



// Main function
int main() {
    BoardState start_state = 0;
    BoardState goal_state = 0;

    // Initialize start state
    start_state = 0b11111111100111111111; // Standard start state

    // Fill the board with pegs except center
    // for (int i = 0; i < ROWS; i++) { 
    //     for (int j = 0; j < COLS; j++) {
    //         if (!(i == 2 && j == 1)) {
    //             SET_PEG(start_state, POS(i, j));
    //         }
    //     }
    // }

    // Initialize goal state
    // SET_PEG(goal_state, POS(3, 1));
    goal_state = 0b10011010010010101001;

    printf("Start state: %llu\n", start_state);
    printf("Goal state: %llu\n", goal_state);

    if (greedy_best_first_search(start_state, goal_state)) {
        printf("The goal state is reachable from the starting state.\n");
    } else {
        printf("The goal state is not reachable from the starting state.\n");
    }

    return 0;
}


// Greedy Best-First Search implementation
int greedy_best_first_search(BoardState start_state, BoardState goal_state) {
    PriorityQueue open_set;
    init_priority_queue(&open_set, MAX_QUEUE_SIZE);

    HashSet closed_set;
    init_hash_set(&closed_set, MAX_QUEUE_SIZE);

    Node start_node;
    start_node.state = start_state;
    start_node.h = heuristic(start_state, goal_state);

    insert_priority_queue(&open_set, start_node);

    while (!is_empty_priority_queue(&open_set)) {
        Node current_node = extract_min_priority_queue(&open_set);

        if (is_in_hash_set(&closed_set, current_node.state)) {
            continue;
        }

        if (current_node.h == 0) {
            // Goal reached
            free(open_set.nodes);
            free(closed_set.states);
            return 1;
        }

        // printf("%llu\n", current_node.state);
        insert_hash_set(&closed_set, current_node.state);

        // Generate children
        BoardState successors[MAX_SUCCESSORS];
        int num_successors = 0;
        generate_successors(current_node.state, successors, &num_successors);

        for (int i = 0; i < num_successors; i++) {
            if (is_in_hash_set(&closed_set, successors[i])) {
                continue;
            }

            Node successor_node;
            successor_node.state = successors[i];
            successor_node.h = heuristic(successors[i], goal_state);

            insert_priority_queue(&open_set, successor_node);
        }
    }

    // Goal not reachable
    free(open_set.nodes);
    free(closed_set.states);
    return 0;
}

// Heuristic function -- Counts the number of pegs that are different from the goal state (hamming distance)
int heuristic(BoardState current_state, BoardState goal_state) {
    int h = 0;
    for (int i = 0; i < ROWS * COLS; i++) {
        if (IS_PEG(current_state, i) != IS_PEG(goal_state, i)) {
            h++;
        }
    }

    if (h <= TOLERANCE) {
        printf("(%d,%llu),\n", h, current_state);
    }

    return h;
}

// Compare two board states - UNUSED
int compare_board_states(BoardState state1, BoardState state2) {
    return state1 == state2;
}

// Generate all valid successor states from the current state
void generate_successors(BoardState current_state, BoardState successors[], int *num_successors) {
    *num_successors = 0;

    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS; col++) {
            int pos = POS(row, col);
            
            if (IS_PEG(current_state, pos)) {
                // Check all four directions

                // Up
                if (row >= 2) {
                    int over_pos = POS(row - 1, col);
                    int to_pos = POS(row - 2, col);
                    if (IS_PEG(current_state, over_pos) && !IS_PEG(current_state, to_pos)) {
                        BoardState new_state = current_state;
                        CLEAR_PEG(new_state, pos);
                        CLEAR_PEG(new_state, over_pos);
                        SET_PEG(new_state, to_pos);
                        successors[(*num_successors)++] = new_state;
                    }
                }
                // Down
                if (row <= ROWS - 3) {
                    int over_pos = POS(row + 1, col);
                    int to_pos = POS(row + 2, col);
                    if (IS_PEG(current_state, over_pos) && !IS_PEG(current_state, to_pos)) {
                        BoardState new_state = current_state;
                        CLEAR_PEG(new_state, pos);
                        CLEAR_PEG(new_state, over_pos);
                        SET_PEG(new_state, to_pos);
                        successors[(*num_successors)++] = new_state;
                    }
                }
                // Left
                if (col >= 2) {
                    int over_pos = POS(row, col - 1);
                    int to_pos = POS(row, col - 2);
                    if (IS_PEG(current_state, over_pos) && !IS_PEG(current_state, to_pos)) {
                        BoardState new_state = current_state;
                        CLEAR_PEG(new_state, pos);
                        CLEAR_PEG(new_state, over_pos);
                        SET_PEG(new_state, to_pos);
                        successors[(*num_successors)++] = new_state;
                    }
                }
                // Right
                if (col <= COLS - 3) {
                    int over_pos = POS(row, col + 1);
                    int to_pos = POS(row, col + 2);
                    if (IS_PEG(current_state, over_pos) && !IS_PEG(current_state, to_pos)) {
                        BoardState new_state = current_state;
                        CLEAR_PEG(new_state, pos);
                        CLEAR_PEG(new_state, over_pos);
                        SET_PEG(new_state, to_pos);
                        successors[(*num_successors)++] = new_state;
                    }
                }
            }
        }
    }
}

// Priority Queue functions
void init_priority_queue(PriorityQueue *pq, int capacity) {
    pq->nodes = (Node *)malloc(sizeof(Node) * capacity);
    pq->size = 0;
    pq->capacity = capacity;
}

void swap_nodes(Node *a, Node *b) {
    Node temp = *a;
    *a = *b;
    *b = temp;
}

void insert_priority_queue(PriorityQueue *pq, Node node) {
    if (pq->size >= pq->capacity) {
        fprintf(stderr, "Priority Queue is full!\n");
        exit(EXIT_FAILURE);
    }
    pq->nodes[pq->size] = node;
    int i = pq->size;
    pq->size++;

    // Min-heapify up
    while (i != 0 && pq->nodes[(i - 1) / 2].h > pq->nodes[i].h) {
        swap_nodes(&pq->nodes[i], &pq->nodes[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
}

Node extract_min_priority_queue(PriorityQueue *pq) {
    if (pq->size <= 0) {
        fprintf(stderr, "Priority Queue is empty!\n");
        exit(EXIT_FAILURE);
    }
    Node root = pq->nodes[0];
    pq->nodes[0] = pq->nodes[pq->size - 1];
    pq->size--;

    // Min-heapify down
    int i = 0;
    while (i < pq->size) {
        int smallest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < pq->size && pq->nodes[left].h < pq->nodes[smallest].h) {
            smallest = left;
        }
        if (right < pq->size && pq->nodes[right].h < pq->nodes[smallest].h) {
            smallest = right;
        }
        if (smallest != i) {
            swap_nodes(&pq->nodes[i], &pq->nodes[smallest]);
            i = smallest;
        } else {
            break;
        }
    }
    return root;
}

int is_empty_priority_queue(PriorityQueue *pq) {
    return pq->size == 0;
}

// Hash Set functions
void init_hash_set(HashSet *hs, int capacity) {
    hs->states = (BoardState *)malloc(sizeof(BoardState) * capacity);
    hs->size = 0;
    hs->capacity = capacity;
}

int is_in_hash_set(HashSet *hs, BoardState state) {
    for (int i = 0; i < hs->size; i++) {
        if (hs->states[i] == state) {
            return 1;
        }
    }
    return 0;
}

void insert_hash_set(HashSet *hs, BoardState state) {
    if (hs->size >= hs->capacity) {
        fprintf(stderr, "Hash Set is full!\n");
        exit(EXIT_FAILURE);
    }
    hs->states[hs->size++] = state;
}