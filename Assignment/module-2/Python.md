##### **Python – Collections, functions and Modules**





1. **Accessing List:**



**✦ Understanding how to create and access elements in a list.**



**→** A list is a collection of items stored in a single variable. In Python, lists are created using square brackets \[].



▸Example of creating a list:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange"]



▸Accessing elements in a list:

**•** List elements are accessed using their index number. Indexing starts from 0.

like....

&#x09;print(fruits\[0])  # Apple

&#x09;print(fruits\[1])  # Banana

&#x09;print(fruits\[2])  # Mango

&#x09;print(fruits\[-1])  # Orange

\*\*•\*\*Lists help store multiple values in a single variable. Elements in a list can be easily accessed using their index positions.



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Indexing in lists (positive and negative indexing).**



**→** Indexing is used to access elements in a list. In Python, indexing starts from 0.



▸Example List:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange"]



1\. Positive Indexing:

&#x20; **•** Positive indexing starts from the beginning of the list.

&#x20; | Index | Element |

&#x20; | ----- | ------- |

&#x20; | 0     | Apple   |

&#x20; | 1     | Banana  |

&#x20; | 2     | Mango   |

&#x20; | 3     | Orange  |



&#x20; ▸Example:

&#x09;print(fruits\[0])  # Apple

&#x09;print(fruits\[2])  # Mango



2\. Negative Indexing:

&#x20; **•** Negative indexing starts from the end of the list.

&#x20; | Index | Element |

&#x20; | ----- | ------- |

&#x20; | -1    | Orange  |

&#x20; | -2    | Mango   |

&#x20; | -3    | Banana  |

&#x20; | -4    | Apple   |



&#x20; ▸Example:

&#x09;print(fruits\[-1])  # Orange

&#x09;print(fruits\[-2])  # Mango



**→** positive indexing accesses elements from the beginning of the list, while negative indexing accesses elements from the end. This makes it easy to retrieve items from any position in a list.



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Slicing a list: accessing a range of elements.**



**→** List slicing is used to access multiple elements from a list by specifying a range of indexes.



▸Example List:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange", "Grapes"]



▸Syntax:

&#x09;list\_name\[start:end]

&#x09;start → Starting index (included)

&#x09;end → Ending index (excluded)



▸Examples:

&#x09;print(fruits\[1:4])

&#x09;print(fruits\[:3])

&#x09;print(fruits\[2:])

&#x09;print(fruits\[-3:-1])





▸Output:

&#x09;\['Banana', 'Mango', 'Orange']

&#x09;\['Apple', 'Banana', 'Mango']

&#x09;\['Mango', 'Orange', 'Grapes']

&#x09;\['Mango', 'Orange']



**→** List slicing allows us to access a range of elements from a list easily. It makes working with large lists more efficient and flexible



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**2. List Operations:**



**✦ Common list operations: concatenation, repetition, membership.**



**→** Lists are versatile data structures in Python that allow us to store multiple values in a single variable.

**→** Python provides several operations that make it easy to manipulate and work with lists.

**→** Three common list operations are concatenation, repetition, and membership testing.



1\. Concatenation:



&#x20;▸Concatenation means combining two or more lists into a single list.

&#x20;▸It is performed using the + operator.

&#x20;▸The original lists remain unchanged.



▸Example:

&#x09;list1 = \[1, 2, 3]

&#x09;list2 = \[4, 5, 6]

&#x09;

&#x09;result = list1 + list2

&#x09;print(result)



▸Output:

&#x09;\[1, 2, 3, 4, 5, 6]



2\. Repetition:



&#x20;▸Repetition means repeating the elements of a list multiple times.

&#x20;▸It is performed using the \* operator.

&#x20;▸The number after \* specifies how many times the list will be repeated.



▸Example:

&#x09;list1 = \[1, 2, 3]



&#x09;result = list1 \* 3

&#x09;print(result)



▸Output:

&#x09;\[1, 2, 3, 1, 2, 3, 1, 2, 3]



3\. Membership Testing:



&#x20;▸Membership testing checks whether a specific element exists in a list.

&#x20;▸The in operator returns True if the element is present.

&#x20;▸The not in operator returns True if the element is not present.



▸Example:

&#x09;list1 = \[1, 2, 3]

&#x09;print(2 in list1)

&#x09;print(7 not in list1)



▸Output:

&#x09;True

&#x09;True

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

**✦ Understanding list methods like append(), insert(), remove(), pop().**



**→** Lists in Python provide several built-in methods that help us add, delete, and manage elements efficiently. Some of the most commonly used list methods are append(), insert(), remove(), and pop().



1\. append():



&#x20;▸The append() method is used to add an element at the end of a list.

&#x20;▸It adds only one element at a time.

&#x20;▸The original list is modified.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;fruits.append("Orange")

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Banana', 'Mango', 'Orange']



2\. insert():



&#x20;▸The insert() method is used to add an element at a specific position in the list.

&#x20;▸It requires two arguments: index position and value.



▸Syntax:

&#x09;list\_name.insert(index, element)



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;fruits.insert(1, "Orange")

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Orange', 'Banana', 'Mango']



3\. remove():



&#x20;▸The remove() method is used to remove a specific element from a list.

&#x20;▸It removes the first occurrence of the specified value.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]

&#x09;

&#x09;fruits.remove("Banana")

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Mango']



4\. pop():

&#x20;▸The pop() method removes and returns an element from the list.

