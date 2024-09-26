#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>

#define ROWS 7
#define COLS 5
#define TOTAL_POSITIONS (ROWS * COLS)
#define MAX_MOVES 200  
#define INITIAL_QUEUE_SIZE 1000000
#define HASH_TABLE_SIZE 10000019

typedef uint64_t BoardState;

typedef struct {
    int from;
    int over;
    int to;
} Move;

typedef struct {
    BoardState *data;
    size_t head;
    size_t tail;
    size_t capacity;
} Queue;

typedef struct {
    BoardState *keys;
    char *values;
    size_t size;
} HashTable;

// Function prototypes
void generate_moves(Move *moves, int *num_moves);
BoardState serialize_state(int *state);
void deserialize_state(BoardState num, int size, int *state);
int is_reachable(int *start_state, int *end_state);
void queue_init(Queue *q, size_t capacity);
void queue_free(Queue *q);
void queue_enqueue(Queue *q, BoardState state);
int queue_dequeue(Queue *q, BoardState *state);
void hash_table_init(HashTable *ht, size_t size);
void hash_table_free(HashTable *ht);
int hash_table_insert(HashTable *ht, BoardState key);
int hash_table_contains(HashTable *ht, BoardState key);


int main() {
    // Define starting state and ending state as arrays of 35 bits (0 or 1)
    int start_state[TOTAL_POSITIONS];
    int end_state[TOTAL_POSITIONS];

    // Initialize start_state: all ones except center position (position index 17)
    for (int i = 0; i < TOTAL_POSITIONS; i++) {
        start_state[i] = 1;
    }
    start_state[17] = 0;

    // Initialize end_state: only one peg at center position
    for (int i = 0; i < TOTAL_POSITIONS; i++) {
        end_state[i] = 0;
    }
    end_state[17] = 1;

    // Check if the ending state is reachable from the starting state
    int reachable = is_reachable(start_state, end_state);
    printf("Reachable: %s\n", reachable ? "Yes" : "No");

    return 0;
}

// Function definitions

void generate_moves(Move *moves, int *num_moves) {
    *num_moves = 0;
    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c < COLS; c++) {
            int from_idx = r * COLS + c;
            // Move Up
            if (r >= 2) {
                int over_idx = (r - 1) * COLS + c;
                int to_idx = (r - 2) * COLS + c;
                moves[(*num_moves)++] = (Move){from_idx, over_idx, to_idx};
            }
            // Move Down
            if (r <= ROWS - 3) {
                int over_idx = (r + 1) * COLS + c;
                int to_idx = (r + 2) * COLS + c;
                moves[(*num_moves)++] = (Move){from_idx, over_idx, to_idx};
            }
            // Move Left
            if (c >= 2) {
                int over_idx = r * COLS + (c - 1);
                int to_idx = r * COLS + (c - 2);
                moves[(*num_moves)++] = (Move){from_idx, over_idx, to_idx};
            }
            // Move Right
            if (c <= COLS - 3) {
                int over_idx = r * COLS + (c + 1);
                int to_idx = r * COLS + (c + 2);
                moves[(*num_moves)++] = (Move){from_idx, over_idx, to_idx};
            }
        }
    }
}

BoardState serialize_state(int *state) {
    BoardState result = 0;
    for (int i = 0; i < TOTAL_POSITIONS; i++) {
        result = (result << 1) | (state[i] & 1);
    }
    return result;
}

void deserialize_state(BoardState num, int size, int *state) {
    for (int i = size - 1; i >= 0; i--) {
        state[i] = num & 1;
        num >>= 1;
    }
}

