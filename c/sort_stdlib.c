#include <stdio.h>

#include "common.h"

// https://stackoverflow.com/questions/1787996/c-library-function-to-perform-sort
int comp(const void* elem1, const void* elem2) {
	double f = *((double*)elem1);
	double s = *((double*)elem2);
	if (f > s)
		return 1;
	if (f < s)
		return -1;
	return 0;
}

double act(int size) {
	double* l = calloc(size, sizeof(double));

	for (int i = 0; i < size; i++) {
		l[i] = get_number();
	}
#ifdef DEBUG
	print_list(l, size);
#endif

	double start = CLOCK();
	qsort(l, size, sizeof(double), comp);
	double end = CLOCK();

	fprintf(stderr, "%f\n", l[0]);

#ifdef DEBUG
	print_list(l, size);
#endif
	free(l);

	return end - start;
}

int main(int argc, char** argv) { return main_g(argc, argv, act); }