&#x20;▸If no index is specified, it removes the last element.



▸Example 1:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;fruits.pop()

&#x09;print(fruits)

&#x09;fruits.pop(1)

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Banana']

&#x09;\['Apple', 'Mango']



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**3. Working with Lists:**



**→** Lists often contain multiple elements, and it is common to perform operations on each element.

**→** Iterating over a list means accessing each element of the list one by one.

**→** In Python, loops are used to iterate through lists efficiently.

**→** The most commonly used loops for list iteration are for loops and while loops.



1\. Using a For Loop:

&#x20;▸A for loop is the easiest and most commonly used way to iterate over a list.

&#x20;▸It automatically accesses each element one by one.

&#x20;▸No index management is required.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange"]

&#x09;

&#x09;for fruit in fruits:

&#x20;   		print(fruit)



▸Output:

&#x09;Apple

&#x09;Banana

&#x09;Mango

&#x09;Orange



2\. Using a While Loop:

&#x20;▸A while loop can also be used to iterate over a list.

&#x20;▸It requires an index variable to access list elements.

&#x20;▸The index must be updated manually.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange"]



&#x09;i = 0

&#x09;while i < len(fruits):

&#x20;   		print(fruits\[i])

&#x20;   	i += 1



▸Output:

&#x09;Apple

&#x09;Banana

&#x09;Mango

&#x09;Orange



3\. Iterating with Index Using For Loop:

&#x20;▸Sometimes both the index and the element are needed.

&#x20;▸The range() function can be used with a for loop.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;for i in range(len(fruits)):

&#x20;   		print(i, fruits\[i])



▸Output:

&#x09;0 Apple

&#x09;1 Banana

&#x09;2 Mango



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Sorting and reversing a list using sort(), sorted(), and reverse().**



**→** Lists often need to be arranged in a specific order for better organization and data processing.

**→** Python provides built-in methods such as sort(), sorted(), and reverse() to sort and reverse list elements easily.



1\. sort() Method:

&#x20;▸The sort() method sorts the elements of a list in ascending order by default.

&#x20;▸It modifies the original list.

&#x20;▸It does not create a new list.



▸Example:

&#x09;numbers = \[5, 2, 8, 1, 3]



&#x09;numbers.sort()

&#x09;print(numbers)

&#x09;#Descending Order:

&#x09;numbers.sort(reverse=True)

&#x09;print(numbers)



▸Output:

&#x09;\[1, 2, 3, 5, 8]

&#x09;\[8, 5, 3, 2, 1]



2\. sorted() Function:



&#x20;▸The sorted() function returns a new sorted list.

&#x20;▸It does not change the original list.

&#x20;▸It can be used with lists, tuples, and other iterable objects.



▸Example:

&#x09;numbers = \[5, 2, 8, 1, 3]



&#x09;new\_list = sorted(numbers)

&#x09;print(new\_list)

&#x09;print(numbers)



▸Output:

&#x09;\[1, 2, 3, 5, 8]

&#x09;\[5, 2, 8, 1, 3]



3\. reverse() Method



&#x20;▸The reverse() method reverses the order of elements in a list.

&#x20;▸It modifies the original list.

&#x20;▸It does not sort the list; it only changes the order.



▸Example:

&#x09;numbers = \[5, 2, 8, 1, 3]



&#x09;numbers.reverse()

&#x09;print(numbers)



▸Output:

&#x09;\[3, 1, 8, 2, 5]



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Basic list manipulations: addition, deletion, updating, and slicing.**



**→** Lists are one of the most flexible data structures in Python.

**→** They allow users to store multiple values and modify them easily.

**→** Common list manipulations include adding elements, deleting elements, updating elements, and slicing lists.

**→** These operations help in managing and organizing data efficiently.



1\. Addition of Elements:



&#x20;▸Elements can be added to a list using methods like append() and insert().

&#x20;▸append() adds an element at the end of the list.

&#x20;▸insert() adds an element at a specific position.



▸Example:

&#x09;fruits = \["Apple", "Banana"]



&#x09;fruits.append("Mango")

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Banana', 'Mango']



2\. Deletion of Elements:



&#x20;▸Elements can be removed using remove(), pop(), or the del keyword.

&#x20;▸remove() deletes a specific value.

&#x20;▸pop() removes an element by index.

&#x20;▸del deletes an element or the entire list.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;fruits.remove("Banana")

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Mango']



3\. Updating Elements:



&#x20;▸List elements can be changed by assigning a new value to a specific index.

&#x20;▸This allows modification of existing data.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango"]



&#x09;fruits\[1] = "Orange"

&#x09;print(fruits)



▸Output:

&#x09;\['Apple', 'Orange', 'Mango']



4\. Slicing a List:



&#x20;▸Slicing is used to access a range of elements from a list.

&#x20;▸The syntax is list\[start:end].

&#x20;▸The start index is included, while the end index is excluded.



▸Example:

&#x09;fruits = \["Apple", "Banana", "Mango", "Orange", "Grapes"]



&#x09;print(fruits\[1:4])



▸Output:

&#x09;\['Banana', 'Mango', 'Orange']



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**4. Tuple:**



**✦ Introduction to tuples, immutability.**



**→** A tuple is a built-in data structure in Python used to store multiple items in a single variable.

**→** Tuples are similar to lists, but the main difference is that tuples are immutable, which means their elements cannot be changed after creation.

