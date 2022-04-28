#include <cblas.h>

#include "common.h"
#include "matmul_common.h"

void multiply_matrices(double* a, double* b, double* c, int size) {
    cblas_dgemm(
            CblasRowMajor, CblasNoTrans, CblasNoTrans,
            size, size, size,
            1.0,
            a, size,
            b, size,
            0.0, c, size
    );
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
