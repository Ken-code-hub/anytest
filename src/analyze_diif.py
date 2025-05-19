from sympy import diff, symbols

var_input = input("リストの要素をカンマ区切りで入力してください: ")
var_list = [item.strip() for item in var_input.split(',')]

symbol_list = [symbols(item) for item in var_list]

value_input = input("リストの値をカンマ区切りで入力してください: ")
value_list = [float(item.strip()) for item in value_input.split(',')]

user_function = input("関数を入力してください（例: x**2 + 2*x + 1）: ")
difference_input = input("差を入力してください: ")
difference_list = [float(item.strip()) for item in difference_input.split(',')]
total = 0
for symbol, difference in zip(symbol_list, difference_list):
    diff_func = diff(user_function, symbol)
    evaluated = diff_func.subs(dict(zip(symbol_list, value_list)))
    
    calc_diff = difference*evaluated**2
    total += calc_diff
    
total_diff = total**(1/2)

