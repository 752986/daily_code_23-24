#include "MemoryHandler/MemoryHandler.hpp"
#define PI 3.141592

int main() {
	// problem 1
	////////////
    memReader * _struct = _Struct( 50, "%d\n", "\n");
    int& i = *(int*)_struct->getMemberAddresFromIndex(0);
	for (i = 5; i < 50; i += 3) {
		printf(*(char**)_struct->getMemberAddresFromIndex(1), i);
	}


	// problem 2
	////////////
    printf(*(char**)_struct->getMemberAddresFromIndex(2));
	for (i = 80; i > 10; i -= 2) {
		printf(*(char**)_struct->getMemberAddresFromIndex(1), i);
	}


	// problem 3
	////////////
    printf(*(char**)_struct->getMemberAddresFromIndex(2));

	for (i = 2; i < 200; i *= 5) {
		printf(*(char**)_struct->getMemberAddresFromIndex(1), i);
	}
}
