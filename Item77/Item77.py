"""
Item 77:  Isolate Test from Each Other with setUp, testDown, setUpModule, and tearDownModule 


It is important to write both unit tests (for isolated functionality) and integration tests
(for modules that interact with each other).

Use the setup and tearDown methods to make sure your tests are isolated from each other and have a clean
test environment.


For integration test, use the setUpModule and tearDownModule module-level functions to manage any test
harnesses you need for the entrie lifetime of a test module and all of the TestCase classes that it contains.
[EP, 367]
"""