**→** Tuples are created using parentheses () and can store different types of data such as integers, strings, and floating-point numbers.



&#x20;1. Creating a Tuple:



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango")

&#x09;print(fruits)



▸Output:

&#x09;('Apple', 'Banana', 'Mango')



2\. Accessing Tuple Elements:



&#x20;▸Tuple elements are accessed using indexes.

&#x20;▸Indexing starts from 0.



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango")



&#x09;print(fruits\[0])

&#x09;print(fruits\[1])



▸Output:

&#x09;Apple

&#x09;Banana



3\. Immutability of Tuples:

&#x20;▸Immutability means that once a tuple is created, its elements cannot be modified, added, or removed.

&#x20;▸This makes tuples more secure and efficient than lists when data should remain unchanged.



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango")



&#x09;fruits\[1] = "Orange"



▸Output:

&#x09;TypeError: 'tuple' object does not support item assignment



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Creating and accessing elements in a tuple.**



**→** A tuple is a collection of ordered elements in Python.

**→** It is similar to a list, but unlike lists, tuples are immutable, meaning their elements cannot be changed after creation.

**→** Tuples are commonly used to store related data that should remain constant throughout the program.



1\. Creating a Tuple



&#x20;▸A tuple is created using parentheses ().

&#x20;▸It can contain elements of different data types such as integers, strings, and floats.

&#x20;▸Elements are separated by commas.



▸Example:

&#x09;student = ("John", 20, "Computer Science")

&#x09;print(student)



▸Output:

&#x09;('John', 20, 'Computer Science')



2\. Accessing Tuple Elements:



&#x20;▸Tuple elements are accessed using their index positions.

&#x20;▸Indexing starts from 0.

&#x20;▸Positive indexing starts from the beginning, while negative indexing starts from the end.



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango", "Orange")



&#x09;print(fruits\[0])

&#x09;print(fruits\[2])



▸Output:

&#x09;Apple

&#x09;Mango



3\. Accessing Elements Using Negative Indexing:



&#x20;▸Negative indexes allow access to elements from the end of the tuple.



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango", "Orange")



&#x09;print(fruits\[-1])

&#x09;print(fruits\[-2])



▸Output:

&#x09;Orange

&#x09;Mango



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Basic operations with tuples: concatenation, repetition, membership.**



**→** Tuples are ordered and immutable collections in Python.

**→** Tuple elements cannot be modified after creation, several operations can be performed on tuples, such as concatenation, repetition, and membership testing.

**→** These operations help in combining tuples, repeating elements, and checking whether an element exists in a tuple.



1\. Concatenation:



&#x20;▸Concatenation means joining two or more tuples into a single tuple.

&#x20;▸It is performed using the + operator.

&#x20;▸A new tuple is created as a result.



▸Example:

&#x09;tuple1 = (1, 2, 3)

&#x09;tuple2 = (4, 5, 6)



&#x09;result = tuple1 + tuple2

&#x09;print(result)



▸Output:

&#x09;(1, 2, 3, 4, 5, 6)



2\. Repetition:



&#x20;▸Repetition means repeating the elements of a tuple multiple times.

&#x20;▸It is performed using the \* operator.

&#x20;▸A new tuple containing repeated elements is created.



▸Example:

&#x09;tuple1 = (1, 2, 3)



&#x09;result = tuple1 \* 3

&#x09;print(result)



▸Output:

&#x09;(1, 2, 3, 1, 2, 3, 1, 2, 3)



3\. Membership Testing:



&#x20;▸Membership operators (in and not in) are used to check whether an element exists in a tuple.

&#x20;▸in returns True if the element is present.

&#x20;▸not in returns True if the element is not present.



▸Example:

&#x09;tuple1 = (1, 2, 3, 4)



&#x09;print(2 in tuple1)

&#x09;print(7 not in tuple1)



▸Output:

&#x09;True

&#x09;True



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**5. Accessing Tuples:**



**✦ Accessing tuple elements using positive and negative indexing.**



**→** A tuple is an ordered collection of elements in Python.

**→** Each element in a tuple has an index number that allows it to be accessed easily.

**→** Python supports both positive indexing and negative indexing for accessing tuple elements.



▸Example:

&#x09;fruits = ("Apple", "Banana", "Mango", "Orange")



1\. Positive Indexing:

&#x20;▸Positive indexing starts from the beginning of the tuple.

&#x20;▸The first element has index 0.

&#x20;▸The second element has index 1, and so on.

&#x20; | Index | Element |

&#x20; | ----- | ------- |

&#x20; | 0     | Apple   |

&#x20; | 1     | Banana  |

&#x20; | 2     | Mango   |

&#x20; | 3     | Orange  |



▸Example:

&#x09;print(fruits\[0])

&#x09;print(fruits\[2])



▸Output:

&#x09;Apple

&#x09;Mango



2\. Negative Indexing:

&#x20;▸Negative indexing starts from the end of the tuple.

&#x20;▸The last element has index -1.

&#x20;▸The second last element has index -2, and so on.

&#x20; | Index | Element |

&#x20; | ----- | ------- |

&#x20; | -1    | Orange  |

&#x20; | -2    | Mango   |

&#x20; | -3    | Banana  |

&#x20; | -4    | Apple   |



▸Example:

&#x09;print(fruits\[-1])

&#x09;print(fruits\[-2])



▸Output:

&#x09;Orange

&#x09;Mango



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Slicing a tuple to access ranges of elements.**



