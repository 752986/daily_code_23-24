#include <cstddef>
#include <malloc.h>
#include <stdexcept>
#include <vector>

/// @brief A stack data structure (last in, first out) which automatically grows as needed.
/// @tparam T: The type of elements held in the stack.
template <typename T>
class Stack {
	private:
	/// @brief The base pointer of the stack.
	T* _ptr;
	/// @brief The number of items in the stack.
	size_t _size;
	/// @brief The number of elements currently allocated.
	size_t _capacity;

	public:
	/// @brief Initializes an empty `Stack`. This method does not allocate memory.
	Stack() {
		_ptr = nullptr;
		_size = 0;
		_capacity = 0;
	}

	/// @brief Initializes a `Stack` with enough space allocated for `capacity` elements.
	/// @param capacity: The number of elements the resulting `Stack` should have space for.
	Stack(size_t capacity) {
		_ptr = (T*)malloc(capacity * sizeof(T));
		_size = 0;
		this->_capacity = capacity;
	}

	~Stack() {
		free(_ptr);
	}

	/// @brief Gets the number of items currently in the stack.
	/// @return The number of items in the stack.
	size_t size() {
		return _size;
	}

	/// @brief Checks whether the stack is empty.
	/// @return A boolean indicating whether or not the stack is empty.
	bool isEmpty() {
		return _size == 0;
	}

	/// @brief Pushes an item onto the stack, allocating additional memory if needed. 
	/// @param item: The item to push.
	void push(T item) {
		if (_capacity == 0) {
			_ptr = (T*)malloc(4 * sizeof(T));
			_capacity = 4;
		} else if (_size == _capacity) { // reallocate if there isn't enough room for the new item
			// capacity is doubled to amortize cost of sucessive pushes
			_ptr = (T*)realloc(_ptr, _capacity * 2 * sizeof(T));
			_capacity *= 2;
		}

		_ptr[_size] = item;
		_size++;
	}

	/// @brief Pops the top element off of the stack and returns it.
	/// @return The top element of the stack.
	/// @throw `std::length_error` if the stack is empty.
	T pop() {
		if (_size == 0) {
			throw std::length_error("Cannot pop from an empty stack.");
		}
		_size--;
		return _ptr[_size];
	}

	/// @brief Returns a pointer to the element at the top of the stack.
	/// @warning The returned pointer is only valid until the element is popped off the stack.
	///          Past that point, it may contain other values or garbage data.
	/// @return `nullptr` if the stack is empty, otherwise a pointer to the top element.
	T* top() {
		if (_size == 0) {
			return nullptr;
		}
		return &_ptr[_size - 1];
	}
};

int main(int argc, char const *argv[]) {
	auto s = Stack<int>();
	s.push(10);
	s.push(3);
	s.push(2);
	s.push(8);
	s.push(6);

	printf("stack has size %d\n", s.size());
	printf("the top element is %d\n", *(s.top()));

	while (!s.isEmpty()) {
		printf("%d\n", s.pop());
	}
	
	return 0;
}
