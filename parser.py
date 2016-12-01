import re
from power import *

def extract_quotes(s):
    retval = s
    quotes = []
    
    count = 0
    idx1 = idx2 = -1
    for i in range(len(s)):
        if s[i] == "`" and s[i-1] != "\\":
            if idx1 == -1:
                idx1 = i + 1
            else:
                idx2 = i
                quote = s[idx1:idx2]
                retval = retval.replace("`" + quote + "`", "'variable" + str(count) + "'")
                quotes.append(quote)
                count += 1
                idx1 = -1
                
    return retval, quotes

def is_in_quotes(s):
    return (s[0] == "'" and s[-1] == "'") or (s[0] == "\"" and s[-1] == "\"")

def parse_print(inp):
    inp, quotes = extract_quotes(inp)
    inp = inp.lower().replace('and', '').replace(',', '')
    words = re.split('\s+', inp)
    del words[0]
    
    count = 0
    for i in range(len(words)):
        if words[i][1:9] == 'variable':
            words[i] = "'{}'".format(quotes[count])
            count += 1
    
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
def parse_loop(inp):
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

    new_obj = Loop(lower=start, upper=end, var=var)
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

    return Generic(args="{} = {}".format(var, expression))

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
    return Generic(args=inp)

def parse_input(inp, current):
    if len(inp) == 0:
        current.add_arg(Generic(""))
        return current

    words = inp.split(" ")

    command = words[0].lower()

    if command == "print":
        current.add_arg(parse_print(inp))
    elif command == "if":
        current.add_arg(parse_if(inp))
        current = current.get_args()[-1]
    elif command == "end":
        if current.get_parent() is not None:
            current = current.get_parent()
            current.add_arg(Generic(""))

    elif command == "else":
        if words[1].lower() == "if" and (isinstance(current, If) or isinstance(current, Elif)):
            current = current.get_parent()
            current.add_arg(parse_elif(inp))
            current = current.get_args()[-1]
        elif words[1] != "if" and (isinstance(current, If) or isinstance(current, Elif)):
            current = current.get_parent()
            current.add_arg(parse_else(inp))
            current = current.get_args()[-1]
    elif command == "do" or command == "for" or command == "iterate":
        current.add_arg(parse_loop(inp))
        current = current.get_args()[-1]
    elif command == "undo":
        if current.get_parent() is None:
            pass

        if len(current.get_args()) == 0:
            current = current.get_parent()
            current.remove_arg()
        else:
            current.remove_arg()
    elif command == "set" or command == "assign" or words[1] == "=":
        current.add_arg(parse_set(inp))

    elif command == "define" or command == "def" or command == "function":
        print('lol')
        current.add_arg(parse_function(inp))
        current = current.get_args()[-1]

    elif command == "create":
        if bool(re.search(re.compile('function'), inp)):
            current.add_arg(parse_function(inp))
            current = current.get_args()[-1]

    elif command == "return":
        tmp = current
        while tmp != None and not isinstance(tmp, Function):
            tmp = tmp.get_parent()

        if bool(tmp):
            current.add_arg(parse_return(inp))
            current = current.get_parent()

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