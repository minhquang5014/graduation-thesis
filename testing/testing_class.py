class Testing:
    def __init__(self):
        self.test = "test"
        self.print_test()
    def print_test(self):
        print(self.test)

def print_name():
    print(f"Hello World!")


"""Method number 1"""
class ExtendedTesting(Testing):
    def __init__(self):
        super().__init__()  # Call original __init__
        print_name()        # Add your custom behavior
ExtendedTesting()


"""Method number 2"""
original_init = Testing.__init__

def new_init(self):
    original_init(self)  # Call the original
    print_name()         # Add your code

# Monkey patch the class
Testing.__init__ = new_init

# Usage
Testing()