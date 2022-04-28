#include <alloca.h>
#include <error.h>

#include "common.h"

unsigned int maxu(unsigned int a, unsigned int b) { return a > b ? a : b; }

typedef struct HeapNode {
	double value;
	struct HeapNode* left;
	struct HeapNode* right;
	int empty;
} HeapNode;

HeapNode* node_new_sides(double value, HeapNode* left, HeapNode* right) {
	HeapNode* ret = malloc(sizeof(HeapNode));
	ret->value = value;
	ret->left = left;
	ret->right = right;
	ret->empty = 0;

	return ret;
}

HeapNode* node_new(double value) { return node_new_sides(value, 0, 0); }

unsigned int node_depth(HeapNode* node) {
	unsigned int ldepth = node->left ? node_depth(node->left) + 1 : 1;
	unsigned int rdepth = node->right ? node_depth(node->right) + 1 : 1;

	return maxu(ldepth, rdepth);
}

void node_push(HeapNode* node, double new_value) {
	if (new_value >= node->value) {
		if (!node->left) {
			node->left = node_new(new_value);
		} else if (!node->right) {
			node->right = node_new(new_value);
		} else {
			HeapNode* expand_side =
			    node_depth(node->left) < node_depth(node->right) ? node->left
			                                                     : node->right;
			node_push(expand_side, new_value);
		}
	} else {
		double old_value = node->value;
		HeapNode* old_right = node->right;
		HeapNode* old_left = node->left;

		node->value = new_value;
		node->right = 0;
		node->left = node_new_sides(old_value, old_left, old_right);
	}
}

double node_pop(HeapNode* node) {
	double ret = node->value;

	if (node->left && node->right) {
		HeapNode* pop_side =
		    node->left->value < node->right->value ? node->left : node->right;
		node->value = node_pop(pop_side);
	} else if (node->left) {
		node->value = node->left->value;
		node->right = node->left->right;
		node->left = node->left->left;
	} else if (node->right) {
		node->value = node->right->value;
		node->left = node->right->left;
		node->right = node->right->right;
	} else {
		node->empty = 1;
	}

	if (node->left && node->left->empty) {
		free(node->left);
		node->left = 0;
	}
	if (node->right && node->right->empty) {
		free(node->right);
		node->right = 0;
	}

	return ret;
}

size_t node_count(HeapNode* node) {
	if (node) {
		return 1 + node_count(node->left) + node_count(node->right);
	} else {
		return 0;
	}
}

const size_t OUT_SIZE = 1000;
void node_to_string(HeapNode* node, char* out, size_t out_len) {
	if (node) {
		char* l_out = alloca(sizeof(char) * OUT_SIZE);
		char* r_out = alloca(sizeof(char) * OUT_SIZE);

		node_to_string(node->left, l_out, OUT_SIZE);
		node_to_string(node->right, r_out, OUT_SIZE);

		snprintf(out, out_len, "HeapNode(%f, %s, %s)", node->value, l_out,
		         r_out);
	} else {
		snprintf(out, out_len, "—");
	}
}

void node_print(HeapNode* node) {
	char* out = alloca(sizeof(char) * OUT_SIZE);

	node_to_string(node, out, OUT_SIZE);

	puts(out);
	puts("\n");
}

typedef HeapNode* Heap;

void heap_push(Heap* h, double val) {
	if (*h) {
		node_push(*h, val);
	} else {
		*h = node_new(val);
	}
}

double heap_pop(Heap* h) {
	if (*h) {
		double ret = node_pop(*h);
		if ((*h)->empty) {
			free(*h);
			*h = 0;
		}
		return ret;
	} else {
		error_at_line(-1, -1, __FILE__, __LINE__,
		              "Attempted to pop empty heap");
		return 0;
	}
}

inline int heap_empty(Heap* h) { return *h == 0; }

inline Heap heap_new() { return 0; }

inline size_t heap_count(Heap* h) { return node_count(*h); }

void heap_free(Heap* h) {
	while (!heap_empty(h)) {
		heap_pop(h);
	}
}

inline void heap_print(Heap* h) { node_print(*h); }

double act(int size) {
	double* l = calloc(size, sizeof(double));

	for (int i = 0; i < size; i++) {
		l[i] = get_number();
	}
#ifdef DEBUG
	print_list(l, size);
#endif

	double start = CLOCK();
	Heap h = heap_new();
	for (int i = 0; i < size; i++) {
		heap_push(&h, l[i]);
	}
#ifdef DEBUG
	heap_print(&h);
#endif

	free(l);
	double* out = calloc(heap_count(&h), sizeof(double));

	for (int i = 0; i < size; i++) {
		out[i] = heap_pop(&h);
	}

	double end = CLOCK();

	fprintf(stderr, "%f\n", l[rand() % size]);

#ifdef DEBUG
	print_list(out, size);
#endif
	free(out);

	return end - start;
}

int main(int argc, char** argv) { return main_g(argc, argv, act); }
