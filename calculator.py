import copy
import builtins
from math import floor
from typing import Any


def eval(string: str, functions: dict = None, local: dict = None) -> Any:
    if functions is None:
        functions = {}
    if local is None:
        local = {}
    return builtins.eval(string, {"__builtins__": functions}, local)


def calculator(string: str) -> int | str:
    string = string.replace("^", "**")
    if "=" in string:
        result = equations(string)
        return result
    elif "con" in string.lower():
        string = string.lower()
        string = eval(string.replace("con", "").replace(")", "").replace("(", ""))
        result = str(conversion_notation(*string))
        return result
    elif "sor" in string.lower():
        string = string.lower()
        string = eval(string.replace("sor", "").replace("(", "").replace(")", ""))
        result = str(sorted(*string))
        return result
    elif string.startswith("?"):
        result = simplify(string.split("?")[1])
        return result
    else:
        from math import sqrt, factorial, sin, cos, tan, radians, pi, e, degrees, asin, acos, atan
        from sympy import acot
        functions = \
            {"sqrt": sqrt, "factorial": factorial, "round": round,
             "radians": radians, "pi": pi, "e": e, "degrees": degrees,
             "sin": lambda x: sin(radians(x)), "cos": lambda x: cos(radians(x)), "tan": lambda x: tan(radians(x)),
             "cot": lambda x: cos(radians(x)) / sin(radians(x)),
             "asin": lambda x: degrees(asin(x)), "acos": lambda x: degrees(acos(x)),
             "atan": lambda x: degrees(atan(x)), "acot": lambda x: degrees(eval(str(acot(x)), {"pi": pi})),
             "sinr": sin, "cosr": cos, "tanr": tan, "cotr": lambda x: cos(x) / sin(x),
             "asinr": asin, "acosr": acos, "atanr": atan, "acotr": lambda x: eval(str(acot(x)), {"pi": pi}),
             "tg": lambda x: tan(radians(x)), "ctg": lambda x: cos(radians(x)) / sin(radians(x)),
             "atg": lambda x: degrees(atan(x)), "actg": lambda x: degrees(eval(str(acot(x)), {"pi": pi})),
             "tgr": tan, "ctgr": lambda x: cos(x) / sin(x),
             "atgr": atan, "actgr": lambda x: eval(str(acot(x)), {"pi": pi}),
             "med": median, "dis": dispersion, "ave": average,
             "len": lambda *args: len(args), "max": lambda *args: max(*args), "min": lambda *args: min(*args),
             "abs": abs, "sum": lambda *args: sum(args), "gm": geometric_mean}
        string = string.lower()
        result = round(eval(string, functions), 5)
        if result == int(result):
            return int(result)
        return result


def round(number, ndigits=0):
    return floor(number * 10 ** ndigits + 0.5) / 10 ** ndigits