**→** A tuple is an ordered collection of elements in Python.

**→** Sometimes, instead of accessing a single element, we may need to access a group of elements from a tuple.

**→** This can be done using tuple slicing.

**→** Slicing allows us to extract a specific range of elements from a tuple.



**→** What is Tuple Slicing?

**→** Slicing is used to access multiple elements from a tuple.

**→** It is done using the slicing operator \[:].



▸Syntax:

&#x09;tuple\_name\[start:end]

▸start = Starting index (included)

▸end = Ending index (excluded)



Example:

&#x09;fruits = ("Apple", "Banana", "Mango", "Orange", "Grapes")



1\. Accessing a Range of Elements:



▸Example:

&#x09;print(fruits\[1:4])



▸Output:

&#x09;('Banana', 'Mango', 'Orange')



2\. Accessing Elements from the Beginning:



▸Example:

&#x09;print(fruits\[:3])



▸Output:

&#x09;('Apple', 'Banana', 'Mango')



3\. Accessing Elements up to the End:



▸Example:

&#x09;print(fruits\[2:])



▸Output:

&#x09;('Mango', 'Orange', 'Grapes')



4\. Using Negative Indexing in Slicing:



▸Example:

&#x09;print(fruits\[-4:-1])



▸Output:

&#x09;('Banana', 'Mango', 'Orange')



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**6. Dictionaries:**



**✦ Introduction to dictionaries: key-value pairs.**



**→** A dictionary is a built-in data structure in Python used to store data in the form of key-value pairs.

**→** Each key in a dictionary is unique and is used to access its corresponding value.

**→** Dictionaries are useful for organizing and retrieving data efficiently.



**→**What is a Key-Value Pair?

**→**A key is a unique identifier.

**→**A value is the data associated with that key.

**→**Each key is separated from its value by a colon (:).

**→**Key-value pairs are enclosed within curly braces {}.



1.Create A Dictionary:



▸Example:

&#x09;student = {

&#x20;   		"name": "John",

&#x20;   		"age": 20,

&#x20;   		"course": "Python"

&#x09;}



&#x09;print(student)



▸Output:

&#x09;{'name': 'John', 'age': 20, 'course': 'Python'}



2.Accessing Values in a Dictionary:



&#x20;▸Values are accessed using their keys.

&#x20;▸Square brackets \[] are used to specify the key.



▸Example:

&#x09;student = {

&#x09;    "name": "John",

&#x09;    "age": 20,

&#x09;    "course": "Python"

&#x09;}



&#x09;print(student\["name"])

&#x09;print(student\["age"])



▸Output:

&#x09;John

&#x09;20



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Accessing, adding, updating, and deleting dictionary elements.**



**→** A dictionary is a Python data structure that stores data in the form of key-value pairs.

**→** Dictionaries are mutable, which means their elements can be added, updated, or deleted after creation.

**→** These operations make dictionaries flexible and useful for managing data.



▸Example:

&#x09;student = {

&#x09;    "name": "John",

&#x09;    "age": 20,

&#x09;    "course": "Python"

&#x09;}



1\. Accessing Dictionary Elements:



&#x20;▸Dictionary values are accessed using their keys.

&#x20;▸Square brackets \[] are used to specify the key.



▸Example:

&#x09;print(student\["name"])

&#x09;print(student\["age"])



▸Output:

&#x09;John

&#x09;20



2\. Adding Dictionary Elements:



&#x20;▸New key-value pairs can be added by assigning a value to a new key.

&#x20;▸If the key does not exist, it is added to the dictionary.



▸Example:

&#x09;student\["city"] = "Ahmedabad"

&#x09;print(student)



▸Output:

&#x09;{'name': 'John', 'age': 20, 'course': 'Python', 'city': 'Ahmedabad'}



3\. Updating Dictionary Elements:



&#x20;▸Existing values can be modified by assigning a new value to an existing key.



▸Example:

&#x09;student\["age"] = 21

&#x09;print(student)



▸Output:

&#x09;{'name': 'John', 'age': 21, 'course': 'Python'}



4\. Deleting Dictionary Elements:



&#x20;▸Elements can be removed using del or pop().

&#x20;▸del removes a key-value pair permanently.

&#x20;▸pop() removes a key and returns its value.



▸Example:

&#x09;del student\["course"]

&#x09;print(student)

&#x09;

&#x09;student.pop("age")

&#x09;print(student)





▸Output:

&#x09;{'name': 'John', 'age': 20}

&#x09;{'name': 'John', 'course': 'Python'}



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Dictionary methods like keys(), values(), and items().**



**→** Dictionaries in Python provide several built-in methods that help us access and work with stored data efficiently.

**→**The most commonly used dictionary methods are keys(), values(), and items().

**→** These methods allow users to retrieve dictionary keys, values, and key-value pairs.



▸Example:

&#x09;student = {

&#x09;    "name": "John",

&#x09;    "age": 20,

&#x09;    "course": "Python"

&#x09;}



1\. keys() Method:



&#x20;▸The keys() method returns all the keys present in the dictionary.

&#x20;▸It helps when we need only the key names.



▸Example:

&#x09;print(student.keys())



▸Output:

&#x09;dict\_keys(\['name', 'age', 'course'])



2\. values() Method:



&#x20;▸The values() method returns all the values stored in the dictionary.

&#x20;▸It helps when we need only the values.



▸Example:

&#x09;print(student.values())



▸Output:

