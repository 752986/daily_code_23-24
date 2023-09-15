#include <stdio.h>

int main() {
	// problem 1
	////////////

	for (int i = 5; i < 50; i += 3) {
		printf("%d\n", i);
	}


	// problem 2
	////////////
	printf("\n");

	for (int i = 80; i > 10; i -= 2) {
		printf("%d\n", i);
	}


	// problem 3
	////////////
	printf("\n");

	for (int i = 2; i < 200; i *= 5) {
		printf("%d\n", i);
	}
}
