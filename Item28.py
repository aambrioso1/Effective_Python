"""
Item 28:  Avoid More Than Two Control Subexpressions in Comprehensions

"""

# Comprehensions support multiple levels of logs and multiple conditions per loop level.
#  Avoid more than two control subexpressions in comprehensions. After that use if and for 
# statements and write a helper function.  

matrix = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)

squared = [[x**2 for x in row] for row in matrix]
print(squared)

my_lists = [
		[[1, 2, 3], [4, 5, 6]],
		[[7, 8, 9], [10, 11, 12]],
		[[13, 14, 15], [16, 17, 18]]
	]

# Loops versus comprehension.   In this example looping is clearer.

flat_comp = [x for sublist1 in my_lists
			for sublist2 in sublist1
			for x in sublist2]

flat_loop = []
for sublist1 in my_lists:
	for sublist2 in sublist1:
		flat_loop.extend(sublist2)

print(f'flat_comp: {flat_comp}')
print(f'flat_loop: {flat_loop}')

# Comprehensions support multiple conditions.
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0] # Multiple conditions have an implicit and between them.
c = [x for x in a if x > 4 and x % 2 == 0]
print(f'b: {b}')
print(f'c: {c}')

# Conditions can be specified at each level of looping after the for subexpression.
# This example is a bit harder to read but may be a good fit for some situations.
matrix = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
			for row in matrix if sum(row) >= 10]
print(f'filtered: {filtered}')

