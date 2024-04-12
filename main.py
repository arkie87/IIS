from scipy.optimize import linprog


class LinProblem:
    def __init__(self, c, A_eq, b_eq, bounds=None):
        bounds = bounds if bounds else [(None, None) * len(A[0])]
    
        self.c = c
        self.A_eq = A_eq
        self.b_eq = b_eq
        self.bounds = bounds
        
    def optimize(self):
        self.sol = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, bounds = self.bounds)

    def iis(self):
        self.optimize()
        if self.sol.success:
            print("Solution already feasible")
            print(self.sol)
            return 
        else:
            iis = []
            for i in range(len(self.A_eq)):
            
                A_eq = self.A_eq.copy() 
                del A_eq[i]
                
                b_eq = self.b_eq.copy()
                del b_eq[i]
                
                subproblem = LinProblem(self.c, A_eq, b_eq, self.bounds)
                subproblem.optimize()
                if subproblem.sol.success:
                    iis += [i]
            
            if not iis:
                return self.iis2()
                
            return iis
            
    def iis2(self):
        
        self.optimize()
        if self.sol.success:
            print("Solution already feasible")
            print(self.sol)
            return
        else:
            iis = []
            for i in range(len(self.A_eq)-1):
                for j in range(i+1, len(self.A_eq)):
            
                    A_eq = self.A_eq.copy() 
                    del A_eq[j]
                    del A_eq[i]
                    
                    b_eq = self.b_eq.copy()
                    del b_eq[j]
                    del b_eq[i]
                    
                    subproblem = LinProblem(self.c, A_eq, b_eq, self.bounds)
                    subproblem.optimize()
                    if subproblem.sol.success:
                        iis += [(i,j)]
            
            return iis


c = [-1, 4, 2]
A = [
    [-3, 1, -5],
    [ 1, 2,  -1],
    [ 0, 0,   5]
]
b = [-16, 2,15]

lp = LinProblem(c, A, b, bounds=[(0,None), (2.1, None), (0, 2.9)])
iis = lp.iis()

print(iis)