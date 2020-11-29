"""
Item 10:  Prevent Repetitions with Assignment Expressions (walrus operator := )

"""
fresh_fruit = {
	'apple': 10,
	'banana': 1,
	'lemon': 5,
}

def make_cider(n):
	return 'cider'

def make_lemonade(count):
	return 'lemonade'

def slice_bananas(count):
	return 4*count

def OutOfBananas(Exception):
	pass

def out_of_stock():
	'out_of_stock'

def make_smoothies(count):
	return 'smoothies'


if count := fresh_fruit.get('lemon', 0):
	print(make_lemonade(count))
else:
	print(out_of_stock())

if (count := fresh_fruit.get('apple',0)) >= 4:
	print(make_cider(count))
else:
	print(out_of_stock())

if (count := fresh_fruit.get('pear',0)):
	print(count)
else:
	print('no pears')

print(f'fresh_fruit = {fresh_fruit}')


if (count := fresh_fruit.get('banana', 0)) >= 2:
	pieces = slice_bananas(count)
else:
	pieces = 0

try:
	smoothies = make_smoothies(pieces)
except OutOfBananas:
	out_of_stock()

# Using the walrus operator for implementing a flexible switch/case-like statement

if  (count := fresh_fruit.get('banana', 0) >= 2):
	pieces = slice_bananas(count)
	to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0) >= 4):
	to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
	to_enjoy = make_lemonade(count)
else:
	to_enjoy = 'nothing'

# Use the walrus operator to write better code do/while loops

def pick_fruit():
	pass

def make_juice():
	pass

bottles = []
while fresh_fruit := pick_fruit():
	for fruit, count in fresh_fruit.items():
		batch = make_juice(fruit, count)
		bottles.extend(batch)

print(to_enjoy)
