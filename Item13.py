"""
Item 13:  Prefer Catch-All Unpacking Over Slicing

"""


# Example 1:  Noteworthy for use of try/except/else to keep code running.
import logging

try:
    car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
    car_ages_descending = sorted(car_ages, reverse=True)
    oldest, second_oldest = car_ages_descending
except:
    logging.exception('Expected')
else:
    assert False

# Example 2:  Typical way to pull elements using indexing and slicing.
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)

# Example 3:  The better way:  catch-all unpacking through starred expressions.
# "This code is shorter, easier to read, and no longer has the error-prone brittleness of boundary indexes...."
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# Example 4:  Starred expression can appear in any position.
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)

# Example 5: Can't use starred expression on their own.
try:
    # This will not compile
    source = """*others = car_ages_descending"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 6:  Can't use multiple starred expressions at a single level.
try:
    # This will not compile
    source = """first, *middle, *second_middle, last = [1, 2, 3, 4]"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7:  Can use multiple starred expression on different parts of a multilevel structure.
# For example, this sort of unpacking could be very useful for cherry-picking data from a JASON file.
car_inventory = {
	'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
	'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')


# Example 8: Catch-all expression will return an empty list if nothing is left-over.
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)


# Example 9:  
it = iter(range(1, 3))
first, second = it
print(f'{first} and {second}')


# Example 10
def generate_csv():
	yield ('Date', 'Make' , 'Model', 'Year', 'Price')
	for i in range(100):
		yield ('2019-03-25', 'Honda', 'Fit' , '2010', '$3400')
		yield ('2019-03-26', 'Ford', 'F150' , '2008', '$2400')


# Example 11:  Multilevel unpacking with indexes and slices is visually noising (nice phrase)
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print(all_csv_rows[0:5]) # I put this in so I could take a look at the file.
print('CSV Header:', header)
print('Row count: ', len(rows))


# Example 12:  Less noisy with starred expressions.  
# Be careful with that unpacked items will fit in memory! 
it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

