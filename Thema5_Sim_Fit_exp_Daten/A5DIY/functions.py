import numpy as np


def rand_dist(f, a, b, maxf):
    """
    Returns random numbers between a and b distributed with f
    Warning: this method is very ineffective for strongly varying f

    Advice: Generate the distribution function via random.choice (from numpy)
    Example for Gauß function between -5 and 5, sigma = 1:
    1. Generate the y range: 
    y = np.linspace(-5,5,num=1000)
    2. Generate and normalize the distribution
    py = np.exp(-y*y/2)
    ps = py.sum()
    py = py / ps
    3. Generate 1000 random numbers according to this distribution
    x = random.choice(y,p=py,size=1000)
    """
    while True:
        x, y = np.random.random(2)
        x = a + (b-a)*x
        y = y*maxf
        if y <= f(x):
            return x
        

def fifty_fifty():
    return np.random.random() <= 0.5
        

# def rand_dist(f, a, b, size=1):
#     """
#     Generate random numbers according to the given distribution function f
#     between a and b.
    
#     Parameters:
#     f (function): The distribution function
#     a (float): The lower bound of the range
#     b (float): The upper bound of the range
#     size (int): The number of random numbers to generate
    
#     Returns:
#     numpy.ndarray: Array of random numbers according to the distribution f
#     """
#     y = np.linspace(a, b, 1000)
#     py = f(y)
#     py = py / py.sum()
#     return np.random.choice(y, p=py, size=size)