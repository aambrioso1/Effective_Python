"""
Item 33: Compose Multiple Generators with yield from

This example compares using for/yield (manual nesting) and yield/from (composed nesting) for nesting generators.
The yield/from expression improves readability and performance.
"""

# Example 1:  We create a couple of generators
def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0


# Example 2:  We nest the generators using for/yield.
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


# Example 3:   Example 1, 2, and 3 show that for/yield expressions when 
# layering generators leads to redundent code that is difficult to follow.
def render(delta):
    print(f'Delta: {delta:.1f}')
    # Move the images onscreen

def run(func):
    for delta in func():
        render(delta)

print('Using for/yield expressions')
run(animate)


# Example 4:  The yield/from expression looks like it renders all the value that need to be
# generating at one by handling the looping code for you.
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)
print('\nUsing yield/from expressions')
run(animate_composed)


# Example 5:  We used timeit to show the performance improvement of yield/from over for/yield expressions.
import timeit

# Create a generator using range.
def child():
    for i in range(1_000_000):
        yield i

def slow():
	# Nest the child generator with another one using for/yield.
	# Slatkin call this manual nesting.
    for i in child():
        yield i

def fast():
	# Nest the child generator with another one using yield/from
	# Slatkin call this composed nesting.
    yield from child()

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f'Manual nesting {baseline:.2f}s')

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f'Composed nesting {comparison:.2f}s')

reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} less time')