import re
from power import *

def is_in_quotes(s):
    return (s[0] == "'" and s[-1] == "'") or (s[0] == "\"" and s[-1] == "\"")

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

def is_in_quotes(s):
    return (s[0] == "'" and s[-1] == "'") or (s[0] == "\"" and s[-1] == "\"")

def parse_print(inp):
    if inp[5] == '(':
        inp = inp[:5] + " " + inp[5:]
        if inp[-1] == ')':
            inp = inp[:6] + inp[7:-1]

    inp, quotes = extract_quotes(inp)
    inp, parens = extract_parenthesis(inp)
    inp, groups = extract_groups(inp)

    inp = inp.lower().replace('and', '').replace(',', '')
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

# if i > 1 then 
def parse_if(inp):
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
        cond = re.sub('is less than', '<', cond, flags=re.IGNORECASE)
        cond = re.sub('is greater than', '>', cond, flags=re.IGNORECASE)
        cond = re.sub('is equal to', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('equals', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('is', '==', cond, flags=re.IGNORECASE)
        conditions = re.split('\s+', cond)
        conditions.remove('if')
        
        new_obj = If(condition=' '.join(conditions).rstrip())
        if len(args) != 0: 
            new_obj.add_arg(parse_input(args))
            
        return new_obj

def parse_elif(inp):
    inp = re.sub('if', 'if', inp, flags=re.IGNORECASE)
    inp = re.sub('then', 'then', inp, flags=re.IGNORECASE)
    inp = re.sub('true', 'True', inp, flags=re.IGNORECASE)
    inp = re.sub('false', 'False', inp, flags=re.IGNORECASE)
    inp = re.sub('else', "", inp, flags=re.IGNORECASE).strip()

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
        cond = re.sub('is less than', '<', cond, flags=re.IGNORECASE)
        cond = re.sub('is greater than', '>', cond, flags=re.IGNORECASE)
        cond = re.sub('is equal to', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('equals', '==', cond, flags=re.IGNORECASE)
        cond = re.sub('is', '==', cond, flags=re.IGNORECASE)
        conditions = re.split('\s+', cond)
        conditions.remove('if')
        
        new_obj = Elif(condition=' '.join(conditions).rstrip())
        if len(args) != 0: 
            new_obj.add_arg(parse_input(args))
        return new_obj

def parse_else(inp):
    words = re.split('\s+', inp)

    if len(words) == 1:
        return Else()
        
    arg = parse_input(' '.join(words[1:]))
    new_obj = Else(args=arg)
    return new_obj 

#iterate from 1 to 5
#for i from 1 to 5
#do from 1 to 5
def parse_for_loop(inp):
    inp = inp.lower().replace('(', ' ').replace(')', '')

    words = re.split('\s+', inp)
    del words[0]

    var = "i"
    if words[0] != "from":
        var = words[0]
        del words[0]

    if "range" in words:
        try:
            start = 0
            end = words[words.index("range") + 1]
        except:
            pass
    else:
        try:
            start = words[1]
            end = words[3]
        except:
            print(words[1])
            print(words[3])
            return None

    new_obj = ForLoop(lower=start, upper=end, var=var)
    return new_obj

# set x equal to apple * sin(banana)
# x = 0 + 
# assign apple to x
def parse_set(inp):
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

    return Generic(args="{} = {}\n".format(var, expression))

#create/define a function called/named name with parameters a, b, c, and d
def parse_function(inp):
    inp = re.sub('named|called', 'named', inp, flags=re.IGNORECASE)
    inp = re.sub('parameter([s]{1}?)|param([s]{1}?)|argument([s]{1}?)|arg([s]{1}?)', 'arg', inp, flags=re.IGNORECASE)
    inp = re.sub('and', '', inp, re.IGNORECASE)
    inp = inp.replace(',', '')
    words = re.split('\s+', inp)
    func_name = words[words.index('named') + 1]
    params = words[words.index('arg') + 1:]

    return Function(name=func_name, params=params)

def parse_return(inp):
    words = inp.split(" ")

    if len(words) == 1:
        return Return()

    retval = ""
    for word in words[1:]:
        if word != "":
            retval += word + " "

    return Return(args=retval)

def parse_call(inp):
    words = inp.split(" ")

    indices = [-1] * 2
    keywords = ["function", "method"]

    for i in range(2):
        try:
            indices[i] = words.index(keywords[i])
        except Exception:
            pass

    keyword_index = max(indices)
    print(keyword_index)
    if keyword_index == -1:
        function_name = words[1]
    else:
        function_name = words[keyword_index + 1]

    parameter_keywords = ["parameters", "parameter", "arguments", "argument"]

    indices = [-1] * 4

    for i in range(4):
        try:
            indices[i] = inp.index(parameter_keywords[i])
        except Exception:
            pass

    parameter_index = max(indices)

    if parameter_index == -1:
        parameters = []
    else:
        temp = inp[parameter_index:].replace(",", "").split(" ")
        print(temp)
        parameters = [word for word in temp[1:] if word != "and"]

    retval = "{}({})\n".format(function_name, ", ".join(parameters))

    return Generic(args=retval)

def parse_input(inp, current):
    if len(inp) == 0:
        current.add_arg(Generic("\n"))
        return current

    words = inp.split(" ")

    command = words[0].lower()

    if command[:5] == "print":
        current.add_arg(parse_print(inp))
    elif command == "if":
        current.add_arg(parse_if(inp))
        current = current.get_args()[-1]
    elif command == "end":
        if current.get_parent() is not None:
            current = current.get_parent()
            current.add_arg(Generic(""))
    elif command == "else" or command == "otherwise":
        if len(words) == 1:
            if isinstance(current, If) or isinstance(current, Elif):
                current = current.get_parent()                
                current.add_arg(Generic(""))
                current.add_arg(Else())
                current = current.get_args()[-1]
        elif words[1].lower() == "if" and (isinstance(current, If) or isinstance(current, Elif)):
            current = current.get_parent()
            current.add_arg(Generic(""))
            current.add_arg(parse_elif(inp))
            current = current.get_args()[-1]
        elif words[1] != "if" and (isinstance(current, If) or isinstance(current, Elif)):
            current = current.get_parent()
            current.add_arg(Generic(""))
            current.add_arg(parse_else(inp))
            current = current.get_args()[-1]
    elif command == "do" or command == "for" or command == "iterate":
        current.add_arg(parse_for_loop(inp))
        current = current.get_args()[-1]
    elif command == "undo" or command == "z":
        if len(current.get_args()) == 0:
            if current.get_parent() is not None:
                current = current.get_parent()
                current.remove_arg()

                if len(current.get_args()) != 0:
                    current = current.get_args()[-1]
        else:
            if isinstance(current.get_args()[-1], Generic):
                if current.get_args()[-1].args[0] == "":
                    current.remove_arg()
                    current = current.get_args()[-1]
                    if isinstance(current.get_args()[-1], Return):
                        current.remove_arg()
                else:
                    current.remove_arg()
            else:
                current.remove_arg()

    elif command == "return":
        tmp = current
        while tmp != None and not isinstance(tmp, Function):
            tmp = tmp.get_parent()

        if bool(tmp):
            current.add_arg(parse_return(inp))      
            current = current.get_parent()
            current.add_arg(Generic(""))

    elif command == "set" or command == "assign":
        current.add_arg(parse_set(inp))

    elif command == "define" or command == "def" or command == "function":
        current.add_arg(parse_function(inp))
        current = current.get_args()[-1]

    elif command == "create":
        if bool(re.search(re.compile('function'), inp)):
            current.add_arg(parse_function(inp))
            current = current.get_args()[-1]

    elif command == "call":
        current.add_arg(parse_call(inp))

    else:
        if len(words) > 1 and words[1] == "=":
            current.add_arg(parse_set(inp))
        elif inp.count("(") == 1 and inp.count(")"):
            current.add_arg(Generic(args="{}\n".format(inp)))

    return current


if __name__ == "__main__":
    root = Parent()
    current = root

    inp = "create a function called fizzbuzz with parameters i"
    inp2 = "if i % 15 is equal to 0"
    inp3 = "print 'fizzbuzz'"
    inp4 = "else if i % 5 is equal to 0"
    inp5 = "print 'buzz'"
    inp6 = 'else if i % 3 is equal to 0'
    inp7 = "print 'fizz'"
    inp8 = 'end'
    inp9 = 'end'
    inp10 = 'print fizzbuzz(15)'


    current = parse_input(inp, current)
    current = parse_input(inp2, current)
    current = parse_input(inp3, current)
    current = parse_input(inp4, current)
    current = parse_input(inp5, current)
    current = parse_input(inp6, current)
    current = parse_input(inp7, current)
    current = parse_input(inp8, current)
    current = parse_input(inp9, current)
    current = parse_input(inp10, current)



    print(root)