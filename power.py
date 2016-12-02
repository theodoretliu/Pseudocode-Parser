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

class ForLoop(Parent):
    def __init__(self, lower=0, upper=10, var="i", args=None, level=0):
        super().__init__(args, level)

        self.lower = lower
        self.upper = upper
        self.var = var

    def __str__(self):
        ret = " " * 4 * self.level + "for {} in range({}, {}):\n".format(self.var, self.lower, self.upper)

        for member in self.args:
            ret += str(member)

        return ret

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
        ret = " " * 4 * level + "class {}({}):\n".format(self.name, parent_name)

        for arg in self.args:
            ret += str(arg)

        return ret

    def get_name(self):
        return self.name

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


if __name__ == "__main__":
    from parser import *

    root = Parent()
    current = root

    current = parse_input("print \"apple and the world\"", current)
    print(root)