&#x09;dict\_values(\['John', 20, 'Python'])



3\. items() Method:



&#x20;▸The items() method returns all key-value pairs as tuples.

&#x20;▸Each tuple contains one key and its corresponding value.



▸Example:

&#x09;print(student.items())



▸Output:

&#x09;dict\_items(\[('name', 'John'), ('age', 20), ('course', 'Python')])



▸Using These Methods with Loops:

Iterating Through Keys

&#x09;for key in student.keys():

&#x09;    print(key)



Iterating Through Values

&#x09;for value in student.values():

&#x09;    print(value)



Iterating Through Key-Value Pairs

&#x09;for key, value in student.items():

&#x09;    print(key, ":", value)



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**7. Working with Dictionaries:**



**✦ Iterating over a dictionary using loops.**



**→** A dictionary stores data in the form of key-value pairs.

**→** Sometimes, we need to access all the keys, values, or key-value pairs in a dictionary.

**→** This process is called iteration.

**→** Python provides loops, especially the for loop, to iterate through dictionaries efficiently.



▸Example:

&#x09;student = {

&#x09;    "name": "John",

&#x09;    "age": 20,

&#x09;    "course": "Python"

&#x09;}



1\. Iterating Through Keys:



&#x20;▸By default, a for loop iterates through the keys of a dictionary.

&#x20;▸Each key is accessed one by one.



▸Example:

&#x09;for key in student:

&#x09;    print(key)



▸Output:

&#x09;name

&#x09;age

&#x09;course



2\. Iterating Through Values:



&#x20;▸The values() method is used to access all values in the dictionary.



▸Example:

&#x09;for value in student.values():

&#x09;    print(value)



▸Output:

&#x09;John

&#x09;20

&#x09;Python



3\. Iterating Through Key-Value Pairs:



&#x20;▸The items() method returns both keys and values together.

&#x20;▸It is useful when both pieces of information are needed.



▸Example:

&#x09;for key, value in student.items():

&#x09;    print(key, ":", value)



▸Output:



&#x09;name : John

&#x09;age : 20

&#x09;course : Python



4\. Iterating Through Keys Using keys():



&#x20;▸The keys() method explicitly returns all keys in the dictionary.



▸Example:

&#x09;for key in student.keys():

&#x09;    print(key)



▸Output:

&#x09;name

&#x09;age

&#x09;course



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Merging two lists into a dictionary using loops or zip().**



**→**In Python, it is often necessary to combine two lists into a dictionary.

**→** One list contains the keys, and the other contains the values.

**→** This can be done using a loop or the built-in zip() function.



▸Example:

&#x09;keys = \["name", "age", "course"]

&#x09;values = \["John", 20, "Python"]



1\. Using a Loop:



&#x20;▸Create an empty dictionary.

&#x20;▸Use a loop to assign each key to its corresponding value.

&#x20;▸Add the key-value pair to the dictionary.



▸Example:

&#x09;keys = \["name", "age", "course"]

&#x09;values = \["John", 20, "Python"]



&#x09;student = {}



&#x09;for i in range(len(keys)):

&#x09;    student\[keys\[i]] = values\[i]



&#x09;print(student)



▸Output:

&#x09;{'name': 'John', 'age': 20, 'course': 'Python'}



2\. Using zip():



&#x20;▸The zip() function combines elements from two lists into pairs.

&#x20;▸These pairs can be directly converted into a dictionary using dict().



▸Example:

&#x09;keys = \["name", "age", "course"]

&#x09;values = \["John", 20, "Python"]



&#x09;student = dict(zip(keys, values))



&#x09;print(student)



▸Output:

&#x09;{'name': 'John', 'age': 20, 'course': 'Python'}



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Counting occurrences of characters in a string using dictionaries.**



**→** A dictionary can be used to count how many times each character appears in a string.

**→** In this approach, each character is stored as a key, and its count is stored as the corresponding value.

**→** This is a common use of dictionaries for frequency counting and data analysis.



**→** Steps to Count Characters

**→** Create an empty dictionary.

**→**Traverse each character in the string using a loop.

**→** If the character already exists in the dictionary, increase its count by 1.

**→** Otherwise, add the character to the dictionary with a count of 1.



▸Example:

&#x09;text = "hello"



&#x09;count = {}



&#x09;for char in text:

&#x09;    if char in count:

&#x09;        count\[char] += 1

&#x09;    else:

&#x09;        count\[char] = 1



&#x09;print(count)



▸Output:

&#x09;{'h': 1, 'e': 1, 'l': 2, 'o': 1}



**→** The dictionary stores these counts as key-value pairs.



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**8. Functions:**



**✦ Defining functions in Python.**



**→** A function is a block of organized and reusable code that performs a specific task. 

**→** Functions help reduce code repetition, improve readability, and make programs easier to maintain.

**→** In Python, functions are defined using the def keyword.



**→** Why Use Functions?

&#x09;**→**Avoids writing the same code multiple times.

&#x09;**→**Makes programs easier to understand.

&#x09;**→**Improves code reusability.

&#x09;**→**Simplifies debugging and maintenance.



▸Syntax:

&#x09;def function\_name():

&#x09;    # Function body

&#x09;    statements



▸Example:

&#x09;def greet():

&#x09;    print("Hello, Welcome to Python!")



&#x09;greet()



▸Output:

&#x09;Hello, Welcome to Python!



1.Function with Parameters:



&#x20;▸Parameters are values passed to a function.

