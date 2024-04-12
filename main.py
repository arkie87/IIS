from numba import njit, jit, boolean
from scipy.optimize import linprog

@njit("float(f8[:,:],f8[:,:],f8[:,:],f8[:,:],f8[:,:],f8[:,:])")
def optimize(c, A_eq=None, b_eq=None, A_ineq=None, b_ineq=None, bounds=None):
    N = len(c)
    M_eq = 0 if b_eq is None else len(b_eq)
    M_ineq = 0 if b_ineq is None else len(b_ineq)
    M = M_eq + M_ineq
    bounds = bounds if bounds else [(None, None) * N]
    sol = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ineq, b_ub=b_ineq, bounds=bounds)
    x = sol.x
    return x


@jit
def copy(A_eq, b_eq, A_ineq, b_ineq):
    return *copy_eq(A_eq, b_eq), *copy_ineq(A_ineq, b_ineq)

@jit
def copy_eq(A_eq, b_eq):
    if b_eq is None:
        return None, None
    else:
        return A_eq.copy(), b_eq.copy()


@jit
def copy_ineq(A_ineq, b_ineq):
    if b_ineq is None:
        return None, None
    else:
        return A_ineq.copy(), b_ineq.copy()


@jit
def iis(c, A_eq=None, B_eq=None, A_ineq=None, B_ineq=None, bounds=None):
    N = len(c)
    M_eq = 0 if B_eq is None else len(B_eq)
    M_ineq = 0 if B_ineq is None else len(B_ineq)
    M = M_eq + M_ineq
    bounds = bounds if bounds else [(None, None) for _ in range(N)]
    
    x = optimize(c, A_eq, B_eq, A_ineq, B_ineq, bounds)
    if x is not None:
        print("Solution already feasible")
        return 
    else:
        iis = []
        
        for i in range(M):
            
            a_eq, b_eq, a_ineq, b_ineq = copy(A_eq, B_eq, A_ineq, B_ineq)
            
            if i < M_eq:
                del a_eq[i]
                del b_eq[i]
            else:
                del a_ineq[i]
                del b_ineq[i]
            
            x = optimize(c, a_eq, b_eq, a_ineq, b_ineq, bounds)
            if x is not None:
                iis += [i]
            
        return iis
    

            
# def iis2(self):
    # self.optimize()
    # if self.sol.success:
        # print("Solution already feasible")
        # print(self.sol)
        # return
    # else:
        # iis = []
        
        # for i in range(self.N - 1):
            # for j in range(i + 1, self.N):
                # A_eq, b_eq, A_ineq, b_ineq = self.copy()
                
                # if i < self.N_eq:
                    # del A_eq[j]
                    # del b_eq[j]
                    # del A_eq[i]
                    # del b_eq[i]
                # else:
                    # del A_ineq[j]
                    # del b_ineq[j]
                    # del A_ineq[i]
                    # del b_ineq[i]
                
                # subproblem = LinearProblem(self.c, A_eq, b_eq, A_ineq, b_ineq, self.bounds)
                # subproblem.optimize()
                # if subproblem.sol.success:
                    # iis += [(i, j)]
        
        # return iis


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

    #lp = LinearProblem(c.tolist(), A.tolist(), b.tolist(), bounds=bounds)
    iis = iis(c.tolist(), A.tolist(), b.tolist(), bounds=bounds)

    print(iis)