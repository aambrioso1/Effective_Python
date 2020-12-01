# Effective_Python
Code and notes from Brett Slatkin's Effective Python (2nd Edition)

This book offers insight into writing Python code, but more importantly, it gives insight into how to write clear code.   The book also teaches about writing ABOUT code.   An example is the nice phrase "visually noisy."   

An other thing I really like about the book is that Slatkin explains his choices.  This habit helps the reader learn to handle coding decisions beyond the specific examples given in the book.  The section on interpolated f-strings (Item 4) is an excellent example of this.   In that section, Slatkin shows precisely the advantages using f-strings have over other ways of formatting in Python.  

All the code, along with some nice improvements, for Slatkin's book can be found here:

https://github.com/bslatkin/effectivepython/tree/master/example_code

One nice improvement in the GitHub code is the use of exemption handling (try/except/else) so that the code for each item will run even when the point of the code is too show an error.  It makes sense to leave this out of the book but if you are running the code it is nice that the parts with deliberate errors in them are easy to spot and won't crash the rest of the code.  See Item 13 for example.  Another improvement is that dummy functions left incomplete and to the imagination in the book are implemented in the GitHub code.  See Item 10 for example.  
