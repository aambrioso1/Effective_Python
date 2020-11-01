"""
Item 21:  Know How Closures Interact with Variable Scope

Shows that Python supports closures and the functions are first class objects in Python.  
This item also shows how to use a helper function to sort data but prioritize a subset of the data.
Recommend wrapping the sorting function with a helper class to avoid scoping issues.

"""

class Sorter:
	def __init__(self, group):
		self.group = group
		self.found = False

	def __call__(self, x):
		if x in self.group:
			self.found = True
			return (0, x)
		return (1, x)


numbers = [8, 3, 1, 2, 5, 7, 4, 6]
group = {9, 10} # {2, 3, 5, 7}

sorter = Sorter(group)
numbers.sort(key=sorter)
print(numbers)
print(sorter.found)
assert sorter.found is True