&#x20;▸They allow the function to work with different inputs.



▸Example:

&#x09;def greet(name):

&#x09;    print("Hello,", name)



&#x09;greet("John")



▸Output:

&#x20;	Hello, John



2.Function with Return Value:



&#x20;▸A function can return a value using the return statement.

&#x20;▸The returned value can be stored in a variable or used directly.



▸Example:

&#x09;def add(a, b):

&#x09;    return a + b



&#x09;result = add(5, 3)

&#x09;print(result)



▸Output:

&#x09;8



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Different types of functions: with/without parameters, with/without return values.**



**→** Functions in Python can be classified based on whether they accept parameters and whether they return values.

**→** Understanding these types of functions helps programmers write flexible and reusable code.



1\. Function Without Parameters and Without Return Value:



&#x20;▸This type of function does not take any input from the user.

&#x20;▸It does not return any value.

&#x20;▸It simply performs a task when called.



▸Example:

&#x09;def greet():

&#x09;    print("Hello, Welcome to Python!")



&#x09;greet()



▸Output:

&#x09;Hello, Welcome to Python!



2\. Function With Parameters and Without Return Value:



&#x20;▸This type of function accepts input values through parameters.

&#x20;▸It does not return any value.

&#x20;▸It performs an action using the provided inputs.



▸Example:

&#x09;def greet(name):

&#x09;    print("Hello,", name)



&#x09;greet("John")



▸Output:

&#x09;Hello, John



3\. Function Without Parameters and With Return Value:



&#x20;▸This type of function does not take any input.

&#x20;▸It returns a value using the return statement.



▸Example:

&#x09;def get\_number():

&#x09;    return 100



&#x09;num = get\_number()

&#x09;print(num)



▸Output:

&#x09;100



4\. Function With Parameters and With Return Value:

&#x20;

&#x20;▸This type of function accepts input values through parameters.

&#x20;▸It processes the inputs and returns a result.

&#x20;▸It is the most commonly used type of function.



▸Example:

&#x09;def add(a, b):

&#x09;    return a + b



&#x09;result = add(5, 3)

&#x09;print(result)



▸Output:

&#x09;8



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Anonymous functions (lambda functions).**



**→** In Python, an anonymous function is a function that is defined without a name.

**→** These functions are created using the lambda keyword and are therefore called lambda functions.

**→** Lambda functions are generally used for short and simple operations where creating a regular function is unnecessary.



**→** What is a Lambda Function?

&#x09;**→**A lambda function is a small, single-line function.

&#x09;**→**It can have any number of arguments but only one expression.

&#x09;**→**The value of the expression is automatically returned.

&#x09;**→**It is useful for simple tasks and temporary function definitions.



▸Syntax:

&#x09;lambda arguments: expression



▸lambda is the keyword used to create an anonymous function.

▸arguments are the input parameters.

▸expression is evaluated and returned automatically.



1.Lambda Function for Addition:



▸Example 1:

&#x09;add = lambda a, b: a + b



&#x09;print(add(5, 3))



▸Output:

&#x09;8



2.Lambda Function for Squaring a Number:

▸Example :

&#x09;square = lambda x: x \* x



&#x09;print(square(4))



▸Output:

&#x09;16



3.Using Lambda in sorted():



▸Example:

&#x09;numbers = \[(1, 3), (4, 1), (2, 2)]



&#x09;result = sorted(numbers, key=lambda x: x\[1])



&#x09;print(result)



▸Output:

&#x09;\[(4, 1), (2, 2), (1, 3)]



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**9. Modules:**



**✦ Introduction to Python modules and importing modules.**



**→** A module in Python is a file that contains Python code such as functions, variables, and classes.

**→** Modules help organize code into separate files, making programs easier to manage, reuse, and maintain.

**→** Python provides many built-in modules, and users can also create their own modules.



**→** What is a Module?

&#x09;**→**A module is a Python file with a .py extension.

&#x09;**→**It contains reusable code.

&#x09;**→**Modules help divide large programs into smaller, manageable parts.

&#x09;**→**They improve code organization and reusability.

**→**Why Use Modules?

&#x09;**→**Avoid rewriting the same code.

&#x09;**→**Improve program organization.

&#x09;**→**Make code easier to maintain.

&#x09;**→**Allow code sharing between different programs.

&#x09;**→**Importing a Module

&#x09;**→**To use a module, it must first be imported using the import keyword.



▸Example:

&#x09;import math

&#x09;print(math.sqrt(25))



▸Output:

&#x09;5.0



▸Importing Specific Functions:

&#x20;▸Instead of importing the entire module, specific functions can be imported.



▸Example:

&#x09;from math import sqrt

&#x09;print(sqrt(36))



▸Output:

&#x09;6.0



▸Importing with an Alias:

&#x20;▸An alias is a short name given to a module using the as keyword.



▸Example:

&#x09;import math as m

&#x09;print(m.pi)



▸Output:

&#x09;3.141592653589793



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Standard library modules: math, random.**



**→**Python comes with a Standard Library, which is a collection of built-in modules that provide useful functions and features.

**→** Two commonly used modules are math and random.

**→** These modules help perform mathematical calculations and generate random values without writing complex code.



1\. The math Module:



&#x20;▸The math module provides mathematical functions and constants.

&#x20;▸It is useful for calculations such as square roots, powers, trigonometry, and more.

&#x20;▸To use it, the module must be imported first.



