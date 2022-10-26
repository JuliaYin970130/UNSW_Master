## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    minimum = 0
    maximum = x//2
    result = 0
    target = x

    if x == 0 or x == 1:
        return x
    else:
        while minimum <= maximum:
            middle = minimum + (maximum - minimum)//2
            double_middle = middle*middle

            if double_middle > target:
                maximum = middle - 1
            else:
                result = middle
                minimum = middle + 1
        return result


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    # x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}
    f_value = f(x_0)
    fprime_value = fprime(x_0)
    x_new = x_0 - f_value / fprime_value
    x = x_0

    for i in range(1, MAX_ITER):
        if abs(x - x_new) < EPSILON:
            return x_new
        else:
            x = x_new
            f_value = f(x)
            fprime_value = fprime(x)
            x_new = x - f_value / fprime_value
            #x_new = x - f(x)/fprime(x)

    return x_new



################# Question 3 #################

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

def make_tree(tokens): # do not change the heading of the function

    if len(tokens) == 0:
        return None
    elif len(tokens) == 1:
        return Tree(tokens[0])
    else:
        root = Tree(tokens[0])
        parent = root
        child = root
        # stack
        parent_record = []

        for i in range(1, len(tokens)):
            # 记录[之前的parent
            if tokens[i] == "[":
                parent_record.append(parent)
                parent = child
                continue
            # 返回上一层的parent
            if tokens[i] == "]":
                parent = parent_record.pop()
                # out of range
                continue
            # [] 内的添加到当前parent的子结点里
            child = Tree(tokens[i])
            parent.add_child(child)

        return root


def max_depth(root): # do not change the heading of the function
    count = [1]
    maxDepth = max(count)
    if root.children is None:
        return maxDepth
    else:
        for i in root.children:
            depth = max_depth(i) + 1
            count.append(depth)
        maxDepth = max(count)
        return maxDepth

    #pass # **replace** this line with your code
