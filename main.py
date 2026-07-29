import random, math, sys

class CSP:
    def __init__(self, n):
        self.name = 'n-queen problem'
        self.n = n
        self.vars = list(range(n))
        self.domains = [[j for j in range(n)] for k in range(n)]
    
    def isSolution(self, state):
        if len(self.conflictedVars(state)) == 0:
            return True
        return False

    def conflictedVars(self, state):
        conflicted_vars = []
        for queen, value in state.vars.items():
            if self.conflicts(queen, value, state) != 0:
                conflicted_vars.append(queen)
        return conflicted_vars
    
    def conflicts(self, var, value, state):
        c = 0
        for queen in self.vars:
            if queen == var:
                continue
            if self.conflict((var, value), queen, state):
                c += 1
        return c

    def domain(self, var):
        return self.domains[var]

    def conflict(self, value, queen, state):
        if value[1] == state.vars[queen]:
            return True
        if abs(value[1] - state.vars[queen]) == abs(value[0] - queen):
            return True
        return False


class State:
    def __init__(self, n):
        self.n = n
        self.vars = {}
        self.arr = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append('-')
            self.arr.append(row)
    
    def set(self, var, value):
        self.vars[var] = value
    
    def __str__(self):
        string = ""
        for var, value in self.vars.items():
            self.arr[var][value] = 'Q'
        for i in range(self.n):
            for j in range(self.n):
                string += self.arr[i][j] + ' '
            string += '\n'
        string = string[:-1]
        return string


def minConflicts(csp, max_steps, current_state):
    for i in range(max_steps):
        if csp.isSolution(current_state):
            return current_state
        conflicted_vars = csp.conflictedVars(current_state)
        var = random.choice(conflicted_vars)
        value = random.choice(minConflictsValues(var, current_state, csp))
        current_state.set(var, value)
    return None

def minConflictsValues(var, state, csp):
    min_conflicts = math.inf
    values = []
    for v in csp.domain(var):
        conflicts = csp.conflicts(var, v, state)
        if conflicts < min_conflicts:
            values = []
            min_conflicts = conflicts
            values.append(v)
            continue
        if conflicts == min_conflicts:
            values.append(v)
    return values

def greedyInitial(n):
    state = State(n)
    arr = list(range(n))
    random.shuffle(arr)
    for i in range(n):
        state.set(i, arr[i])
    return state

n = 8
max_steps = 10
if len(sys.argv) == 2:
    n = int(sys.argv[1])
if len(sys.argv) == 3:
    n = int(sys.argv[1])
    max_steps = int(sys.argv[2])
csp = CSP(n)
solution = None
iteration = 0
while solution is None:
    initial_state = greedyInitial(n)
    solution = minConflicts(csp, max_steps, initial_state)
    iteration += 1
print(solution)
print("Solution found in iteration: {0}".format(iteration))