// NOTE: it is recommended to compile this file with max optimization (-O3)

#include <stdio.h>
#include <math.h>
#include <cstdint>


// way from the assignment using a series

// iterations
// ⎲ 
// ⎳ 1 / n^2
// n = 1
double piBySeries(uint64_t iterations) {
	double sum = 0;
	for (uint64_t i = 1; i <= iterations; i++) {
		sum += 1 / pow(i, 2);
	}
	return sqrt(sum * 6);
}


// my own way using an integral

// 1
// ⌠  
// ⌡ √(1 - t^2) dt
// -1
double piByIntegral(uint64_t iterations) {
	double dt = 2.0 / iterations;
	double sum = 0;
	for (uint64_t i = 0; i < iterations; i++) {
		sum += sqrt(1 - pow((i * dt) - 1, 2));
	}
	return 2 * (sum * dt);
}


int main() {
	// this code shows how each method converges with more iterations
	// printf("integral:\n");
	// for (uint64_t i = 1; i <= 10000000000 /* 10b */; i *= 10) {
	// 	printf("%12llu: %.20f\n", i, piByIntegral(i));
	// }

	// printf("series:\n");
	// for (uint64_t i = 1; i <= 10000000000 /* 10b */; i *= 10) {
	// 	printf("%12llu: %.20f\n", i, piBySeries(i));
	// }
	
	// this code shows the end result of each method:
	printf("%.20f\n", piByIntegral(100000000000 /* 10b */));
	printf("%.20f\n", piBySeries(100000000000 /* 10b */));
}