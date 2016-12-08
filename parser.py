import re
from power import *

# check if a string is surrounded by quotes
def is_in_quotes(s):
    return (s[0] == "'" and s[-1] == "'") or (s[0] == "\"" and s[-1] == "\"")

# check that a string has correctly paired parentheses
def balanced_delimiters(s):
    def inv(s):
        if s == '{': return '}'
        elif s == '(': return '}'
        elif s == '[': return ']'
        elif s == '}': return '{'
        elif s == ')': return '('
        elif s == ']': return '['
        
    def opener(s):
        if s == '{' or s == '[' or s == '(':
            return True
        return False

    def closer(s):
        return not opener(s)

    level = 0
    openers = {}
    keys = set(('{', '[', '(', ')', ']', '}'))
    for i in range(len(s)):
        if s[i] not in keys: continue;
        if opener(s[i]):
            if level in openers:
                openers[level].append(s[i])
            else:
                openers[level] = [s[i]]
            level += 1
        if closer(s[i]):
            level -= 1
            if level not in openers: return False
            if openers[level].pop(-1) != inv(s[i]):
                return False
    for i in openers:
        if len(openers[i]) != 0:
            return False
    return True

# remove parentheses from a string but store them as we go
def extract_parenthesis(s):
    retval = s
    parens = []

    count = 0
    idx1 = idx2 = -1
    for i in range(len(s)):
        if s[i] == "(":
            if idx1 == -1:
                idx1 = i
        elif s[i] == ')' and balanced_delimiters(s[:i + 1]):
            idx2 = i
            paren = s[idx1 + 1:idx2]
            retval = retval.replace('(' + paren + ')', 'paren' + str(count), 1)
            parens.append(paren)
            count = 1
            idx1 = -1
    return retval, parens

def extract_groups(s):
    retval = s
    groups = []

    reg = re.compile("(\s|\(|\[)[a-zA-Z0-9_\.\(\)\[\]\s]+((\+|\-|\*|\*{2}|\/|\%|!=|==|>|>=|<|<=|\^|\&|\~|\|)[a-zA-Z0-9_\.\(\)\[\]\s]+)+")
    count = 0
    search = reg.search(retval)
    while bool(search):
        group = search.group()[1:]
        retval = retval.replace(group, 'expressiongroup' + str(count), 1)
        groups.append(group)
        count += 1
        search = reg.search(retval)

    return retval, groups

# remove stuff from quotations to allow for print to uniformly parse input
def extract_quotes(s):
    retval = s
    quotes = []
    
    count = 0
    idx1 = idx2 = -1
    for i in range(len(s)):
        if s[i] == "\"" and s[i-1] != "\\":
            if idx1 == -1:
                idx1 = i + 1
            else:
                idx2 = i
                quote = s[idx1:idx2]
                retval = retval.replace("\"" + quote + "\"", "'variable" + str(count) + "'")
                quotes.append(quote)
                count += 1
                idx1 = -1
                
    return retval, quotes

# helper function that parses print statements
def parse_print(inp):
    if inp[5] == '(':
        inp = inp[:5] + " " + inp[5:]
        if inp[-1] == ')':
            inp = inp[:6] + inp[7:-1]

    inp, quotes = extract_quotes(inp)
    inp, parens = extract_parenthesis(inp)
    inp, groups = extract_groups(inp)

    inp = inp.lower().replace('and', '').replace(',', ' ')
    words = re.split('\s+', inp)
    del words[0]

    quote_count = 0
    paren_count = 0
    group_count = 0
    for i in range(len(words)):
        quote_reg = re.compile("variable(\d+)")
        paren_reg = re.compile("paren(\d+)")
        group_reg = re.compile("expressiongroup(\d+)")

        for sample in range(3):
            test_quote = quote_reg.search(words[i])
            while bool(test_quote):
                quote = test_quote.group()
                words[i] = words[i].replace(quote, quotes[int(quote[8:])], 1)
                quote_count +=1
                test_quote = quote_reg.search(words[i])

            test_paren = paren_reg.search(words[i])
            while bool(test_paren):
                paren = test_paren.group()
                words[i] = words[i].replace(paren, '({})'.format(parens[int(paren[5:])]), 1)
                paren_count +=1
                test_paren = paren_reg.search(words[i])

            test_group = group_reg.search(words[i])
            while bool(test_group):
                group = test_group.group()
                words[i] = words[i].replace(group, groups[int(group[15:])], 1)
                quote_count +=1
                test_group = group_reg.search(words[i])

        if is_in_quotes(words[i]): words[i] = '"{}"'.format(words[i][1:-1])

    new_obj = Print(args=words)
    return new_obj