def median(*args: int | float) -> int | float:
    args = list(args)
    for arg in args:
        if type(arg) != int and type(arg) != float:
            raise Exception()
    args = sorted(args)
    if len(args) % 2 == 0:
        return (args[len(args) // 2 - 1] + args[len(args) // 2]) / 2
    else:
        return args[len(args) // 2]


def dispersion(*args: int | float) -> int | float:
    args = list(args)
    for arg in args:
        if type(arg) != int and type(arg) != float:
            raise Exception()
    ave = sum(args) / len(args)
    args = [(i - ave) ** 2 for i in args]
    return sum(args) / len(args)


def average(*args: int | float) -> int | float:
    args = list(args)
    for arg in args:
        if type(arg) != int and type(arg) != float:
            raise Exception()
    return sum(args) / len(args)


def geometric_mean(*args: int | float) -> int | float:
    args = list(args)
    for arg in args:
        if type(arg) != int and type(arg) != float:
            raise Exception()
    return eval(" * ".join([str(i) for i in args])) ** (1/len(args))


def conversion_notation(numeric: str | int, base: int, to: int):
    numeric = str(numeric)
    base = int(base)
    to = int(to)
    numeric = int(numeric, base)
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    if to > len(digits): raise Exception()
    result = ''
    while numeric > 0:
        result = digits[numeric % to] + result
        numeric //= to
    return result.upper()


def equations(text: str) -> str:
    from sympy import Eq, solve, symbols, sqrt, factorial, sin, cos, tan, cot, pi, asin, acos, atan, acot, deg, rad
    variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    syms = set()
    for char in text:
        if char in variables:
            syms.add(char)
    if len(syms) == 0: raise Exception()
    syms = [symbols(list(syms)[0])] if len(syms) == 1 else list(symbols(", ".join(syms)))
    for sym in syms:
        locals()[str(sym)] = sym
    eqs = []
    functions = {"sqrt": sqrt, "factorial": factorial, "sin": lambda x: sin(rad(x)), "cos": lambda x: cos(rad(x)),
                 "tan": lambda x: tan(rad(x)), "tg": lambda x: tan(rad(x)), "cot": lambda x: cot(rad(x)), "pi": pi,
                 "ctg": lambda x: cot(rad(x)), "asin": lambda x: deg(asin(x)), "acos": lambda x: deg(acos(x)),
                 "atan": lambda x: atan(asin(x)), "atg": lambda x: deg(atan(x)), "acot": lambda x: deg(acot(x)),
                 "actg": lambda x: deg(acot(x)), "sinr": sin, "cosr": cos, "tanr": tan, "tgr": tan, "cotr": cot,
                 "ctgr": cot, "asinr": asin, "acosr": acos, "atanr": atan, "atgr": atan, "acotr": acot, "actgr": acot}
    system_functions = ["text", "Eq", "solve", "symbols", "sqrt", "factorial", "sin", "cos", "tan", "cot", "pi", "asin",
                        "acos", "atan", "acot", "variables", "char", "sym", "syms", "eqs", "functions", "deg", "rad",
                        "system_functions"]
    local = locals()
    for i in system_functions:
        local.pop(i)
    for string in text.split("\n"):
        eqs.append(Eq(eval(string.split("=")[0], functions, local), eval(string.split("=")[1], functions, local)))
    results = solve(tuple(eqs), tuple(syms))
    if type(results) == list:
        result = [dict([(f"{syms[k]}", j) for k, j in enumerate(i)]) for i in results]
    elif type(results) == dict:
        result = [results]
    else:
        raise Exception()
    result2 = copy.copy(result)
    for i in result2:
        if "I" in str(i.values()):
            result.remove(i)
    result = str(result).replace("}", "\n").replace(", ", "\n").replace("{", "").replace(": ", " = ").\
        replace("'", "").replace("[", "").replace("]", "")
    return str(result) if str(result) != "" else "Нет действительного решения или любое"


def simplify(text):
    from sympy import symbols, simplify, sqrt, factorial, sin, cos, tan, cot, pi, asin, acos, atan, acot, rad, deg, \
        expand, factor, Abs
    variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    syms = set()
    for char in text:
        if char in variables:
            syms.add(char)
    syms = [symbols(list(syms)[0])] if len(syms) == 1 else list(symbols(", ".join(syms)))
    for sym in syms:
        locals()[str(sym)] = sym
    functions = {"sqrt": sqrt, "factorial": factorial, "sin": lambda x: sin(rad(x)), "cos": lambda x: cos(rad(x)),
                 "tan": lambda x: tan(rad(x)), "tg": lambda x: tan(rad(x)), "cot": lambda x: cot(rad(x)), "pi": pi,
                 "ctg": lambda x: cot(rad(x)), "asin": lambda x: deg(asin(x)), "acos": lambda x: deg(acos(x)),
                 "atan": lambda x: atan(asin(x)), "atg": lambda x: deg(atan(x)), "acot": lambda x: deg(acot(x)),
                 "actg": lambda x: deg(acot(x)), "sinr": sin, "cosr": cos, "tanr": tan, "tgr": tan, "cotr": cot,
                 "ctgr": cot, "asinr": asin, "acosr": acos, "atanr": atan, "atgr": atan, "acotr": acot, "actgr": acot,
                 "abs": Abs}
    system_functions = ["text", "symbols", "simplify", "sqrt", "factorial", "sin", "cos", "tan", "cot", "pi", "asin",
                        "acos", "atan", "acot", "variables", "char", "sym", "syms", "functions", "deg", "rad", "expand",
                        "system_functions", "factor", "Abs"]
    local = locals()
    for i in system_functions:
        local.pop(i)
    answers = set()
    answers.add(str(simplify(eval(text, functions, local))))
    answers.add(str(expand(eval(text, functions, local))))
    answers.add(str(factor(eval(text, functions, local))))
    answers = list(answers)
    for i in range(len(answers)):
        answers[i] = f"{i + 1}.   " + answers[i]
    answer = str(answers).replace("[", "").replace("]", "").replace(", ", "\n\n").replace("'", "")
    return answer if answer != "" else "Я не могу его решить"
