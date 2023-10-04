# Module 9: Subscripted Variables and Pointers Excercises

From https://www.cs.purdue.edu/homes/bxd/CandC++/cpp.ch9.html. My answers are in blockquotes.

# Problems:

1. Given the following definition:

	```cpp
	int box[10];
	```

	What is wrong (if anything) with the following assignment statement?

	```cpp
	box[10] = 20;
	```

> The problem is that index `10` doesn't exist; since arrays are zero-indexed, the last index of a 10-element array is `9`.

---

2. Is the following statement correct? If not, why?

	In any one array there can be values of different types.

> It is not allowed in C(++), since it is a statically typed language.

---

3. Is the following statement correct? If not, why?

	Passing large arrays into functions is a bad idea because it takes a long time to copy an array from a calling function into a called function.

> Generally it not correct, since arrays are passed by pointer reference, not by value.

---

4. Assume the following definition and initialization:

	```cpp
  	int link[5] = { 2, 3, 4, 0, 1} ;
	```

	What output does each of the following statements produce:

	a. 
	```cpp
	cout << link[0];
	```

	b. 
	```cpp
	cout << link[link[2]];
	```

	c. Given any integer `k` where `0 <= k <= 4`, what is the value of the following expression:

	```cpp
	link[link[link[link[link[k]]]]]
	```

> a. `2`
> 
> b. `1`
> 
> c. `k`

---

5. A fibonacci sequence of numbers is defined as follows: 
	The first two numbers in the sequence are `0` and `1`. Then, each additional fibonacci number is the sum of the two previous numbers in the sequence. Thus, the first ten fibonacci numbers are `0, 1, 1, 2, 3, 5, 8, 13, 21, 34`.

	Complete the following function so that the function generates the first `fib_num` numbers (where `fib_num > 2`) and puts them in the array `F`. Do **not** write a recursive function. Declare any local variable(s) you need.

	```cpp
	void fib_general(int result[], int fib_num) {
		// Declare any local variable(s)

		// Initialize the first two numbers in the array F

		// Use a loop to generate the rest
	}
	```

> ```cpp
> void fib_general(int result[], int fib_num) {
> 	F[0] = 0;
> 	F[1] = 1;
> 
> 	for (int i = 2; i < fib_num; i++) {
> 		F[i] = F[i-2] + F[i-1];
> 	}
> }
> ```

---

6. Complete the following recursive binary search function. 
	It searches a sorted (in ascending order) array `array` for a given value `element`. The parameter `first` is the first index of the array being searched, while the parameter `last` is the last index.

	```cpp
	int bin_search(int array[], int element, int first, int last) {
		int mid;

		if (/* code here */) {
			return -1; // not found
		} else { 
			mid = (first + last) / 2;

			if (/* code here */) {
				return mid;
			} else {
				if (element < array[mid]) {
					return /* code here */;
				} else {
					return /* code here */;
				}
			}
		}
	}
	```

> ```cpp
> int bin_search(int array[], int element, int first, int last) {
> 	int mid;
> 
> 	if (last - first == 1) {
> 		return -1; // not found
> 	} else { 
> 		mid = (first + last) / 2;
> 		
> 		if (array[mid] == element) {
> 			return mid;
> 		} else if (element < array[mid]) {
> 			return bin_search(array, element, first, mid);
> 		} else {
> 			return bin_search(array, element, mid, last);
> 		}
> 	}
> }
> ```

---

7. Write 3 lines of C++ code to: 

	- Declare the variable `zolish` to be a pointer to an integer

	- Make `zolish` point to the location where `xerxes` is

	- Store the number `45` in the location where `zolish` is pointing

	```cpp
	int xerxes;
	xerxes = 37;
	```

> ```cpp
> int* zolish;
> zolish = &xerxes;
> *zolish = 45;
> ```

---

8. Now what will
	```cpp
	cout << xerxes << endl;
	```
	print?

**`45`**

---

9. Write 3 lines of C++ code to: 

	- Declare the variable `salary` to be a pointer to a `float`
	
	- Dynamically allocate space for a `float` and make `salary` point to it
	
	- Store the value `150.75` in the location where `salary` is pointing

> ```cpp
> float* salary;
> salary = (float*)malloc(sizeof(float));
> *salary = 150.75;
> ```

---

10. Write a line of C++ code to de-allocate the memory that
you allocated in problem 9.

> ```cpp
> free(salary);
> ```

---

11. Assume the following declarations:

	```cpp
	int pixel;
	int pad;
	int *plane;
	int *dots;
	```

	What is stored in pixel, pad, plane, and dots after the following statements?

	```cpp
	pixel = 24;
	pad = 57;
	plane = &pixel;
	dots = &pad;
	```

> `pixel` is `24`
> 
> `pad` is `57`
> 
> `plane` is some memory address, pointing to a value of `24`
> 
> `dots` is some memory address, pointing to a value of `57`
