from copy import deepcopy
import re


# An expression tree node
class Et:
    # Constructor to create a node
    def __init__(self, value, termianl=False):
        self.terminal = termianl
        self.value = value
        self.label = None
        self.left = None
        self.right = None


def construct_tree_from_prefix(expression):
    tree = []
    st = []
    op = "+-*/^"
    for idx, e in enumerate(expression):
        if e in op:
            et = Et(e)
            et.label = str(idx)
            st.append(et)
            tree.append(et)
        else:
            et = Et(e, True)
            et.label = str(idx)
            tree.append(et)
            while len(st) > 0 and st[-1].terminal:
                left_node = st.pop()
                o = st.pop()
                o.left = left_node
                o.right = et
                o.terminal = True
                et = o
            st.append(et)
    return tree


def generate_infix(node):
    priority = {"+": 0, "-": 0, "×": 1, "÷": 1, "^": 2}
    if node.value not in priority:
        return node.value
    else:
        infix = ""
        if node.left.value in priority and priority[node.left.value] < priority[node.value]:
            infix += "(" + generate_infix(node.left) + ")" + node.value
        else:
            infix += generate_infix(node.left) + node.value
        if node.right.value in priority and priority[node.right.value] < priority[node.value]:
            infix += "(" + generate_infix(node.right) + ")"
        else:
            infix += generate_infix(node.right)
        return infix


def generate_dot_tree(node):
    priority = ["+", "-", "×", "÷", "^"]
    if node.value not in priority:
        return ""
    else:
        c = node.label + " -- " + node.left.label + ";"
        c += node.label + " -- " + node.right.label + ";"
        return c + generate_dot_tree(node.left) + generate_dot_tree(node.right)


def generate_exp_tree(expression):
    tree = construct_tree_from_prefix(expression)
    str_tree = ""

    for t in tree:
        if t.value == "/":
            t.value = "÷"
            str_tree += str(t.label) + " " + "[label = &#x22;&#xF7;&#x22;];"
        elif t.value == "*":
            t.value = "×"
            str_tree += str(t.label) + " " + "[label = &#x22;&#xD7;&#x22;];"
        else:
            str_tree += str(t.label) + " " + "[label = &#x22;" + t.value + "&#x22;];"

    return generate_infix(tree[0]), "{" + str_tree + generate_dot_tree(tree[0]) + "}"


def from_infix_to_prefix(expression):
    st = list()
    res = list()
    priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 2}
    expression = deepcopy(expression)
    expression.reverse()
    for e in expression:
        if e in [")", "]"]:
            st.append(e)
        elif e == "(":
            c = st.pop()
            while c != ")":
                res.append(c)
                c = st.pop()
        elif e == "[":
            c = st.pop()
            while c != "]":
                res.append(c)
                c = st.pop()
        elif e in priority:
            while len(st) > 0 and st[-1] not in [")", "]"] and priority[e] < priority[st[-1]]:
                res.append(st.pop())
            st.append(e)
        else:
            res.append(e)
    while len(st) > 0:
        res.append(st.pop())
    res.reverse()
    return res


def out_expression_list(test, output_lang, num_list, num_stack=None):
    max_index = output_lang.n_words
    res = []
    for i in test:
        # if i == 0:
        #     return res
        if i < max_index - 1:
            idx = output_lang.index2word[i]
            if idx[0] == "N":
                if int(idx[1:]) >= len(num_list):
                    return None
                res.append(num_list[int(idx[1:])])
            else:
                res.append(idx)
        else:
            pos_list = num_stack.pop()
            c = num_list[pos_list[0]]
            res.append(c)
    return res


def compute_prefix_expression(pre_fix):
    st = list()
    operators = ["+", "-", "^", "*", "/"]
    pre_fix = deepcopy(pre_fix)
    pre_fix.reverse()
    for p in pre_fix:
        if p not in operators:
            pos = re.search("\d+\(", p)
            if pos:
                st.append(eval(p[pos.start(): pos.end() - 1] + "+" + p[pos.end() - 1:]))
            elif p[-1] == "%":
                st.append(float(p[:-1]) / 100)
            else:
                st.append(eval(p))
        elif p == "+" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            st.append(a + b)
        elif p == "*" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            st.append(a * b)
        elif p == "*" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            st.append(a * b)
        elif p == "/" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            if b == 0:
                return None
            st.append(a / b)
        elif p == "-" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            st.append(a - b)
        elif p == "^" and len(st) > 1:
            a = st.pop()
            b = st.pop()
            if float(eval(b)) != 2.0 or float(eval(b)) != 3.0:
                return None
            st.append(a ** b)
        else:
            return None
    if len(st) == 1:
        return st.pop()
    return None



