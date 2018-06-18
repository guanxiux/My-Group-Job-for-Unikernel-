import sys
import string
#suppose the environment is Linux
#let sys.argv formation be like " 'Directory Path' 'File Name'"
# print(sys.argv)

filename = str(sys.argv[1]) + '/' +str(sys.argv[2])

#debug in pycharm
# filename = str(sys.argv[0])
f = open(filename, 'r')
if f:
    origin_content = f.read()
    f.close()
else:
    print("Failed to open " + filename)
    exit(1)

C_return_value_type = ['int',  'long', 'double', 'char', 'struct', 'void']
length = len(origin_content)
commented = [0]*length

def Commented(target_string):
    # // /*
    comment_index_begin = FindNearestElement(target_string, 0, length, '/', 0)
    comment_index_end = comment_index_begin
    while comment_index_begin >= 0:
        comment_end = False
        if target_string[comment_index_begin + 1] == '/':
            comment_end = True
            comment_index_end = FindNearestElement(target_string, comment_index_begin, length, '\n', 0)
        elif target_string[comment_index_begin + 1] == '*':
            comment_index_end = comment_index_begin + 2
            while comment_end == False:
                comment_index_end = FindNearestElement(target_string, comment_index_end, length, '*', 0)
                if comment_index_end < 0 :
                    comment_end = True
                    comment_index_end = length
                elif target_string[comment_index_end + 1] == '/':
                    comment_end = True
                    comment_index_end += 1
                else:
                    comment_index_end += 1
        if comment_end :
            commented[comment_index_begin : comment_index_end] = [1] * (comment_index_end - comment_index_begin + 1)
        if comment_index_begin < comment_index_end:
            comment_index_begin = comment_index_end + 1
        else:
            comment_index_begin += 1
        comment_index_begin = FindNearestElement(target_string, comment_index_begin, length, '/', 0)
    # ""
    comment_index_begin = FindNearestElement(target_string, 0, length, '\"', 0)
    comment_index_end = comment_index_begin
    while comment_index_begin >= 0:
        comment_index_end = FindNearestElement(target_string, comment_index_begin + 1, length, '\"', 0)
        if comment_index_end < 0 :
            comment_index_end = length
        commented[comment_index_begin : comment_index_end] = [1] * (comment_index_end - comment_index_begin)
        comment_index_begin = FindNearestElement(target_string, comment_index_end + 1, length, '\"', 0)

        
def LetterNumAnd_(c):
    a = ord(c)
    if 65 <= a <= 90 or 97 <= a <= 122 or 48 <= a <= 57 or a == 95:
        return 1
    else:
        return 0

#target_type: -2 find letters, numbers or _; -1 find all ASCII codes except those selected by -2;
#  other value between 0 and 127 find the ASCII code it represents.
def FindNearestElement(target_string, target_index_beg, target_index_end, target_type, forward_or_backward):
    if isinstance(target_type, str):
        target = ord(target_type)
    else:
        target = target_type
    if forward_or_backward == 1:
        range_list = reversed(range(target_index_beg, target_index_end))
    else:
        range_list = range(target_index_beg, target_index_end)
    for i in range_list:
        if target < 0:
            if target == -2 and LetterNumAnd_(target_string[i]) == 1  and commented[i] == 0:
                return i
            elif target == -1 and LetterNumAnd_(target_string[i]) == 0 and commented[i] == 0:
                return i
        elif 0 <= target <= 127:
            if target_string[i] == target_type and commented[i] == 0:
                return i
        else:
            print("Target type error.")
            exit(1)
    return -1

def SkipBracketPair(target_string, target_index, bracket):
    bracket_pairs = 0
    if bracket == '(':
        paired_bracket = ')'
    elif bracket == '{':
        paired_bracket = '}'
    for i in range(target_index, len(target_string)):
        if target_string[i] == bracket and commented[i] == 0:
            bracket_pairs += 1
        elif target_string[i] == paired_bracket and commented[i] == 0:
            bracket_pairs -= 1
        if bracket_pairs == 0:
            return i
    return -1

def ProcessFunctionDef(function):
    return function

first_index = 0
next_index = 0
function_def_beg = 0
function_def_end = 0
found_type_def = False
found_parameter_list = False
found_function = False 

read_end = False

f = open(filename, 'w')
if f:
    print("Open and re-organize "+filename)
else:
    print("Fail to open and re-organize " + filename)

Commented(origin_content)

for i in range(0, len(origin_content)):
    if found_parameter_list == False:
        next_index = FindNearestElement(origin_content, first_index, length, '(', 0)
        found_parameter_list = True
        found_function = False
    else:
        found_parameter_list = False
        next_index = SkipBracketPair(origin_content, first_index, '(')
        temp = FindNearestElement(origin_content, next_index, length, '{', 0)
        if FindNearestElement(origin_content, next_index, temp, -2, 0) < 0:
            t1 = first_index
            while 1:
                t2 = FindNearestElement(origin_content, 0, t1, -2, 1)
                t1 = FindNearestElement(origin_content, 0, t2, -1, 1)
                if origin_content[t1 + 1 : t2 + 1] in C_return_value_type:
                    function_def_beg = t1 + 1
                    function_def_end = next_index + 1
                    function_definition = origin_content[function_def_beg : function_def_end]
                    found_function = True
                    next_index = temp + 1
                    break
        else: 
            found_function = False
            found_parameter_list = False
    if next_index < 0:
        next_index = length
        read_end = True
    content_to_write = origin_content[first_index : next_index]
    f.write(content_to_write)
    first_index = next_index
    if found_function == True:
        f.write("\n\tprintf(\"" + function_definition + "\")")
        next_index = SkipBracketPair(origin_content, temp, '{')
        content_to_write = origin_content[first_index : next_index]
        f.write(content_to_write)
        first_index = next_index
        found_parameter_list = False
        found_function = False
    if read_end:
        break

f.close()

