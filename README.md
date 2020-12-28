# Effective_Python
Code and notes from Brett Slatkin's Effective Python (2nd Edition)

This book gives lots of ideas and examples that will help the reader write better Python code.  But more importantly, it gives insight into how to write clear code in general.   The book also teaches how to write ABOUT code.   An example is the nice phrase "visually noisy" for code that is more difficult to read than it needs to be.  One other thing I really like about the book is that Slatkin explains his choices.  This habit helps the reader learn how to think about coding decisions beyond the specific examples given in the book.  The section on interpolated f-strings (Item 4) is an excellent example of this.   In that section, Slatkin shows precisely the advantages using f-strings has over other ways of formatting in Python.   He sprinkles nice examples of using f-strings throughout the book.    

You can purchase the book here:  https://effectivepython.com/

All the code for Slatkin's book, along with some nice improvements, can be found here: 
https://github.com/bslatkin/effectivepython/tree/master/example_code

I have added notes and more examples to all the code which you can find here:
https://github.com/aambrioso1/Effective_Python

Items 30, 32, and 33 provide a nice introduction to generators along with some good advice.

Item 36 points out the more important functions in the itertools built-in module for organizing and interacting with iterators by linking iterators together, filtering items from an iterator, and producing combinations of items from an iterator.

Item 37 is a good example of the using classes in Python.   The example also using the namedtuple class from the built-in collections module.   Slatkin using a nice approach.   He begins with an code that works well for a simple case but gets more difficult to follow as the code is adjust for additional requirements.  Then he refactors the code, with the namedtuple playing a role, to make it easier to follow and more adaptable.


One nice improvement in the GitHub code is the use of exemption handling (try/except/else) so that the code for each item will run even when the point of the code is to show an error.  It makes sense to leave this out of the book but if you are trying out the code it is nice that the parts with deliberate errors in them are easy to spot and won't crash the rest of the code.  For an example, see Item 13.  Another improvement is that dummy functions and variables left to the imagination in the book are implemented in the GitHub code.  For an example, see Item 10.  Another example of this can be found in Item 30 where the book shows a small snippet of the text for the Gettysburg address.   In the GitHub code, Slatkin includes more of the text so that the item will run.  Throughout, the GitHub code for the book is written so that it will run as is.