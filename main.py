from scipy.optimize import linprog


class LinearProblem:
    def __init__(self, c, A_eq=None, b_eq=None, A_ineq=None, b_ineq=None, bounds=None):
        self.c = c
        self.A_eq = A_eq
        self.b_eq = b_eq
        self.A_ineq = A_ineq
        self.b_ineq = b_ineq
        self.bounds = bounds if bounds else [(None, None) * len(A[0])]
        
        self.N_eq = 0 if self.b_eq is None else len(self.b_eq)
        self.N_ineq = 0 if self.b_ineq is None else len(self.b_ineq)
        self.N = self.N_eq + self.N_ineq
        
    def optimize(self):
        self.sol = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, A_ub=self.A_ineq, b_ub=self.b_ineq, bounds=self.bounds)
        
    def copy(self):
        return *self.copy_eq(), *self.copy_ineq()
    
    def copy_eq(self):
        if self.b_eq is None:
            return None, None
        else:
            return self.A_eq.copy(), self.b_eq.copy()

    def copy_ineq(self):
        if self.b_ineq is None:
            return None, None
        else:
            return self.A_ineq.copy(), self.b_ineq.copy()

    def iis(self):
        self.optimize()
        if self.sol.success:
            print("Solution already feasible")
            print(self.sol)
            return 
        else:
            iis = []
            
            for i in range(self.N):
                
                A_eq, b_eq, A_ineq, b_ineq = self.copy()
                
                if i < self.N_eq:
                    del A_eq[i]
                    del b_eq[i]
                else:
                    del A_ineq[i]
                    del b_ineq[i]
                
                subproblem = LinearProblem(self.c, A_eq, b_eq, A_ineq, b_ineq, self.bounds)
                subproblem.optimize()
                if subproblem.sol.success:
                    iis += [i]
                
            return iis
            
    def iis2(self):
        self.optimize()
        if self.sol.success:
            print("Solution already feasible")
            print(self.sol)
            return
        else:
            iis = []
            
            for i in range(self.N - 1):
                for j in range(i + 1, self.N):
                    A_eq, b_eq, A_ineq, b_ineq = self.copy()
                    
                    if i < self.N_eq:
                        del A_eq[j]
                        del b_eq[j]
                        del A_eq[i]
                        del b_eq[i]
                    else:
                        del A_ineq[j]
                        del b_ineq[j]
                        del A_ineq[i]
                        del b_ineq[i]
                    
                    subproblem = LinearProblem(self.c, A_eq, b_eq, A_ineq, b_ineq, self.bounds)
                    subproblem.optimize()
                    if subproblem.sol.success:
                        iis += [(i, j)]
            
            return iis


if __name__ == "__main__":
    from numpy.random import random
    
    c = [-1, 4, 2]
    A = [
        [-3, 1, -5],
        [ 1, 2,  -1],
        [ 0, 0,   5]
    ]
    b = [-16, 2,15]
    
    bounds = [(0,None), (2.1, None), (0, 2.9)]
    
    N = 1000
    M = 100
    A = random((M, N))
    A[A<0.5]=0
    b = 100*random(M)
    c = random(N)
    
    
    bounds = [(0, None) for _ in range(N)]

    lp = LinearProblem(c.tolist(), A.tolist(), b.tolist(), bounds=bounds)
    iis = lp.iis()

    print(iis)