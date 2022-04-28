#ifndef MATMUL_COMMON_H
#define MATMUL_COMMON_H

#include <stdio.h>
#include <stdlib.h>

#include "common.h"

static inline double* malloc_matrix(int size) {
	printf("%ld\n", size * size * sizeof(double));
	return calloc(size * size, sizeof(double));
}

static inline void free_matrix(double* mat) { free(mat); }

static inline int matrix_index(int i, int j, int size) {
	return (i * size + j);
}

void fill_matrix(double* mat, int size) {
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			mat[matrix_index(i, j, size)] = get_number();
		}
	}
}

void print_matrix(double* mat, int size) {
	printf("\n");
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			printf("%7.2f ", mat[matrix_index(i, j, size)]);
		}
		printf("\n");
	}
	printf("\n");
}

double* get_matrix(int size) {
	double* ret = malloc_matrix(size);
	fill_matrix(ret, size);
	return ret;
}

#endif
