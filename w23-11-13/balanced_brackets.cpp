#include <iostream>
#include <stack>
using namespace std;

bool isBalanced(istream &input) {
	stack<char> brackets;

	for (char c = 0; c != '\n'; input >> c) {
		cout << c;
		if (c == '(' or c == '[' or c == '{') {
			// if c is a left bracket push it to the stack
			brackets.push(c);
		} else if (c == ')' or c == ']' or c == '}') {
			if (brackets.empty()) {
				// if there aren't any more brackets then it's unbalanced
				return false;
			}
			
			if (
				(c == ')' and brackets.top() == '(') or
				(c == ']' and brackets.top() == '[') or
				(c == '}' and brackets.top() == '{')
			) {
				
				// if c is a right bracket check if it matches the left bracket on the stack
					brackets.pop();
			} else {
				// if the left and right brackets don't match then it's unbalanced
				return false;
			}
		}
	}

	return true;
}

int main() {
	cout << (isBalanced(cin) ? "true" : "false");
}
