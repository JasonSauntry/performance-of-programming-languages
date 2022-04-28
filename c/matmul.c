#include "matmul_common.h"

void multiply_matrices(double* a, double* b, double* c, int size) {
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			int index = matrix_index(i, j, size);
			c[index] = 0;
			for (int k = 0; k < size; k++) {
				c[index] +=
					a[matrix_index(k, j, size)] *
					b[matrix_index(i, k, size)];
			}
		}
	}
}

double act(int size) {
	double* a = get_matrix(size);
	double* b = get_matrix(size);
	double* c = malloc_matrix(size);

	double start = CLOCK();
	multiply_matrices(a, b, c, size);
	double end = CLOCK();

	fprintf(stderr, "%f\n", c[0]);

#ifdef DEBUG
	print_matrix(a, size);
	print_matrix(b, size);
	print_matrix(c, size);
#endif
	free_matrix(a);
	free_matrix(b);
	free_matrix(c);

	return end - start;
}

int main(int argc, char** argv) {
	return main_g(argc, argv, act);
}
