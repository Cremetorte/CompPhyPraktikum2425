import numpy as np

# Aufgabe 1 a)

def monte_carlo_pi(n):
    count_inside = 0

    for _ in range(n):
        x = np.random.uniform(0, 1, 1)  # Stichprobenpunkte im Einheitsquadrat
        y = np.random.uniform(0, 1, 1)
        if x**2 + y**2 <= 1:  # Prüfen, ob der Punkt im Kreis liegt
            count_inside += 1
    
    return 4 * count_inside / n

# Berechnung
n_samples = 1_000_000
approx_pi = monte_carlo_pi(n_samples)
print(f"Monte-Carlo Approximation von Pi mit {n_samples} Stichproben: {approx_pi:.6f}")

# Aufgabe 1 b)

def monte_carlo_integral(n, mu=0, sigma=1):
    samples = np.random.normal(mu, sigma, n)  # Zufallsgenerator für Normalverteilung
    integral_estimate = np.mean(np.exp(-samples**2 / 2)) * 2 * np.sqrt(np.pi)  # Monte-Carlo-Integration
    return integral_estimate

# Berechnung
n_samples = 1_000_000
integral_value = monte_carlo_integral(n_samples)
print(f"Monte-Carlo Approximation des Integrals mit {n_samples} Stichproben: {integral_value:.6f}")