▸Example:

&#x09;import math

&#x09;print(math.sqrt(25))

&#x09;print(math.pow(2, 3))

&#x09;print(math.pi)



▸Output:

&#x09;5.0

&#x09;8.0

&#x09;3.141592653589793

▸Common Functions in math:

| Function            | Description                     |

| ------------------- | ------------------------------- |

| `math.sqrt(x)`      | Returns the square root of x    |

| `math.pow(x, y)`    | Returns x raised to the power y |

| `math.pi`           | Returns the value of π (pi)     |

| `math.factorial(x)` | Returns the factorial of x      |

| `math.ceil(x)`      | Rounds a number up              |

| `math.floor(x)`     | Rounds a number down            |



2\. The random Module:



&#x20;▸The random module is used to generate random numbers and select random items.

&#x20;▸It is useful in games, simulations, and testing applications.



▸Example:

&#x09;import random

&#x09;print(random.randint(1, 10))



▸Output:

&#x09;7



▸Selecting a Random Element

&#x09;import random

&#x09;fruits = \["Apple", "Banana", "Mango"]

&#x09;print(random.choice(fruits))



▸Output:

&#x09;Banana



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**✦ Creating custom modules.**



**→** A custom module is a Python file created by the user to store functions, variables, and classes that can be reused in other Python programs.

**→** Custom modules help organize code, improve readability, and promote code reuse.



**→** What is a Custom Module?

&#x09;**→**A custom module is a Python file with a .py extension.

&#x09;**→**It contains reusable code written by the programmer.

&#x09;**→**It can be imported and used in other Python programs.



▸Steps to Create a Custom Module



Step 1: Create a Python File

&#x20;▸Create a file named mymodule.py.

&#x09;def greet(name):

&#x09;    return "Hello, " + name



&#x09;def add(a, b):

&#x09;    return a + b



Step 2: Import the Module

&#x20;▸Create another Python file and import the custom module.

&#x09;import mymodule

&#x09;print(mymodule.greet("John"))	

&#x09;print(mymodule.add(5, 3))



▸Output:

&#x09;Hello, John

&#x09;8



▸Importing Specific Functions

&#x20;▸Instead of importing the entire module, specific functions can be imported.

&#x09;from mymodule import greet

&#x09;print(greet("John"))



▸Output:

&#x09;Hello, John

&#x09;Using an Alias



▸A module can be imported with a shorter name using the as keyword.

&#x09;import mymodule as mm

&#x09;print(mm.add(10, 5))



▸Output:

&#x09;15



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**10.  Functions and Methods**



**• Function arguments (positional, keyword, default).**



**→** Function arguments are values passed to a function when it is called.

**→** They allow functions to work with different data and make programs more flexible.

**→** Python supports different types of arguments, including positional arguments, keyword arguments, and default arguments.



1\. Positional Arguments:

&#x20;

▸In positional arguments, values are passed in the same order as the parameters are defined.

▸The position of each argument is important.



▸Example:

&#x09;def student(name, age):

&#x09;    print("Name:", name)

&#x09;    print("Age:", age)



&#x09;student("John", 20)



▸Output:

&#x09;Name: John	

&#x09;Age: 20



2\. Keyword Arguments:



&#x20;▸In keyword arguments, values are passed using the parameter names.

&#x20;▸The order of arguments does not matter.



▸Example:

&#x09;def student(name, age):

&#x09;    print("Name:", name)

&#x09;    print("Age:", age)



&#x09;student(age=20, name="John")



▸Output:

&#x09;Name: John

&#x09;Age: 20



3\. Default Arguments:



&#x20;▸Default arguments have predefined values.

&#x20;▸If no value is provided during the function call, the default value is used.



▸Example:

&#x09;def greet(name="Guest"):

&#x09;     print("Hello,", name)

&#x09;greet()

&#x09;greet("John")



▸Output:

&#x09;Hello, Guest

&#x09;Hello, John



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**• Scope of variables in Python.**



**→** The scope of a variable refers to the region of a program where a variable can be accessed.

**→** In Python, variables can have different scopes depending on where they are declared.

**→** Understanding variable scope helps avoid errors and makes programs easier to manage.



**→**Types of Variable Scope in Python:

1\. Local Scope:



&#x20;▸A variable declared inside a function is called a local variable.

&#x20;▸It can only be accessed within that function.

&#x20;▸It is destroyed when the function finishes execution.



▸Example:

&#x09;def greet():

&#x09;    message = "Hello"

&#x09;    print(message)

&#x09;

&#x09;greet()



▸Output:

&#x09;Hello



▸Here, message is a local variable and cannot be accessed outside the function.



2\. Global Scope:



&#x20;▸A variable declared outside all functions is called a global variable.

&#x20;▸It can be accessed from anywhere in the program.



▸Example:

&#x09;name = "John"



&#x09;def display():

&#x09;    print(name)



&#x09;display()

&#x09;print(name)



▸Output:	

&#x09;John

&#x09;John



▸Here, name is a global variable.



3\. Using the global Keyword:



&#x20;▸The global keyword allows a function to modify a global variable.

&#x20;▸Without global, changes inside the function create a new local variable.



▸Example:

&#x09;count = 10



&#x09;def update():

&#x09;    global count

&#x09;    count = 20



&#x09;update()

&#x09;print(count)



▸Output:

&#x09;20



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**



**11. Generators and Iterators**



**• Understanding how generators work in Python.**



