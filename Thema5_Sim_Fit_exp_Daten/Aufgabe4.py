from ctypes import ArgumentError
from networkx import reverse
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def l_2_norm(x):
    return np.linalg.norm(x)

def Himmelblau(x):
    y = x[1]
    x = x[0]
    return (x**2 + y -11)**2 + (x+y**2-7)**2


def downhill_simplex(func, f_dim, alpha=1, gamma=1, beta=0.5, sigma=0.5, start_points=None, tolerance=1e-10):
    # handle starting points
    if start_points is None:
        #initialize starting points randomly
        start_points = []
        for i in range(f_dim+1):
            start_points.append(np.random.random(f_dim))
    else:
        # get start_points
        try:
            if len(start_points) != f_dim+1:
                raise ArgumentError(f"Wrong Number of Starting points! Needed: {f_dim+1}, given: {len(start_points)}.")
            for i in start_points:
                if len(i) != f_dim:
                    raise ArgumentError(f"Starting points are of wrong dimension! Needed: {f_dim}, given: {len(i)}.")
        except:
            raise ArgumentError(f"Type of start_points has to be arraylike! Given type: {type(start_points)}.")
    

    # convert to np array
    points = np.array(start_points)
        

    for i in range(1000):
        # ------------------------------------------------ Sort points by function
        func_vals = [func(point) for point in points]
        # check for convergence
        if np.std(func_vals) < tolerance:
            break

        sorted_indices = np.argsort(func_vals)

        points = points[sorted_indices]
        # print(points)

        worst_point = points[-1]
        worst_f = func(worst_point)

        # ------------------------------------------------ calculate middle point
        mp = np.mean(points[:-1],axis=0)

        # ------------------------------------------------ reflect worst point at middle point
        r = mp + alpha*(mp - worst_point)
    
        # ------------------------------------------------ check if r is new best point
        if func(r) < func(points[0]):
            # expanded point
            e = r + gamma*(r - mp)
            
            # choose the better point of e or r
            points[-1] = e if func(e) < func(r) else r
            continue
        
        # ------------------------------------------------ check if r is better than the second worst point
        if func(r) < func(points[-2]):
            points[-1] = r
            continue
            
        # ------------------------------------------------ calaculate contracted point c
        h = worst_point if worst_f < func(r) else r
        c = h + beta*(mp - h)

        # ------------------------------------------------ check if c is better than the worst point
        if func(c) < worst_f:
            points[-1] = c
            continue
        
        # ------------------------------------------------ compress simplex
        points = points + sigma*(points[0]-points)


    # print(points)
    return points[0]



