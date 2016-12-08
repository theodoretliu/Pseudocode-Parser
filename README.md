#PSEUDOCODE PARSER
Nenya Edjah and Theodore Liu

DEPLOYMENT
A live, working website can be found at https://radiant-lowlands-50868.herokuapp.com. Please give about thirty seconds for the website to first load up. After thirty minutes, Heroku hibernates "free" dynos, and the extra time is to wake the dyno from hibernation. 

The full source code can be found at https://github.com/theodoretliu/Pseudocode-Parser.

If you would like to run the app locally, cd into the correct folder and execute the following commands

pip install -r requirements.txt  
export FLASK_APP=application.py  
export FLASK_DEBUG=1  
flask run  

Then go to your web browser and go to localhost:5000 or 127.0.0.1:5000. If using the CS50 IDE, you can navigate to CS50 IDE > Web Server in the top left corner of the page.

#OVERVIEW
The overall structure of the website is simple. On the homepage, there is a single line input form where the user can enter lines of pseudocode one-by-one. After each line of pseudocode is entered, the user can press "Submit" on the right or press the ENTER key on the keyboard. If the pseudocode can be parsed correctly, it will be displayed in the textarea below with proper Python syntax highlighting. Indentation and styling will be handled automatically. Hypothetically, the parser should be able to handle any pseudocode (within reason). If the pseudocode cannot be parsed correctly, the user will be notified via an error message at the bottom of the screen and prompted to try again. Consult the SUPPORTED SYNTAX if presented with problems. The code in the textarea may not be edited by the user although the user may copy the code from the editor.

Previous entries into the parser can be accessed using the up and down arrow keys (like in bash).

On the top of the website, the user can find "Home", "About", "Contact", and "Help". The "Home" page is the page with the actual pseudocode parser. The "About" page contains information about our goals and customer support. The "Contact" page simply has an email at which we can be contacted. The "Help" page contains supported syntax and examples, much like the contents of this very document.

#FULL DEMONSTRATION
The following can be inputted line by line to create the classic "fizzbuzz" function

create a function called fizzbuzz with parameter n  
if n % 15 is equal to 0  
print "fizzbuzz"  
else if n % 3 is equal to 0  
print "fizz"  
otherwise if n % 5 equals 0  
print "buzz"  
print "buzz"   <- a mistake  
z 			   <- undo  
end            <- close else block  
end            <- close function  

for i in range 20  
call fizzbuzz with parameter i  
end  

#IMPORTANT COMMANDS
##Undo
To undo an inserted piece of Python code, the user must simply type "undo" or "z" into the submission form. If the user would like to undo multiple insertions, they can type "zz...zz" where the number of "z" is the desired number of undos.

##Insert blank line
To insert a blank line, the user must simply hit enter with a blank submission form.

##Exit current code structure
If the user would like to exit a code structure, e.g. if block, for block, function block, they can type "end" and submit, which will bring the user out of the current code structure. This command can also be undone.

##Clear everything
Simply refresh the page with Ctrl-R or Cmd-R (Mac).

#SUPPORTED SYNTAX
##Print
###Ex: print "hello", variable, and x + y

Strings must be surrounded by double quotes and any special characters, e.g. "\\", "\"", "\'", must be escaped properly by the user. Variable names must be typed without double quotes. Any math expressions can be typed without quotes.

##Assign variables
###Ex: set x to y
###Ex: x = 4

The user may assign variables to each other using either the "set" keyword or by directly typing the assignment using the "=" sign. The parser will not check for valid Python syntax; for example, the parser will allow the assignment "set 9 to x", generating the code 9 = x

##If, Elif
###Ex: if i is greater than 1
###Ex: else if i does not equal 1

If and else if statements may be typed verbatim, e.g. "greater than", or with "real" comparison operators like >, <, ==, etc. The general form is "if *conditional*". The conditional may be compound with "or" and "and" and can also include parentheses. All numbers must be typed using digits; there is currently no support for "one". In addition to else, the user may also type "otherwise if" which is equivalent to "else if". 

The parser WILL check that Elif statements are inserted with a matching If statement. Otherwise, the parser will not insert the Elif. The parser is not responsible for variable names. If the variable "i" has not been initialized, the parser will still naively insert the if condition.

##Else
###Ex: else

Else must go on its own line of pseudocode. "Otherwise" is also supported. The parser will check to ensure that the Else is paired with an If or Elif statement.

##For Loops
###Ex: for i in range 0 to 10
###Ex: do from 0 to 4
###Ex: for i in range 4-10

For loops can be instantiated with the "for", "do", and "iterate" keywords. The iterating variable may optionally be specified, and the upper bound must be specified, although the lower bound is optional. Currently, only for loops over ranges are allowed; "for-each" loops are not supported.

##While Loops
###Ex: while i is not equal to 1

While loops are constructed in the same way as if statements. Incur them with the "while" keyword followed by the conditional statement. Again, the conditional may include "or" or "and" and parentheses and may be typed verbatim, e.g. "greater than", or with actual comparison operators, e.g. "<" or ">".

##Function Creation
###Ex: create a function called fizzbuzz with parameter n

Functions can be created using the words "create", "make", and "define". The name of the function must come after the keywords "called" or "named". The parameters of the function can be specified after keywords "parameter(s)", "argument(s)", or "arg(s)". The s's are optional. If the function does not take any parameters, the clause "with parameters ..." is optional. 

##Return
###Ex: return "hello"
###Ex: return x + y

Almost anything can be returned at any point. The parser WILL check to ensure that the return exists within a function before inputting it into the Python code. After the return, the parser will automatically exit the current code structure - if block, for block, etc. - though not necessarily the function (since a function can have multiple return statements).

##Call functions
###Ex: call function fizzbuzz with argument 2
###Ex: fizzbuzz(2)

Calling a function can be done with the "call" keyword or by just typing the function name with parentheses as would actually happen in Python code. The name of the function must be specified somewhere in the line of pseudocode. The arguments are optional. The parser is not responsible for checking the existence of the function or the required arguments.

##Lists
###Ex: create a list called array
###Ex: add 3 to array
###Ex: append 2, 6, 7 and 9 to array
###Ex: sort array
###Ex: remove 6 from array

Lists can be created and modified with a few simple commands. Create a list using "create" or "make". Add one or multiple elements to the list with "add" or "append". Sort a numeric list with "sort" followed by the list's name. Finally, you can remove an element from a list using "remove" or "delete" followed by the element that you want to remove and "from" the list's name.