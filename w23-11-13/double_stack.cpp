#include <iostream>
#include <vector>
#include <string>

template <typename T>
class TwoColorStack {
private:
	int redLength = 0;
	int blueLength = 0;
	int stackSize;
	std::vector<T> data;
public:
	TwoColorStack(int stackSize) {
		this->stackSize = stackSize;
		this->data.reserve(stackSize);
	}

	void pushRed(T value) {
		if (redLength == stackSize) {
			throw std::length_error("Cannot push to full stack.");
		}

		data[redLength] = value;
		redLength++;
	}

	T popRed() {
		if (redLength == 0) {
			throw std::length_error("Cannot pop from an empty stack.");
		}

		redLength--;
		return data[redLength];
	}

	void printRed() {
		for (int i = 0; i < redLength; i++) {
			std::cout << data[i];
			if (i != redLength - 1) {
				std::cout << ", ";
			}
		}
		std::cout << std::endl;
	}

	void pushBlue(T value) {
		if (blueLength == stackSize) {
			throw std::length_error("Cannot push to full stack.");
		}

		data[redLength] = value;
		blueLength++;
	}

	T popBlue() {
		if (blueLength == 0) {
			throw std::length_error("Cannot pop from an empty stack.");
		}

		blueLength--;
		return data[redLength];
	}

	void printBlue() {
		for (int i = 0; i < blueLength; i++) {
			std::cout << data[i];
			if (i != blueLength - 1) {
				std::cout << ", ";
			}
		}
		std::cout << std::endl;
	}
};

int main() {
	auto s = TwoColorStack<std::string>(10);
	s.pushRed("Hello");
	s.pushRed("world");

	s.printRed();
}