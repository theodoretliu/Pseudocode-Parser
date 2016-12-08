# the grandaddy of all the classes. other classes will inherit from this class
class Parent():
    # constructor. set args = None to avoid a weird Python thing that I won't go into
    def __init__(self, args=None, level=-1):
        if args is None:
            self.args = []
        else:
            self.args = args

        self.level = level
        self.parent = None

        if not isinstance(self.args, list):
            self.args = [self.args]

        for arg in self.args:
            arg.set_level(self.level + 1)
            arg.set_parent(self)

    # override the default string function. Instead iterate over the arguments and return their
    # string values
    def __str__(self):
        ret = ""

        for arg in self.args:
            ret += str(arg)

        return ret

    # adds an argument as a child to the object. sets the objects level and parent attributes
    # accordingly
    def add_arg(self, arg):
        if isinstance(arg, str):
            self.args.append(arg)
            return

        arg.set_level(self.level + 1)
        arg.set_parent(self)
        self.args.append(arg)

    # decrease the level of the object (indentation) and decrease the indentation of every one of
    # its children as well
    def decrement_level(self):
        if self.level == 0:
            return

        self.level -= 1
        for arg in self.args:
            arg.decrement_level()

    # bunch of getters
    def get_args(self):
        return self.args

    def get_level(self):
        return self.level

    def get_parent(self):
        return self.parent

    def increment_level(self):
        self.level += 1
        for arg in self.args:
            arg.increment_level()

    # removes the last child of the object
    def remove_arg(self):
        self.args.pop(-1)

    # sets the level of the object to whatever desired
    def set_level(self, level):
        if level < 0:
            return

        if self.level < level:
            while self.level < level:
                self.increment_level()
        else:
            while self.level > level:
                self.decrement_level()

    # changes the parent attribute of the current object
    def set_parent(self, parent):
        self.parent = parent

# class for Print. inherits from the Parent class
class Print(Parent):
    # constructor for Print does not use the super constructor from Parent class because
    # the children of print don't really have "levels" to be set
    def __init__(self, args=None, level=0):
        if args is None:
            self.args = []
        else:
            self.args = args

        self.level = level

        if not isinstance(self.args, list):
            self.args = [self.args]

    # returns the proper Python code for a print with proper indentation
    def __str__(self):
        ret = " " * 4 * self.level + "print("

        ret += ", ".join([str(arg) for arg in self.args])

        ret += ")\n"

        return ret

    # overrides the set_level from Parent again because the children of Print can't have their levels
    # set
    def set_level(self, level):
        self.level = level

# class for a For Loop
class ForLoop(Parent):
    # constructor with lower, upper, iterating variable, args, and level
    # uses the super constructor
    def __init__(self, lower=0, upper=10, var="i", args=None, level=0):
        super().__init__(args, level)

        self.lower = lower
        self.upper = upper
        self.var = var

    # Python code for a loop
    def __str__(self):
        if len(self.args) == 0:
            return " " * 4 * self.level + "for {} in range({}{}):\n".format(
                self.var, (str(self.lower) + ", " if self.lower != 0 else ""), self.upper)

        ret = " " * 4 * self.level + "for {} in range({}{}):\n".format(
            self.var, (str(self.lower) + ", " if self.lower != 0 else ""), self.upper)

        for member in self.args:
            ret += str(member)

        return ret

    # getters
    def get_lower(self):
        return self.lower

    def get_upper(self):
        return self.upper

    # setters
    def set_bounds(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def set_lower(self, lower):
        self.lower = lower

    def set_upper(self, upper):
        self.upper = upper

# class for While Loop
class WhileLoop(Parent):
    def __init__(self, condition="", args=None, level=0):
        super().__init__(args, level)

        self.condition = condition

    def __str__(self):
        if len(self.args) == 0:
            return " " * 4 * self.level + "while {}:\n".format(self.condition)

        retval = " " * 4 * self.level + "while {}:\n".format(self.condition)

        for arg in self.args:
            retval += str(arg)

        return retval

# class for If object
class If(Parent):
    def __init__(self, condition="", args=None, level=0):
        super().__init__(args, level)

        self.condition = condition

    def __str__(self):
        if len(self.condition) == 0:
            return " " * 4 * self.level + "if\n"

        if len(self.args) == 0:
            return " " * 4 * self.level + "if {}:\n".format(self.condition)

        ret = " " * 4 * self.level + "if {}:\n".format(self.condition)

        for arg in self.args:
            ret += str(arg)

        return ret

class Elif(If):
    def __init__(self, condition="", args=None, level=0):
        super().__init__(condition, args, level)

    def __str__(self):
        if len(self.condition) == 0:
            return " " * 4 * self.level + "elif\n"

        if len(self.args) == 0:
            return " " * 4 * self.level + "elif {}:\n".format(self.condition)

        ret = " " * 4 * self.level + "elif {}:\n".format(self.condition)

        for arg in self.args:
            ret += str(arg)

        return ret

class Else(Parent):
    def __init__(self, args=None, level=0):
        super().__init__(args, level)

    def __str__(self):
        if len(self.args) == 0:
            return " " * 4 * self.level + "else:\n"

        ret = " " * 4 * self.level + "else:\n"

        for arg in self.args:
            ret += str(arg)

        return ret

class Function(Parent):
    def __init__(self, name="function", params=None, args=None, level=0):
        super().__init__(args, level)

        if params is None:
            self.params = []
        else:
            self.params = params

        self.name = name

        if not isinstance(self.params, list):
            self.params = [self.params]

    def __str__(self):
        if len(self.args) == 0:
            return " " * 4 * self.level + "def {}({}):\n".format(self.name, ", ".join(self.params))

        ret = " " * 4 * self.level + "def {}({}):\n".format(self.name, ", ".join(self.params))

        for arg in self.args:
            ret += str(arg)

        return ret

    def get_name(self):
        return self.name

class Class(Parent):
    def __init__(self, name="Class", parent_class=None, args=None, level=0):
        super().__init__(args, level)

        self.name = name
        self.parent_class = parent_class

    def __str__(self):
        parent_name = self.parent_class.get_name() if self.parent_class is not None else ""

        if len(self.args) == 0:
            return " " * 4 * self.level + "class {}({}):\n".format(
                self.name, parent_name)

        ret = " " * 4 * self.level + "class {}({}):\n".format(self.name, parent_name)

        for arg in self.args:
            ret += str(arg)

        return ret

    def get_name(self):
        return self.name

# Generic class in case we want to put some raw strings inside the code without needing to go
# through the hassle of creating an object
class Generic(Parent):
    def __init__(self, args=None, level=0):
        if args is None:
            self.args = []
        else:
            self.args = args

        self.level = level

        if not isinstance(self.args, list):
            self.args = [self.args]

    def __str__(self):
        return self.args[0]

    def set_level(self, level):
        self.level = level

class Return(Parent):
    def __init__(self, args=None, level=0):
        if args is None:
            self.args = []
        else:
            self.args = args

        self.level = level

        if not isinstance(self.args, list):
            self.args = [self.args]

    def __str__(self):
        if len(self.args) == 0:
            return " " * 4 * self.level + "return\n"
            
        return " " * 4 * self.level + "return {}\n".format(self.args[0])

    def set_level(self, level):
        self.level = level

# testing
if __name__ == "__main__":
    from parser import *

    root = Parent()
    current = root

    current = parse_input("print \"apple and the world\"", current)
    current = parse_input("if i is greater than 1", current)
    current = parse_input("print hello", current)
    current = parse_input("else if i is less than 1", current)
    print(root)
    current = parse_input("z", current)
    print("current")
    print(current)
    print("root")
    print(root)