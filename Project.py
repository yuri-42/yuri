import re

# error code list
error_code = {
    1: 'invalid token: leading zeros in integer literals are not permitted',
    2: 'uninitialized variables',
    3: 'invalid expression',
    4: 'invalid operator',
    5: 'invalid assignment'
}

# a dictionary store symbol
sym = {}


def calculator(rpn):
    # calculate the reverse polish notation
    # res is a stack
    res = []
    cal = {'+': lambda a, b: a + b,
           '-': lambda a, b: a - b,
           '*': lambda a, b: a * b}

    for ch in rpn:
        try:
            # if it is a number, just push it into stack
            if isinstance(ch, int):
                res.append(ch)

            # if it is '+', '-' or '*', pop two elements on the top, calculate them, push it back
            elif ch == '+' or ch == '-' or ch == '*':
                temp1 = res.pop()
                temp2 = res.pop()
                res.append(cal[ch](temp2, temp1))

            # if it is negative sign, pop the element on the top, multiply by -1, push it back
            # the positive sign can be ignore
            elif ch == 'N':
                temp = res.pop()
                res.append(-temp)

        except IndexError:
            print(error_code[3])
            return

    # if the stack only left one element, that's the correct answer
    if len(res) == 1:
        return res[0]
    # otherwise, something wrong
    else:
        print(error_code[3])
        return


def reverse_polish_notation_generator(exp_list):
    # set the priority of operator, 'N' represents negative sign, 'P' represents positive sign
    pri = {'+': 1, '-': 1, '(': 1, '*': 2, 'N': 3, 'P': 3}
    opera = []
    rpn = []
    num = ''
    pre = ''

    # a loop that generator reverse polish notation
    for ch in exp_list:
        if ch.isnumeric():
            num += ch
        else:
            if num:
                if re.fullmatch(r'[1-9][0-9]*|0', num):
                    rpn.append(int(num))
                    num = ''
                else:
                    print(error_code[1])
                    return
            if ch == '-' and not (pre.isnumeric() and pre):
                opera.append('N')
            elif ch == '+' and not (pre.isnumeric() and pre):
                opera.append('P')
            elif ch == '(':
                opera.append(ch)
            elif ch == '+' or ch == '-' or ch == '*':
                while opera and pri[opera[len(opera) - 1]] > pri[ch]:
                    rpn.append(opera.pop())
                opera.append(ch)
            elif ch == ')':
                try:
                    while opera[len(opera) - 1] != '(':
                        rpn.append(opera.pop())
                    opera.pop()
                except IndexError:
                    print(error_code[3])
                    return
            else:
                print(error_code[4])
                return
        pre = ch

    if num:
        rpn.append(int(num))

    rpn.extend(opera[::-1])

    # calculate the reverse polish notation
    return calculator(rpn)


def exp_recognizer(exp):
    # substitute the letter in the expression into digit by using the symbol table first
    for i, e in sym.items():
        if i in exp:
            exp = exp.replace(i, str(e))

    # if the expression still contain letter after substitution, it must has uninitialized variables
    if re.findall(r'[a-zA-Z_]', exp):
        print(error_code[2])
        return

    # if after the substitution, the expression only contains digit
    elif exp.isnumeric():
        # determine if it is a valid number
        # if it is a valid digit, return the number
        if re.fullmatch(r'[1-9][0-9]*|0', exp):
            return int(exp)
        else:
            print(error_code[1])
            return

    # if after the substitution, the expression neither contain letter nor only contain digit
    # that means the expression needs to calculate the result
    # convert the expression into a character list and put it into reverse_polish_notation_generator method
    else:
        return reverse_polish_notation_generator([ch for ch in exp])


if __name__ == '__main__':
    # a pattern to match the statement
    pa = re.compile(r'[A-Za-z_][\w]* = (.*?);')
    with open("input.txt") as f:
        for stmt in f:
            stmt = stmt.strip()

            # decide whether a statement has a valid identifier and the semicolon
            # but not decide whether it has a valid expression yet
            if re.fullmatch(pa, stmt):

                # separate out the identifier and the expression
                identifier, expression = re.findall(r'(.*?) = (.*?);', stmt)[0]

                # put the expression into exp_recognizer method to decide whether it is a valid expression
                expression = exp_recognizer(expression)

                # if the return value is an integer, put identifier and expression into symbol table
                if isinstance(expression, int):
                    sym[identifier] = expression

                # otherwise, something wrong, stop the loop
                else:
                    sym.clear()
                    break
            else:
                print(error_code[5])
                sym.clear()
                break

    # output the symbol table
    for identifier, expression in sym.items():
        print(identifier, '=', expression)
