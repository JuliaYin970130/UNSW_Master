from searchGeneric import AStarSearcher
from cspProblem import Constraint,CSP
from cspConsistency import Search_with_AC_from_CSP,select
import sys

class mySearcher(AStarSearcher):
    """returns a searcher for a problem.
    Using priority queue to minimize the cost
    Paths can be found by repeatedly calling search().
    """
    def __init__(self, problem):
        super().__init__(problem)

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost,
        path cost is set to 0 in this problem
        """
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)
 
class myCSP(CSP):
    """A CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    """
    def __init__(self, domains, constraints, durations, positions={}):
        super().__init__(domains, constraints, positions)
        self.durations = durations
        self.cost = self.heuristic_cost()

    def heuristic_cost(self):
        sum_cost = 0
        for var in self.variables:
            min_cost = 100
            duration = self.durations[var]  # the duration of the current task
            for val in self.domains[var]:
                if val < min_cost:
                    min_cost = val
            sum_cost += min_cost + duration - 1
        return sum_cost

class Search_with_AC_from_cost_CSP(Search_with_AC_from_CSP):
    def __init__(self, csp):
        super().__init__(csp)

    def heuristic(self,node):
        """Gives the heuristic value of a node.
        """
        sum_cost = 0
        for var in self.cons.csp.variables:
            min_cost = 100
            duration = self.cons.csp.durations[var]  # the duration of the current task
            for val in node[var]:
                if val < min_cost:
                    min_cost = val
            sum_cost += min_cost + duration - 1
        return sum_cost

def ac_search_solver(csp):
    """arc consistency (search interface)"""
    sol = mySearcher(Search_with_AC_from_cost_CSP(csp)).search()
    if sol:
        return {v:select(d) for (v,d) in sol.end().items()}
    else:
        return {}


if __name__ == "__main__":
    # check the command line arguments
    if len(sys.argv) != 2:
        print("Wrong number of arguments! Usage: python3 temporalPlanner.py input_filename.txt")
        sys.exit()
    
    domains = {}
    constraints = []
    durations = {}
    input_filename = sys.argv[1]
    with open(input_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0 and line[0] == '#':  # skip the comment lines
                continue
            line = line.split()
            if line[0] == 'task':  # task lines
                domains[line[1]] = set(range(100))
                durations[line[1]] = int(line[2])  # store the durations of tasks
            elif line[0] == 'constraint':  # binaray constraint lines
                duration1 = durations[line[1]]  # duration for the first task
                duration2 = durations[line[3]]  # duration for the second task
                # dealing with different key words
                if line[2] == 'before':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1: a+duration1-1<b,
                        "{}+{}-1<{}".format(line[1],duration1,line[3])))
                elif line[2] == 'after':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration2=duration2: a>b+duration2-1,
                        "{}>{}+{}-1".format(line[1],line[3],duration2)))
                elif line[2] == 'starts':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b: a==b,
                        "{}={}".format(line[1],line[3])))
                elif line[2] == 'ends':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1,duration2=duration2: a+duration1==b+duration2,
                        "{}+{}={}+{}".format(line[1],duration1,line[3],duration2)))
                elif line[2] == 'meets':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1: a+duration1==b,
                        "{}+{}={}".format(line[1],duration1,line[3])))
                elif line[2] == 'overlaps':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1,duration2=duration2: b>a and b<=a+duration1-1 and b+duration2>a+duration1,
                        "{}>{} and {}<={}+{}-1 and {}+{}>{}+{}".format(line[3],line[1],line[3],line[1],duration1,line[3],duration2,line[1],duration1)))
                elif line[2] == 'during':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1,duration2=duration2: a>b and a+duration1<b+duration2,
                        "{}>{} and {}+{}<{}+{}".format(line[1],line[3],line[1],duration1,line[3],duration2)))
                elif line[2] == 'equals':
                    constraints.append(Constraint([line[1],line[3]],
                        lambda a,b,duration1=duration1,duration2=duration2: a==b and a+duration1==b+duration2,
                        "{}={} and {}+{}={}+{}".format(line[1],line[3],line[1],duration1,line[3],duration2)))
            elif line[0] == 'domain':  # domain constraint lines
                duration = durations[line[1]]
                # dealing with different key words
                if line[2] == 'starts-before':
                    day = int(line[3])
                    constraints.append(Constraint([line[1]],
                        lambda a,day=day: a<=day,
                        "{}<={}".format(line[1],day)))
                elif line[2] == 'starts-after':
                    day = int(line[3])
                    constraints.append(Constraint([line[1]],
                        lambda a,day=day: a>=day,
                        "{}>={}".format(line[1],day)))
                elif line[2] == 'ends-before':
                    day = int(line[3])
                    constraints.append(Constraint([line[1]],
                        lambda a,day=day,duration=duration: a+duration-1<=day,
                        "{}+{}-1<={}".format(line[1],duration,day)))
                elif line[2] == 'ends-after':
                    day = int(line[3])
                    constraints.append(Constraint([line[1]],
                        lambda a,day=day,duration=duration: a+duration-1>=day,
                        "{}+{}-1>={}".format(line[1],duration,day)))
                elif line[2] == 'starts-in':
                    day1 = int(line[3])
                    day2 = int(line[4])
                    constraints.append(Constraint([line[1]],
                        lambda a,day1=day1,day2=day2: a>=day1 and a<=day2,
                        "{}>={} and {}<={}".format(line[1],day1,line[1],day2)))
                elif line[2] == 'ends-in':
                    day1 = int(line[3])
                    day2 = int(line[4])
                    constraints.append(Constraint([line[1]],
                        lambda a,day1=day1,day2=day2,duration=duration: a+duration-1>=day1 and a+duration-1<=day2,
                        "{}+{}-1>={} and {}+{}-1<={}".format(line[1],duration,day1,line[1],duration,day2)))
                elif line[2] == 'between':
                    day1 = int(line[3])
                    day2 = int(line[4])
                    constraints.append(Constraint([line[1]],
                        lambda a,day1=day1,day2=day2,duration=duration: a>=day1 and a+duration-1<=day2,
                        "{}>={} and {}+{}-1<={}".format(line[1],day1,line[1],duration,day2)))
    # construct a CSP problem and solve it
    csp = myCSP(domains,constraints,durations)
    sol = ac_search_solver(csp)

    # print output to standard output
    total_cost = 0
    for key,val in sol.items():
        print("{}:{}".format(key,val))
        total_cost += val + durations[key] - 1

    if sol:
        print("cost:{}".format(total_cost),end="")
    else:
        print("No solution",end="")
