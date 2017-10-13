# dodo code
def matrixmultiply(A,B):
    
    if len(B) != len(A[0]):
        print "Matrices cannot be multiplied due to dimensions!"
        return None
    
    else:    
        result = [[sum(a*b for a,b in zip(A_rows,B_cols)) for B_cols in zip(*B)] for A_rows in A]
 
        return result      
##

def identity(n):
    return [ [ 1. if i==j else 0. for i in range(n) ] for j in range(n) ]        

        
def rearrangeForPivot(problem, c):
    # find largest abs val element in col below row col
    n = len (problem)
    mx = (-1, None)
    for r in range(c,n):
        if abs(problem[r][c]) > mx[0]:
            mx = (abs(problem[r][c]), r)
    mr = mx[1];
    #swap row mr into row c
    mat = identity(n)
    mat[mr][mr] = 0.; mat[c][c] = 0.
    mat[mr][c] = 1.; mat[c][mr] = 1./problem[mr][c]
    return matrixmultiply(mat, problem)
    

def gje( problem ):
    n = len(problem)
    for c in range(n):
        # rearrange for pivot
        problem = rearrangeForPivot(problem, c)
        mat = identity(n)
        for r in range(n):
            if r != c:
                mat[r][c] = - problem[r][c]
        problem = matrixmultiply(mat, problem)
    return problem
        
problem = [  [ 1., 1., 1., 6. ],
             [ 1., 2., 3., 14. ],
             [ 4., 3., 1., 13. ] ]

print gje(problem)
