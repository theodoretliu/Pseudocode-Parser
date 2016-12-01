class Parent():
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

    def __str__(self):
        ret = ""

        for arg in self.args:
            ret += str(arg)

        return ret

    def add_arg(self, arg):
        if isinstance(arg, str):
            self.args.append(arg)
            return

        arg.set_level(self.level + 1)
        arg.set_parent(self)
        self.args.append(arg)

    def decrement_level(self):
        if self.level == 0:
            return

        self.level -= 1
        for arg in self.args:
            arg.decrement_level()

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

    def remove_arg(self):
        self.args.pop(-1)

    def set_level(self, level):
        if level < 0:
            return

        if self.level < level:
            while self.level < level:
                self.increment_level()
        else:
            while self.level > level:
                self.decrement_level()

    def set_parent(self, parent):
        self.parent = parent

class Argument(Parent):
    def __init__(self, isString=True, args="hello world", level=-1):
        self.args = args
        self.level = -1

        self.isString = isString

    def __str__(self):
        return ("\"{}\"".format(self.args) if self.isString else str(self.args))

    def add_arg(self, arg):
        raise AttributeError("'Argument' object has no attribute 'addArg'")

    def decrement_level(self):
        return

    def get_is_string(self):
        return self.isString

    def increment_level(self):
        return

    def set_is_string(self, isString):
        self.isString = isString

    def set_level(self, level):
        return

class Print(Parent):
    def __init__(self, args=None, level=0):
        if args is None:
            self.args = []
        else:
            self.args = args

        self.level = level

        if not isinstance(self.args, list):
            self.args = [self.args]

    def __str__(self):
        ret = " " * 4 * self.level + "print("

        ret += ", ".join([str(arg) for arg in self.args])

        ret += ")\n"

        return ret

    def set_level(self, level):
        self.level = level

class Loop(Parent):
    def __init__(self, lower=0, upper=10, var="i", args=None, level=0):
        super().__init__(args, level)

        self.lower = lower
        self.upper = upper
        self.var = var

    def __str__(self):
        ret = " " * 4 * self.level + "for {} in range({}, {}):\n".format(self.var, self.lower, self.upper)

        for member in self.args:
            ret += str(member)

        return ret + "\n"

    def get_lower(self):
        return self.lower

    def get_upper(self):
        return self.upper

    def set_bounds(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def set_lower(self, lower):
        self.lower = lower

    def set_upper(self, upper):
        self.upper = upper

class If(Parent):
    def __init__(self, condition="", args=None, level=0):
        super().__init__(args, level)

        self.condition = condition

    def __str__(self):
        if len(self.condition) == 0:
            return "if\n"

        if len(self.args) == 0:
            return "if {}:\n".format(self.condition)

        ret = " " * 4 * self.level + "if {}:\n".format(self.condition)

        for arg in self.args:
            ret += str(arg)

        return ret + "\n"

class Elif(If):
    def __init__(self, condition="", args=None, level=0):
        super().__init__(condition, args, level)

    def __str__(self):
        if len(self.condition) == 0:
            return "elif\n"

        if len(self.args) == 0:
            return "elif {}:\n".format(self.condition)

        ret = " " * 4 * self.level + "elif {}:\n".format(self.condition)

        for arg in self.args:
            ret += str(arg)

        return ret + "\n"

class Else(Parent):
    def __init__(self, args=None, level=0):
        super().__init__(args, level)

    def __str__(self):
        if len(self.args) == 0:
            return "else:\n"

        ret = " " * 4 * self.level + "else:\n"

        for arg in self.args:
            ret += str(arg)

        return ret + "\n"

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

        self.ret_val = None

    def __str__(self):
        ret = " " * 4 * self.level + "def {}({}):\n".format(self.name, ", ".join(params))

        for arg in self.args:
            ret += str(arg)

        if self.ret_val is not None:
            ret += " " * 4 * (self.level + 1) + "return {}".format(self.ret_val)

        return ret

    def get_name(self):
        return self.name

    def set_ret_val(self, ret_val):
        self.ret_val = ret_val

class Class(Parent):
    def __init__(self, name="Class", parent_class=None, args=None, level=0):
        super().__init__(args, level)

        self.name = name
        self.parent_class = parent_class

    def __str__(self):
        parent_name = self.parent_class.get_name() if self.parent_class is not None else ""
        ret = " " * 4 * level + "class {}({}):\n".format(self.name, parent_name)

        for arg in self.args:
            ret += str(arg)

        return ret

    def get_name(self):
        return self.name

if __name__ == "__main__":
    from parser import *

    root = Parent()
    current = root

    current = parse_input("print apple", current)
    current = parse_input("if i > 1", current)
    current = parse_input("print hello", current)
    print(root)
    current = parse_input("undo", current)
    print(root)
    current = parse_input("print 'poop'", current)
    current = parse_input("if i < 1", current)
    print(root)
    current = parse_input("undo", current)
    print(root)
    current = parse_input("end", current)
    current = parse_input("", current)
    print(root)
    # print(Argument())
    # print(Print())
    # print(Loop())
    # print(If())

    # root = Parent()
    # current = root
    # current.addArg(If(condition="i > 10", args=Print(Argument(args="Fizz"))))
    # current = current.getArgs()[-1]
    # current.addArg(Print(Argument(args="Hello World")))
    # current.addArg("\n")
    # current = current.getParent()
    # current.addArg(Elif(condition="i < 10", args=Print(Argument(args="Buzz"))))
    # current = current.getArgs()[-1]
    # current = current.getParent()
    # current.addArg(Else(args=Print(Argument(args="FizzBuzz"))))
    # current.addArg(If(condition="x > 10", args=Print(Argument(args="Fiiiasdfiajsdifj"))))
    # print(root)
    # current.addArg("\n")
    # print(root)

    # fizz_buzz = If(condition="i > 10", args=Print(Argument(args="Fizz")))
    # fizz_buzz.addCondition("i < 10")
    # fizz_buzz.addArg(Print(Argument(args="Buzz")))
    # fizz_buzz.addArg(Print(Argument(args="FizzBuzz")))
    # print(fizz_buzz)
    # print(fizz_buzz)
    # loop = Loop(args=fizz_buzz)
    # loop.addArg(Print())
    # print(loop)
    # loop.incrementLevel()
    # print(loop)
    # print(isinstance(fizz_buzz, If))
    root = Parent()
    current = root

    a = Loop()
    root.add_arg(a)
    current = current.get_args()[-1]
    current.add_arg(Print(args='lol'))
    current = current.get_parent()

    b = Loop()
    current.add_arg(b)
    current = current.get_args()[-1]
    current.add_arg(Print(args='false'))
    print(root)