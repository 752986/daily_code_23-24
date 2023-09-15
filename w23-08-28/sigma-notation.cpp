#include <stdio.h>

int main() {
	/* 
	/  10
	/  ___
	/  \
	/  / 2n - 1
	/  ___
	/  n = 1
	*/

	auto sum = 0;
	for (auto n = 1; n <= 10; n++) {
		sum += (2 * n) - 1;
	}
	printf("%d", sum);
}

