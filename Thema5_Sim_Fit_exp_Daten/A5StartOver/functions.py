import numpy as np


def random_percent(probability):
    if probability > 1:
        raise ValueError("Probability must be between 0 and 1")
    return np.random.rand() < probability


def rand_dist(f, a, b, maxf):
    while True:
        x, y = np.random.rand(2)
        x = a + (b-a)*x
        y = y*maxf
        if y <= f(x):
            return x
        


def rand_dist_alt(f, a, b, alpha=0.5, M=None, grid_points=1000):
    """
    Sample a random number x in the interval [a, b] according to the target density f(x),
    die eventuell bei x -> a divergiert.
    
    Es wird die Transformation
        x = a + (b - a) * u^(1/alpha)
    verwendet, wobei u ~ U(0,1) ist.
    
    Dadurch lautet die Dichte des Vorschlags g(x):
        g(x) = (1/alpha) / (b - a) * ((x - a)/(b - a))^(1/alpha - 1)
    
    Der Parameter alpha (< 1) sorgt dafür, dass mehr Samples im unteren Bereich (nahe a) gezogen werden.
    
    Parameter:
      f          : Ziel-Dichtefunktion (nicht normiert), definiert auf [a, b].
      a, b       : Untere und obere Grenze.
      alpha      : Transformationsparameter (empfohlen: alpha < 1, z.B. 0.5).
      M          : Optionales Supremum von f(x)/g(x) über [a,b]. Falls None, wird M auf einem Gitter geschätzt.
      grid_points: Anzahl der Punkte zur Abschätzung von M, falls M nicht angegeben wird.
      
    Returns:
      x          : Ein Zufallswert gemäß f(x).
    """
    # Abschätzung von M, falls nicht vorgegeben:
    if M is None:
        xs = np.linspace(a, b, grid_points)
        # Berechne g(x) entsprechend der Transformation:
        gxs = (1/alpha) / (b - a) * (((xs - a) / (b - a)) ** (1/alpha - 1))
        # Um Division durch Null zu vermeiden, setze bei x == a einen sehr kleinen Wert:
        gxs = np.where(xs == a, 1e-12, gxs)
        ratios = f(xs) / gxs
        M = ratios.max()

    while True:
        u = np.random.rand()
        # Transformation: x wird gezielt im unteren Bereich stärker gewichtet
        x = a + (b - a) * (u ** (1/alpha))
        # Berechne die Dichte des Vorschlags g(x)
        g = (1/alpha) / (b - a) * (((x - a) / (b - a)) ** (1/alpha - 1))
        # Akzeptanzwahrscheinlichkeit
        if np.random.rand() < f(x) / (M * g):
            return x