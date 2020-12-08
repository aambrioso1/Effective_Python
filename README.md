# Effective_Python
Code and notes from Brett Slatkin's Effective Python (2nd Edition)

This book gives lots of ideas and examples that will help the reader write better Python code.  But more importantly, it gives insight into how to write clear code in general.   The book also teaches how to write ABOUT code.   An example is the nice phrase "visually noisy" for code that is more difficult to read than it needs to be.  One other thing I really like about the book is that Slatkin explains his choices.  This habit helps the reader learn to handle coding decisions beyond the specific examples given in the book.  The section on interpolated f-strings (Item 4) is an excellent example of this.   In that section, Slatkin shows precisely the advantages using f-strings has over other ways of formatting in Python.  

You can purchase the book here:  https://effectivepython.com/

Items 30, 32, and 33 provide a nice introduction to generators along with some good advice.


All the code for Slatkin's book, along with some nice improvements, can be found here: 
https://github.com/bslatkin/effectivepython/tree/master/example_code

One nice improvement in the GitHub code is the use of exemption handling (try/except/else) so that the code for each item will run even when the point of the code is to show an error.  It makes sense to leave this out of the book but if you are running the code it is nice that the parts with deliberate errors in them are easy to spot and won't crash the rest of the code.  For an example, see Item 13.  Another improvement is that dummy functions left to the imagination in the book are implemented in the GitHub code.  For an example, see Item 10.  Another example is can be found in Item 30 where the book shows a small snippet of the text for the Gettyburg address.   In the code, Slatkin includes more the text so that the code later in the item will run.  Throughout, the GitHub code for the book is written so that it will run as is.