**→** A generator is a special type of function in Python that generates values one at a time instead of returning all values at once.

**→** Generators are useful when working with large amounts of data because they save memory and improve performance.

**→** Generators use the yield keyword instead of the return keyword.



**→**What is a Generator?

&#x09;**→**A generator is a function that produces a sequence of values.

&#x09;**→**It uses yield to return values one by one.

&#x09;**→**The function pauses after each yield and resumes from the same point when called again.

&#x09;**→**Generators are memory-efficient because they do not store all values at once.



▸Creating a Generator



▸Example:

&#x09;def numbers():

&#x09;    yield 1

&#x09;    yield 2

&#x09;    yield 3



&#x09;gen = numbers()



&#x09;print(next(gen))

&#x09;print(next(gen))

&#x09;print(next(gen))



▸Output:

&#x09;1

&#x09;2

&#x09;3



&#x20;▸yield returns a value and pauses the function.

&#x20;▸The function remembers its state.

&#x20;▸On the next call, execution continues from where it stopped.



▸Example:

&#x09;def count():

&#x09;    yield 1

&#x09;    yield 2

&#x09;    yield 3



&#x09;for num in count():

&#x09;    print(num)



▸Output:

&#x09;1

&#x09;2

&#x09;3



▸Generator vs Normal Function



1.Normal Function

&#x09;def numbers():

&#x09;    return \[1, 2, 3]



&#x09;print(numbers())



▸Output:

&#x09;\[1, 2, 3]



2.Generator Function

&#x09;def numbers():

&#x09;    yield 1

&#x09;    yield 2

&#x09;    yield 3



&#x09;print(numbers())



▸Output:

&#x09;<generator object numbers at ...>



▸Real-Life Example

&#x09;def even\_numbers():

&#x09;    for i in range(2, 11, 2):

&#x09;        yield i



&#x09;for num in even\_numbers():

&#x09;    print(num)



▸Output:

&#x09;2

&#x09;4

&#x09;6

&#x09;8

&#x09;10



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**• Difference between yield and return.**



**→** In Python, both yield and return are used inside functions, but they work differently.

**→** The return statement ends the function and sends back a value, whereas yield pauses the function and generates values one at a time.



1\. return Statement:



&#x20;▸Used in normal functions.

&#x20;▸Returns a value and terminates the function.

&#x20;▸After return is executed, the function ends.



▸Example:

&#x09;def add(a, b):

&#x09;    return a + b



&#x09;result = add(5, 3)

&#x09;print(result)



▸Output:	

&#x09;8



2\. yield Statement:

&#x20;▸Used in generator functions.

&#x20;▸Returns a value and pauses the function.

&#x20;▸The function resumes from the same point when called again.

&#x20;▸Generates values one at a time.



▸Example:

&#x09;def numbers():

&#x09;    yield 1

&#x09;    yield 2

&#x09;    yield 3



&#x09;gen = numbers()



&#x09;print(next(gen))

&#x09;print(next(gen))

&#x09;print(next(gen))



▸Output:

&#x09;1

&#x09;2

&#x09;3



▸Difference Between yield and return:



| `return`                         | `yield`                              |

| -------------------------------- | ------------------------------------ |

| Ends the function completely     | Pauses the function temporarily      |

| Returns a single value           | Generates multiple values one by one |

| Used in normal functions         | Used in generator functions          |

| Does not save function state     | Saves function state between calls   |

| More memory usage for large data | More memory efficient                |



**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**



**• Understanding iterators and creating custom iterators.**



**→** An iterator is an object in Python that allows you to traverse through a collection of data one element at a time.

**→** Iterators are used in loops such as the for loop to access elements sequentially.



**→** What is an Iterator?

&#x09;**→**An iterator is an object that can be iterated upon.

&#x09;**→**It returns one element at a time.

&#x09;**→**It keeps track of its current position.

&#x09;**→**It uses the methods \_\_iter\_\_() and \_\_next\_\_().



▸Creating an Iterator from a List



▸Example:

&#x09;numbers = \[10, 20, 30]

&#x09;it = iter(numbers)

&#x09;print(next(it))

&#x09;print(next(it))

&#x09;print(next(it))



▸Output:

&#x09;10

&#x09;20

&#x09;30



▸How Iterators Work

▸iter() converts an iterable object into an iterator.

▸next() retrieves the next value from the iterator.

▸When no elements remain, Python raises a StopIteration exception.



▸Creating a Custom Iterator



▸To create a custom iterator, define a class with:



&#x09;\_\_iter\_\_() method

&#x09;\_\_next\_\_() method



▸Example:

&#x09;class Counter:

&#x09;    def \_\_init\_\_(self, max):

&#x09;        self.max = max

&#x09;        self.num = 1



&#x09;    def \_\_iter\_\_(self):

&#x09;        return self



&#x09;    def \_\_next\_\_(self):

&#x09;        if self.num <= self.max:

&#x09;            value = self.num

&#x09;            self.num += 1

&#x09;            return value

&#x09;        else:

&#x09;            raise StopIteration



&#x09;counter = Counter(5)



&#x09;for i in counter:

&#x09;    print(i)



▸Output:



&#x09;1

&#x09;2

&#x09;3

&#x09;4

&#x09;5



▸Explanation

▸\_\_iter\_\_() returns the iterator object itself.

▸\_\_next\_\_() returns the next value.

▸When all values are generated, StopIteration stops the loop.



**════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════**

