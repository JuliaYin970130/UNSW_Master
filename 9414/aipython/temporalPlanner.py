import sys
import searchGeneric
from cspConsistency import Con_solver, partition_domain,copy_with_assign, Arc, select
from cspProblem import Constraint, CSP
from searchProblem import Search_problem
from display import Displayable

# AIpython Reference:
# Environment:
#   searchProblem.py
#   cspConsistency.py
#   cspProblem.py
# Agent:
#   searchGeneric.py
# Display:
#   display.py

# ---------- file Input ---------- #
def file_read(file):
    with open(file, 'r') as f:
        input = f.readlines()
    return input


# ---------- file Output ---------- #
def file_out(search_result):
    if search_result:
        solution = search_result.end()
        cost = 0
        for i in solution.domains:
            start = list(solution.domains[i])[0][0]
            print(f"{i}:{start}")
            end = list(solution.domains[i])[0][1]
            cost += end
        print(f"cost:{cost}", end='')
    else:
        print("No solution", end='')

    return 0


# ---------- domain constraints update ---------- #

def domain_constraints_update(condition, duration, day, day1, day2):
    # dealing with different key words
    if condition == "starts-after":
        return [(i, i + duration - 1) for i in range(100) if i >= day]
    if condition == "starts-before":
        return [(i, i + duration - 1) for i in range(100) if i <= day]
    if condition == "ends-before":
        return [(i, i + duration - 1) for i in range(100) if i + duration - 1 <= day]
    if condition == "ends-after":
        return [(i, i + duration - 1) for i in range(100) if i + duration - 1 >= day]
    if condition == "starts-in":
        return [(i, i + duration - 1) for i in range(100) if i >= day1 and i <= day2]
    if condition == "ends-in":
        return [(i, i + duration - 1) for i in range(100) if i + duration - 1 >= day1 and i + duration - 1 <= day2]
    if condition == "between":
        return [(i, i + duration - 1) for i in range(100) if i >= day1 and i + duration - 1 <= day2]


# ---------- binary constraints update ---------- #

def binary_constraints_update(constraints, words):
    condition = words[2]
    scope = [words[1], words[3]]

    # dealing with different key words
    if condition == 'before':
        constraints.append(Constraint(scope, lambda a, b: a[1] < b[0]))
    elif condition == 'after':
        constraints.append(Constraint(scope, lambda a, b: a[0] > b[1]))
    elif condition == 'starts':
        constraints.append(Constraint(scope, lambda a, b: a[0] == b[0]))
    elif condition == 'ends':
        constraints.append(Constraint(scope, lambda a, b: a[1] == b[1]))
    elif condition == 'meets':
        constraints.append(Constraint(scope, lambda a, b: a[1] + 1 == b[0]))
    elif condition == 'overlaps':
        constraints.append(Constraint(scope, lambda a, b: b[0] > a[0] and b[0] <= a[1] and b[1] > a[1]))
    elif condition == 'during':
        constraints.append(Constraint(scope, lambda a, b: a[0] > b[0] and a[1] < b[1]))
    elif condition == 'equals':
        constraints.append(Constraint(scope, lambda a, b: a[0] == b[0] and a[1] == b[1]))


# ---------- Environment initialization ---------- #

def initial_env(input):
    # structure from cspExamples.py
    domain = {}  # {task:[(start1,end1),(start2,end2)...]}
    constraints = []  # [Constraint(scope,condition)]

    for line in input:
        words = line.strip().split(' ')
        # task initial
        if words[0] == 'task':
            task = words[1]
            duration = int(words[2])
            domain[task] = [(i, i + duration - 1) for i in range(100)]
        # binary constraints update
        if words[0] == 'constraint':
            # dealing with different key words
            binary_constraints_update(constraints, words)
        # domain constraints update
        if words[0] == 'domain':
            task = words[1]
            condition = words[2]
            days = domain[task][0]
            duration = days[1] + 1 - days[0]
            day, day1, day2 = 0, 0, 0
            if len(words) == 5:
                day1 = int(words[-2])
                day2 = int(words[-1])
            else:
                day = int(words[-1])
            prev_domain = domain[task]
            cur_domain = domain_constraints_update(condition, duration, day, day1, day2)
            intersection = list(set(cur_domain) & set(prev_domain))
            if intersection:
                intersection.sort(key=prev_domain.index)
                domain[task] = intersection
            else:
                domain[task] = []

    csp = new_CSP(domain, constraints)
    return csp



class new_CSP(CSP):
    """
    update original CSP
    add parameter - cost
    cost_calculation - sums minimal costs over the set of all variables
    """
    def __init__(self, domains, constraints):
        super().__init__(domains, constraints)
        self.cost = self.cost_calculation()

    def cost_calculation(self):
        min_end = []
        end = []
        temp_domain = self.domains.copy()
        for i in temp_domain.keys():
            if temp_domain[i]:
                for j in temp_domain[i]:
                    end_day = j[1]
                    end.append(end_day)
                min_ = min(end)
                end = []
                min_end.append(min_)
        h_value = sum(min_end)
        return h_value


# ---------- Search Problem ---------- #

class Search_with_AC_from_Cost_CSP(Search_problem,Displayable):
    """
    A search problem with arc consistency and domain splitting
    A node is a CSP
    Structure reference from cspConsistency.Search_with_AC_from_CSP()
    """

    def __init__(self, csp):
        self.csp = csp
        self.cons = Con_solver(self.csp)  # copy of the CSP
        self.domains = self.cons.make_arc_consistent()

    def start_node(self):
        return self.csp

    def is_goal(self, node):
        """node is a goal if all domains have 1 element"""
        variables = node.domains
        return all(len(variables[var]) == 1 for var in variables)

    def neighbors(self, node):
        """returns the neighboring nodes of node.
        """
        neighs = []
        variables = node.domains
        var = select(x for x in variables if len(variables[x]) > 1)
        # print(var)
        if var:
            temp_domain = node.domains
            dom1, dom2 = partition_domain(set(temp_domain[var]))
            self.display(2, "Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var, None)
            # {(var,cons)}
            for dom in [dom1, dom2]:
                newdoms = copy_with_assign(temp_domain, var, dom)
                cons_doms = self.cons.make_arc_consistent(newdoms, to_do)
                if all(len(cons_doms[v]) > 0 for v in cons_doms):
                    # all domains are non-empty
                    neighs.append(Arc(node, new_CSP(cons_doms, node.constraints)))
                else:
                    self.display(2,"...",var,"in",dom,"has no solution")

        return neighs

    def heuristic(self, path):
        """Gives the heuristic value of node n."""
        return path.cost


# ---------- Greedy Search ---------- #

class Search_Agent(searchGeneric.AStarSearcher):
    """
    returns a searcher for a problem.
    Using priority queue to minimize the cost
    Paths can be found by repeatedly calling search().
    """

    max_display_level = 0

    def __init__(self, problem):
        super().__init__(problem)

    def add_to_frontier(self, path):
        """add path to the frontier with the appropriate cost"""
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


if __name__ == "__main__":
    input_file = 'input1.txt'
    # input_file = sys.argv[1]
    input_data = file_read(input_file)
    csp = initial_env(input_data)
    search_result = Search_Agent(Search_with_AC_from_Cost_CSP(csp)).search()
    file_out(search_result)


