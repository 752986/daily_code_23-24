#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() { 
	srand(time(NULL)); // seed the rng so it doesn't give the same result every time

	for (int i = 0; i < 24; i++) {
		for (int j = 0; j < 40; j++) {
			if (rand() % 5 == 0) {
				printf("❤️ ");// extra space because emoji are double-wide
				// printf("\u2764\uFE0F "); // unicode version i guess
			} else {
				printf("  ");
			}
		}

		printf("\n");
	}
}