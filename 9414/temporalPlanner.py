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
#   cspExamples.py
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

def binary_constraints_update(constraints):
    def before(t1, t2):
        return t1[1] < t2[0]

    def after(t1, t2):
        return t1[0] > t2[1]

    def starts(t1, t2):
        return t1[0] == t2[0]

    def ends(t1, t2):
        return t1[1] == t2[1]

    def meets(t1, t2):
        return t1[1] + 1 == t2[0]

    def overlaps(t1, t2):
        return (t1[0] < t2[0] and t1[1] >= t2[0]) and t1[1] < t2[1]

    def during(t1, t2):
        return t1[0] > t2[0] and t1[1] < t2[1]

    def equals(t1, t2):
        return t1[0] == t2[0] and t1[1] == t2[1]

    if constraints == "before":
        return before
    if constraints == "after":
        return after
    if constraints == "starts":
        return starts
    if constraints == "ends":
        return ends
    if constraints == "meets":
        return meets
    if constraints == "overlaps":
        return overlaps
    if constraints == "during":
        return during
    if constraints == "equals":
        return equals


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
            task1 = words[1]
            task2 = words[-1]
            scope = [task1, task2]
            request = words[2]
            condition = binary_constraints_update(request)
            # print(condition)
            constraints.append(Constraint(scope, condition))

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
    '''
    update original CSP
    add parameter - cost
    cost_calculation - sums minimal costs over the set of all variables
    '''

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
    Reference from cspConsistency.Search_with_AC_from_CSP()
    """

    def __init__(self, csp):

        self.csp = csp
        self.cons = Con_solver(csp)  # copy of the CSP
        self.domains = self.cons.make_arc_consistent()

    def start_node(self):
        return self.csp

    def is_goal(self, node):
        """node is a goal if all domains have 1 element"""
        return all(len(node.domains[var]) == 1 for var in node.domains)

    def neighbors(self, node):
        """returns the neighboring nodes of node.
        """
        neighs = []
        var = select(x for x in node.domains if len(node.domains[x]) > 1)
        # print(var)
        if var:
            temp_domain = node.domains
            dom1, dom2 = partition_domain(set(temp_domain[var]))
            self.display(2, "Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var, None)
            # {(var,cons)}
            for dom in [dom1, dom2]:
                newdoms = copy_with_assign(node.domains, var, dom)
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
    max_display_level = 0

    def __init__(self, problem):
        super().__init__(problem)

    def add_to_frontier(self, path):
        """add path to the frontier with the appropriate cost"""
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


if __name__ == "__main__":
    input_file = sys.argv[1]
    input_data = file_read(input_file)
    csp = initial_env(input_data)
    # print(csp)
    search_result = Search_Agent(Search_with_AC_from_Cost_CSP(csp)).search()
    file_out(search_result)


