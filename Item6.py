"""
Item 6:  Prefer Multiple Assignments Unpacking Over Indexing
"""

# Muliple level unpacking - good to know.   Unpacking can be applied to any iterable.
favorite_snacks = {
	'salty': ('pretzels', 100),
	'sweet': ('cookies', 180),
	'veggie': ('carrots', 20),
}

((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()

print(f'Favorite {type1} is {name1} with {cals1} calories')
print(f'Favorite {type2} is {name2} with {cals2} calories')
print(f'Favorite {type3} is {name3} with {cals3} calories')


def bubble_sort(a):
	for _ in range(len(a)):
		for i in range(1, len(a)):
			if a[i] < a[i-1]:
				temp = a[i]
				a[i] = a[i-1]
				a[i-1] = temp

names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)

def bubble_sort2(a):
	for _ in range(len(a)):
		for i in range(1, len(a)):
			if a[i] < a[i-1]:
				a[i-1], a[i] = a[i], a[i-1] # swap in place


names = ['pretzels', 'carrots', 'arugula', 'bacon', 'lettuce']
bubble_sort2(names)
print(names)

snacks = [('bacon', 350), ('donut', 240), ('muffin', 190), ('eggs', 175)]

for rank, (name, calories) in enumerate(snacks, 1):
	print(f'#{rank}: {name} has {calories} calories')
