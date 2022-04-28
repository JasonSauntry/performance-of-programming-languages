#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double CLOCK() {

	// From hw3
	struct timespec t;
	clock_gettime(CLOCK_MONOTONIC, &t);
	return (t.tv_sec * 1000) + (t.tv_nsec * 1e-6);
}

#define BOX_MULLER_ITS 20

double get_number() {
	// This incantation apparently approximates a normal distrobution, from:
	// https://stackoverflow.com/questions/2325472/generate-random-numbers-following-a-normal-distribution-in-c-c
	double sum = 0;
	for (short i = 0; i < BOX_MULLER_ITS * 2; i++) {
		sum += (double)rand() / RAND_MAX;
	}
	return sum - BOX_MULLER_ITS;
}

int main_g(int argc, char** argv, double (*f)(int)) {
	srand(time(0));

	int size = argc > 1 ? atoi(argv[1]) : 10;

	double millis = f(size);

	printf("time: %f\n", millis);

	return 0;
}

void print_list(double* l, int size) {
	for (int i = 0; i < size; i++) {
		printf("%f, ", l[i]);
	}
	printf("\n");
}

#endif