int is_reachable(int *start_state, int *end_state) {
    Move moves[MAX_MOVES];
    int num_moves;
    generate_moves(moves, &num_moves);

    HashTable visited;
    hash_table_init(&visited, HASH_TABLE_SIZE);

    Queue queue;
    queue_init(&queue, INITIAL_QUEUE_SIZE);

    BoardState start_num = serialize_state(start_state);
    BoardState end_num = serialize_state(end_state);

    queue_enqueue(&queue, start_num);
    hash_table_insert(&visited, start_num);

    while (queue_dequeue(&queue, &start_num)) {
        if (start_num == end_num) {
            hash_table_free(&visited);
            queue_free(&queue);
            return 1;  // Reachable
        }

        // For each possible move
        for (int i = 0; i < num_moves; i++) {
            int from_idx = moves[i].from;
            int over_idx = moves[i].over;
            int to_idx = moves[i].to;

            // Extract bits
            int from_bit = (start_num >> (TOTAL_POSITIONS - 1 - from_idx)) & 1;
            int over_bit = (start_num >> (TOTAL_POSITIONS - 1 - over_idx)) & 1;
            int to_bit = (start_num >> (TOTAL_POSITIONS - 1 - to_idx)) & 1;

            // Check if move is valid
            if (from_bit == 1 && over_bit == 1 && to_bit == 0) {
                // Make the move
                BoardState new_state = start_num;

                // Remove peg from 'from' position
                new_state &= ~(1ULL << (TOTAL_POSITIONS - 1 - from_idx));
                // Remove peg from 'over' position
                new_state &= ~(1ULL << (TOTAL_POSITIONS - 1 - over_idx));
                // Place peg at 'to' position
                new_state |= (1ULL << (TOTAL_POSITIONS - 1 - to_idx));

                if (!hash_table_contains(&visited, new_state)) {
                    hash_table_insert(&visited, new_state);
                    queue_enqueue(&queue, new_state);
                }
            }
        }
    }

    hash_table_free(&visited);
    queue_free(&queue);
    return 0;  // Not reachable
}

// Queue implementation
void queue_init(Queue *q, size_t capacity) {
    q->data = (BoardState *)malloc(capacity * sizeof(BoardState));
    q->head = 0;
    q->tail = 0;
    q->capacity = capacity;
}

void queue_free(Queue *q) {
    free(q->data);
}

void queue_enqueue(Queue *q, BoardState state) {
    if (q->tail >= q->capacity) {
        // Resize the queue
        q->capacity *= 2;
        q->data = (BoardState *)realloc(q->data, q->capacity * sizeof(BoardState));
    }
    q->data[q->tail++] = state;
}

int queue_dequeue(Queue *q, BoardState *state) {
    if (q->head == q->tail) {
        return 0;  // Queue is empty
    }
    *state = q->data[q->head++];
    return 1;
}

// Hash table implementation
void hash_table_init(HashTable *ht, size_t size) {
    ht->size = size;
    ht->keys = (BoardState *)calloc(size, sizeof(BoardState));
    ht->values = (char *)calloc(size, sizeof(char));
}

void hash_table_free(HashTable *ht) {
    free(ht->keys);
    free(ht->values);
}

size_t hash_function(BoardState key, size_t size) {
    return key % size;
}

int hash_table_insert(HashTable *ht, BoardState key) {
    size_t idx = hash_function(key, ht->size);
    size_t original_idx = idx;
    while (ht->values[idx]) {
        if (ht->keys[idx] == key) {
            return 0;  // Already exists
        }
        idx = (idx + 1) % ht->size;
        if (idx == original_idx) {
            // Hash table is full
            fprintf(stderr, "Hash table is full\n");
            exit(EXIT_FAILURE);
        }
    }
    ht->keys[idx] = key;
    ht->values[idx] = 1;
    return 1;
}

int hash_table_contains(HashTable *ht, BoardState key) {
    size_t idx = hash_function(key, ht->size);
    size_t original_idx = idx;
    while (ht->values[idx]) {
        if (ht->keys[idx] == key) {
            return 1;  // Found
        }
        idx = (idx + 1) % ht->size;
        if (idx == original_idx) {
            return 0;  // Not found
        }
    }
    return 0;  // Not found
}