def parse_list(inp, current):
    inp = re.sub('named|called', 'named', inp, flags=re.IGNORECASE)
    inp = re.sub('array|list', 'list', inp, flags=re.IGNORECASE)
    words = re.split('\s+', inp)
    list_name = "new_list"

    del words[0]
    if 'named' in words:
        try:
            list_name = words[words.index('named') + 1]
        except:
            pass
    else:
        try:
            list_name = words[words.index('list') + 1]
        except:
            pass

    return Generic(args="{}{} = []\n".format(' ' * 4 * (current.level + 1), list_name))

def parse_list_function(inp, key, current):
    if key == "append":
        inp = re.sub('to', 'to', inp, flags=re.IGNORECASE)
        inp = re.sub(',', ' ', inp)
        inp = re.sub('and', ' ', inp, flags=re.IGNORECASE)
        words = re.split('\s+', inp)
        del words[0]
        if 'to' not in words:
            raise Exception
        to = len(words) - list(reversed(words)).index('to') - 1
        try:
            list_name = words[to + 1]
            del words[to]
            words.remove(list_name)
            if len(words) == 1:
                return Generic("{}{}.append({})\n".format(' ' * 4 * (current.level + 1), list_name, words[0]))
            elif len(words) > 1:
                return Generic("{}{}.extend([{}])\n".format(' ' * 4 * (current.level + 1), list_name, ", ".join(words)))
        except:
            raise Exception

    elif key == "sort":
        words = re.split('\s+', inp)
        if len(words) != 2:
            raise Exception
        else:
            return Generic("{}{}.sort()\n".format(' ' * 4 * (current.level + 1), words[1]))
    elif key == "remove":
        inp = re.sub('from', 'from', inp, flags=re.IGNORECASE)
        words = re.split('\s+', inp)
        if len(words) != 4 or 'from' not in words:
            raise Exception
        else:
            list_name = words[3]
            obj_to_delete = words[1]
            return Generic("{}{}.remove({})\n".format(' ' * 4 * (current.level + 1), list_name, obj_to_delete))

