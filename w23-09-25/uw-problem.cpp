/*
* based on CSE390C Sample Midterm handout #3, problem #3
*/

#include <fstream>
#include <istream>
#include <iostream>
#include <string>
using namespace std;


void replace_all(istream& input, char toReplace, char replaceWith) {
	//   this ampersand ^ is very important, otherwise it gives you incredibly unhelpful errors
	char c;
	do {
		c = input.get(); // `get` because stream operators skip whitespace
		if (c == toReplace) {
			cout << replaceWith;
		} else {
			cout << c;
		}
	} while (!input.eof()); // checks if the stream is at end of file
}

int main() {
	ifstream input("sample.txt");
	if (!input.is_open()) {
		cout << "file not found!" << endl;
		return 1;
	}
	
	replace_all(input, '.', '!');
}