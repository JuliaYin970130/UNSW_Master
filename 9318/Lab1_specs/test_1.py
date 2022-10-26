class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


def make_tree(tokens):  # do not change the heading of the function
    if len(tokens) == 0:
        return None
    if len(tokens) == 1:
        return Tree(tokens[0])
    root = Tree(tokens[0])
    parent = root
    child = root
    root_record = []

    for i in range(1, len(tokens)):
        # 记录[之前的root
        if tokens[i] == "[":
            root_record.append(parent)
            parent = child
        # 返回上一层的root
        elif tokens[i] == "]":
            parent = root_record[-1]
        # [] 内的添加到当前root的子结点里
        else:
            child = Tree(tokens[i])
            parent.add_child(child)

    return root

def make_tree_1(tokens): # do not change the heading of the function
    root = Tree(tokens[0])
    parent = root
    node = root
    temp = []

    for i in tokens[1:]:
        if i == '[':
            temp.append(parent)
            parent = node
        elif i == ']':
            parent = temp[-1]
            temp = temp[:-1]
        else:
            node = Tree(i)
            parent.add_child(node)

    return root

def make_tree_2(tokens): # do not change the heading of the function
    tree = Tree(tokens[0])
    child = tree
    parent = Tree(tokens[0])
    root = []
    for i in range(1, len(tokens)):
        if tokens[i] == '[':
            root.append(parent)
            parent = child
            i += 1
        elif tokens[i] == ']':
            i += 1
            parent = root.pop()
            continue
        else:
            child = Tree(tokens[i])
            parent.add_child(child)
    return tree


def make_tree_3(tokens): # do not change the heading of the function
    result = ""
    for i in range(0, len(tokens)):
        if tokens[i] == '[':
            result += ',['
        if tokens[i] == ']':
            if i < len(tokens) - 1:
                if tokens[i+1] != ']':
                    result += ")]), "
                if tokens[i+1] == ']':
                    result += ")]"
            else:
                result += ")])"
        if tokens[i] not in {'[', ']'}:
            if tokens[i+1] not in {'[', ']'}:
                #result += f"Tree('{tokens[i]}'),"
                result = result + "Tree('" +tokens[i] + "'),"
            else:
                #result += f"Tree('{tokens[i]}'"
                result = result + "Tree('" +tokens[i] + "'"
    return eval(result)


def make_tree_4(tokens):  # do not change the heading of the function
    if len(tokens) == 0:
        return None
    elif len(tokens) == 1:
        return Tree(tokens[0])

    cur_tt = Tree(tokens[0])

    sep_tokens = seperate(tokens[2:-1])

    for sep_token in sep_tokens:
        res_tt = make_tree_4(sep_token)
        cur_tt.add_child(res_tt)

    return cur_tt


def seperate(words):
    if len(words) == 0:  # recursive base
        return []
    elif len(words) == 1:
        return [words]

    if words[1] != '[':  # recursive body
        res = seperate(words[1::])
        res.insert(0, [words[0]])
        return res
    else:
        list = []
        brackets = 1
        list.extend(words[0:2])

        for i in range(2, len(words)):
            if words[i] == '[':
                brackets += 1
            elif words[i] == ']':
                brackets -= 1
            list.append(words[i])

            if brackets == 0:
                break

        res = seperate(words[len(list):])
        res.insert(0, list)
        return res

def print_tree(root, indent=0):
    print(' ' * indent, root)
    if len(root.children) > 0:
        for child in root.children:
            print_tree(child, indent+4)


def make_tree_5(tokens):

    if len(tokens) == 0:
        return None
    elif len(tokens) == 1:
        return Tree(tokens[0])

    else:
        root = Tree(tokens[0])
        parent = root
        child = root
        record_parent = []

        for i in range(1, len(tokens)):
            res = make_tree_5(tokens[i])
            parent.add_child(res)


def find(word):
    for i in range(1, len(word)):
        if word == ']':
            word.pop()
            return
        if word == '[':
            continue



import submission as submission
toks =['1', '[', '2', '[', '3', '4', '5', ']', '6', '[', '7', '8', '[', '9', ']', '10', '[', '11', '12', ']', ']', '13', ']']
tt = make_tree_5(toks)
print_tree(tt)

depth = submission.max_depth(tt)
print(depth)