# if i > 1 then 
# helper function that parses if statements correctly
def parse_if(inp):
    modulo = re.search('is( not)? divisible( by)?(\s+[a-zA-Z0-9]+)', inp, flags=re.IGNORECASE)
    if modulo:
        op = "="
        if modulo.group(1) == " not":
            op = "!"
        inp = inp.replace(modulo.group(0), '% {} {}= 0'.format(modulo.group(3), op), 1)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(>|greater than)', '<=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(<|less than)', '>=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)( equal to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('(does not|doesn(\')?t) equal( to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('not equal(s)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('if', 'if', inp, flags=re.IGNORECASE)
    inp = re.sub('then', 'then', inp, flags=re.IGNORECASE)
    inp = re.sub('true', 'True', inp, flags=re.IGNORECASE)
    inp = re.sub('false', 'False', inp, flags=re.IGNORECASE)

    # ASSUMING THE USER WONT USE SUBSTRINGS OR SLICES
    inp = re.sub(':', 'then', inp, flags=re.IGNORECASE)

    if inp[0:2].lower() != 'if':
        reverse_mode = True
    else:
        reverse_mode = False

    if reverse_mode:
        return do_some_shit()

    else:
        if 'then' in inp:
            cond, args = inp.split('then')
        else:
            cond = inp
            args = []
        cond = re.sub('(is )?less than or equal to', '<=', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?greater than or equal to', '>=', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?less than', '<', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?greater than', '>', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?equal to', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('equal(s)?', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('is', '==', cond, flags=re.IGNORECASE)
        conditions = re.split('\s+', cond)
        conditions.remove('if')
        
        new_obj = If(condition=' '.join(conditions).rstrip())

        if len(args) != 0:
            new_obj.add_arg(parse_input(args))
            
        return new_obj

# helper function that parses else ifs
def parse_elif(inp):
    modulo = re.search('is( not)? divisible( by)?(\s+[a-zA-Z0-9]+)', inp, flags=re.IGNORECASE)
    if modulo:
        op = "="
        if modulo.group(1) == " not":
            op = "!"
        inp = inp.replace(modulo.group(0), '% {} {}= 0'.format(modulo.group(3), op), 1)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(>|greater than)', '<=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(<|less than)', '>=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)( equal to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('(does not|doesn(\')?t) equal( to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('not equal(s)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('if', 'if', inp, flags=re.IGNORECASE)
    inp = re.sub('then', 'then', inp, flags=re.IGNORECASE)
    inp = re.sub('true', 'True', inp, flags=re.IGNORECASE)
    inp = re.sub('false', 'False', inp, flags=re.IGNORECASE)
    inp = re.sub('else|otherwise', "", inp, flags=re.IGNORECASE).strip()

    # ASSUMING THE USER WONT USE SUBSTRINGS OR SLICES
    inp = re.sub(':', 'then', inp, flags=re.IGNORECASE)

    if inp[0:2].lower() != 'if':
        reverse_mode = True
    else:
        reverse_mode = False

    if reverse_mode:
        return #do_some_shit()

    else:
        if 'then' in inp:
            cond, args = inp.split('then')
        else:
            cond = inp
            args = []
        cond = re.sub('(is )?less than or equal to', '<=', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?greater than or equal to', '>=', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?less than', '<', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?greater than', '>', cond, flags=re.IGNORECASE)
        cond = re.sub('(is )?equal to', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('equal(s)?', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('is', '==', cond, flags=re.IGNORECASE)
        conditions = re.split('\s+', cond)
        conditions.remove('if')
        
        new_obj = Elif(condition=' '.join(conditions).rstrip())
        if len(args) != 0: 
            new_obj.add_arg(parse_input(args))
        return new_obj

# simply parses else statements
def parse_else(inp):
    words = re.split('\s+', inp)

    if len(words) == 1:
        return Else()
        
    arg = parse_input(' '.join(words[1:]))
    new_obj = Else(args=arg)
    return new_obj 



# iterate from 1 to 5
# for i from 1 to 5
# do from 1 to 5
# helper function that parses for loops
def parse_for_loop(inp):
    num_search = re.search('(\d+)\s*\-\s*(\d+)', inp)
    if num_search:
        inp = inp.replace(num_search.group(0), num_search.group(1) + " to " + num_search.group(2))

    inp = inp.lower().replace('(', ' ').replace(')', '')

    words = re.split('\s+', inp)
    del words[0]

    start = 0
    end = 0

    var = "i"
    if words[0].lower() == 'to':
        end = words[1]
    elif words[0] != "from":
        var = words[0]
        del words[0]

    if "range" in words:
        try:
            tmp = start = words[words.index('range') + 1]
            end = words[words.index('range') + 3]
        except:
            if tmp:
                end = start
                start = 0
    elif words[0].lower() != 'to':
        try:
            start = words[1]
            end = words[3]
        except:
            pass

    new_obj = ForLoop(lower=start, upper=end, var=var)
    return new_obj

# set x equal to apple * sin(banana)
# x = 0 + 
# assign apple to x
# helper function that parses "set" keyword
def parse_set(inp, current):
    inp = re.sub('equal to|equal|to', '=', inp, flags=re.IGNORECASE)
    inp = re.sub('set', 'set', inp, flags=re.IGNORECASE)
    inp = re.sub('assign', 'assign', inp, flags=re.IGNORECASE)
    inp = re.sub('the value of|the value', ' ', inp, flags=re.IGNORECASE)
    words = re.split('\s+', inp)
    if 'set' in words:
        words.remove('set')
        var = words[0]
        expression = ' '.join(words[2:])
    elif 'assign' in words:
        words.remove('assign')
        var = words[-1]
        expression = ' '.join(words[:-2])
    else:
        var = words[0]
        expression = ' '.join(words[2:])

    return Generic(args=" " * 4 * (current.get_level() + 1) + "{} = {}\n".format(var, expression))

# create/define a function called/named name with parameters a, b, c, and d
# helper function that correctly parses the creation of functions from pseudocode
def parse_function(inp):
    inp = re.sub('named|called', 'named', inp, flags=re.IGNORECASE)
    inp = re.sub('parameter(s)?|param(s)?|argument(s)?|arg(s)?', 'arg', inp, flags=re.IGNORECASE)
    inp = re.sub('and', '', inp, flags=re.IGNORECASE)
    inp = inp.replace(',', ' ')

    func_name = "function"
    if bool(re.search('(create|def(ine)?|make)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)', inp, flags=re.IGNORECASE)):
        inp = inp.replace('(', ' ').replace(')', ' ')
        words = re.split('\s+', inp)
        func_name = words[1]
        params = [x for x in words[2:] if len(x) != 0]

    else:
        paren_test = re.search('([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)', inp)
        if bool(paren_test):
            func_name = paren_test.group(1)
            params = re.split('\s+', paren_test.group(2))

        else: 
            words = re.split('\s+', inp)
            try:
                func_name = words[words.index('named') + 1]
            except:
                try:
                    func_name = words[words.index('function') + 1]
                except:
                    pass
            try:
                params = words[words.index('arg') + 1:]
            except:
                params = []

    return Function(name=func_name, params=params)

# helper function that parses return pseudocode
def parse_return(inp):
    words = inp.split(" ")

    if len(words) == 1:
        return Return()

    retval = ""
    for word in words[1:]:
        if word != "":
            retval += word + " "

    return Return(args=retval)

# helper function that parses function calls correctly
def parse_call(inp, current):
    words = re.split("\s+", inp)

    indices = [-1] * 2
    keywords = ["function", "method"]

    for i in range(2):
        try:
            indices[i] = words.index(keywords[i])
        except Exception:
            pass

    keyword_index = max(indices)
    if keyword_index == -1:
        function_name = words[1]
    else:
        function_name = words[keyword_index + 1]

    parameter_keywords = ["parameters", "parameter", "arguments", "argument", "arg", "args", "param", "params"]

    indices = [-1] * len(parameter_keywords)

    for i in range(len(parameter_keywords)):
        try:
            indices[i] = inp.index(parameter_keywords[i])
        except Exception:
            pass

    parameter_index = max(indices)

    if parameter_index == -1:
        parameters = []
    else:
        temp = inp[parameter_index:].replace(",", "").split(" ")
        parameters = [word for word in temp[1:] if word != "and"]

    retval = " " * 4 * (current.level + 1) + "{}({})\n".format(function_name, ", ".join(parameters))

    return Generic(args=retval)

# helper function that correctly parses while loops (very similar to if statements)
def parse_while(inp):
    modulo = re.search('is( not)? divisible( by)?(\s+[a-zA-Z0-9]+)', inp, flags=re.IGNORECASE)
    if modulo:
        op = "="
        if modulo.group(1) == " not":
            op = "!"
        inp = inp.replace(modulo.group(0), '% {} {}= 0'.format(modulo.group(3), op), 1)
    inp = re.sub('while', '', inp, 1, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(>|greater than)', '<=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)(\s+)?(<|less than)', '>=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is not|isn(\')?t)( equal to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('(does not|doesn(\')?t) equal( to)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('not equal(s)?', '!=', inp, flags=re.IGNORECASE)
    inp = re.sub('if', 'if', inp, flags=re.IGNORECASE)
    inp = re.sub('then', 'then', inp, flags=re.IGNORECASE)
    inp = re.sub('true', 'True', inp, flags=re.IGNORECASE)
    inp = re.sub('false', 'False', inp, flags=re.IGNORECASE)
    inp = re.sub('else', "", inp, flags=re.IGNORECASE).strip()
    inp = re.sub('(is )?less than or equal to', '<=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is )?greater than or equal to', '>=', inp, flags=re.IGNORECASE)
    inp = re.sub('(is )?less than', '<', inp, flags=re.IGNORECASE)
    inp = re.sub('(is )?greater than', '>', inp, flags=re.IGNORECASE)
    inp = re.sub('(is )?equal to', '==', inp, flags=re.IGNORECASE)
    inp = re.sub('equal(s)?', '==', inp, flags=re.IGNORECASE)
    inp = re.sub('is', '==', inp, flags=re.IGNORECASE)
    conditions = re.split('\s+', inp)

    return WhileLoop(condition=' '.join(conditions).rstrip())

# function that undos the last argument
def undo(current):
    # if the current thing has no arguments
    if len(current.get_args()) == 0:
        # if its not the root object
        if current.get_parent() is not None:
            # if its an else if object or else object
            if isinstance(current, Elif) or isinstance(current, Else):
                # go up a level and remove the last two arguments (end object and else if object)
                current = current.get_parent()
                current.remove_arg()
                current.remove_arg()

                # go down a level to the last child
                current = current.get_args()[-1]
            else:
                # go up a level and remove the child
                current = current.get_parent()
                current.remove_arg()

    else:
        # check for a Generic instance
        if isinstance(current.get_args()[-1], Generic):
            if current.get_args()[-1].args[0] == "":
                current.remove_arg()
                current = current.get_args()[-1]

                if len(current.get_args()) > 0 and isinstance(current.get_args()[-1], Return):
                    current.remove_arg()
            else:
                current.remove_arg()
        else:
            current.remove_arg()

    return current

def parse_comment(inp, current):
    words = inp.split(" ")
    command = words[0].lower()
    length = len(command)

    return Generic(" " * 4 * (current.level + 1) + "#{}\n".format(inp[length:]))

# the crown jewel
def parse_input(inp, current):
    # if the length of the input is 0, the user wants a new line inserted
    if len(inp) == 0:
        current.add_arg(Generic(" " * 4 * (current.level + 1) + "\n"))
        return current

    # get rid of leading and trailing whitespace and split the input into words
    inp = inp.strip()
    words = inp.split(" ")

    # assume that the command is the first word
    command = words[0].lower()

    # tree of all the commands and their related objects
    if command[:5] == "print":
        current.add_arg(parse_print(inp))
    elif command == "add" or command == "append":
        current.add_arg(parse_list_function(inp, "append", current))
    elif command == "remove" or command == "delete":
        current.add_arg(parse_list_function(inp, "remove", current))
    elif command == "sort":
        current.add_arg(parse_list_function(inp, "sort", current))
    elif command == "if":
        current.add_arg(parse_if(inp))
        current = current.get_args()[-1]
    elif command == "while":
        current.add_arg(parse_while(inp))
        current = current.get_args()[-1]
    elif command == "end":
        if current.get_parent() is not None:
            current = current.get_parent()
            current.add_arg(Generic(""))
        else:
            raise Exception
    elif command == "else" or command == "otherwise":
        if len(words) == 1:
            if isinstance(current, If) or isinstance(current, Elif):
                current = current.get_parent()                
                current.add_arg(Generic(""))
                current.add_arg(Else())
                current = current.get_args()[-1]
            elif len(current.get_args()) >= 2 and (isinstance(current.get_args()[-2], Elif) or isinstance(current.get_args()[-2], If)):
                current.add_arg(Else())
                current = current.get_args()[-1]
            else:
                raise Exception
        elif words[1].lower() == "if":
            if isinstance(current, If) or isinstance(current, Elif):
                current = current.get_parent()
                current.add_arg(Generic(""))
                current.add_arg(parse_elif(inp))
                current = current.get_args()[-1]
            elif len(current.get_args()) >= 2 and (isinstance(current.get_args()[-2], Elif) or isinstance(current.get_args()[-2], If)):
                current.add_arg(parse_elif(inp))
                current = current.get_args()[-1]
            else:
                raise Exception
        elif words[1] != "if":
            if isinstance(current, If) or isinstance(current, Elif):
                current = current.get_parent()
                current.add_arg(Generic(""))
                current.add_arg(parse_else(inp))
                current = current.get_args()[-1]
            elif len(current.get_args()) >= 2 and (isinstance(current.get_args()[-2], Elif) or isinstance(current.get_args()[-2], If)):
                current.add_arg(parse_else(inp))
                current = current.get_args()[-1]
            else:
                raise Exception
        else:
            raise Exception
    elif command == "do" or command == "for" or command == "iterate":
        current.add_arg(parse_for_loop(inp))
        current = current.get_args()[-1]
    elif command == "undo":
        current = undo(current)
    elif command[0] == "z":
        if all(a == "z" for a in command):
            for i in range(command.count("z")):
                current = undo(current)
    elif command == "return":
        tmp = current
        while tmp != None and not isinstance(tmp, Function):
            tmp = tmp.get_parent()

        if bool(tmp):
            current.add_arg(parse_return(inp))      
            current = current.get_parent()
            current.add_arg(Generic(""))
        else:
            raise Exception

    elif command == "set" or command == "assign":
        current.add_arg(parse_set(inp, current))

    elif command == "define" or command == "def" or command == "function":
        current.add_arg(parse_function(inp))
        current = current.get_args()[-1]

    elif command == "create" or command == "make":
        if re.search('function', inp, flags=re.IGNORECASE):
            current.add_arg(parse_function(inp))
            current = current.get_args()[-1]
        elif re.search('list|array', inp, flags=re.IGNORECASE):
            current.add_arg(parse_list(inp, current))

    elif command == "call":
        current.add_arg(parse_call(inp, current))

    elif command == "comment" or command == "//" or command == "#":
        current.add_arg(parse_comment(inp, current))

    else:
        if len(words) > 1 and words[1] == "=":
            current.add_arg(parse_set(inp, current))
        elif inp.count("(") == 1 and inp.count(")") == 1:
            current.add_arg(Generic(args="{}\n".format(" " * 4 * (current.level + 1) + inp)))
        else:
            raise Exception
    return current

# just some testing
if __name__ == "__main__":
    root = Parent()
    current = root

    inp = "if i is divisible by n and i is not less than 2"
    current = parse_input(inp, current)

    inp2 = "append 2 to apple"
    current = parse_input(inp2, current)

    inp3 = "otherwise if i is not divisible by 2"
    current = parse_input(inp3, current)

    inp4 = "remove 3 from apple"
    current = parse_input(inp4, current)
    print(root)