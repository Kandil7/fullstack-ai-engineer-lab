"""
02 - Getting Started with SciPy
================================
This module covers installation, basic usage patterns, and the core
workflow for using SciPy in scientific computing projects.

Topics:
- Installation and import patterns
- SciPy's relationship with NumPy
- Basic array operations with SciPy extensions
- Working with sparse matrices
"""

import numpy as np

# ============================================================
# Example 1: Import Patterns and Version Check
# ============================================================
print("=" * 60)
print("Example 1: Import Patterns and Version Info")
print("=" * 60)

import scipy
import scipy.stats
import scipy.optimize
from scipy import linalg, integrate, interpolate

print(f"SciPy version:  {scipy.__version__}")
print(f"NumPy version:  {np.__version__}")
print(f"Python built on top of NumPy arrays")
print(f"SciPy adds: optimization, integration, interpolation, linalg, stats")

# Common import alias conventions
print("\nCommon import conventions:")
print("  import scipy.stats as stats")
print("  from scipy.optimize import minimize")
print("  from scipy.integrate import quad")
print("  import scipy.sparse as sp")

# ============================================================
# Example 2: Basic SciPy Operations
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Basic Operations with SciPy")
print("=" * 60)

from scipy import constants

# Physical calculations using constants
def kinetic_energy(mass_kg, velocity_ms):
    """Calculate kinetic energy: KE = 0.5 * m * v^2"""
    return 0.5 * mass_kg * velocity_ms**2

def gravitational_force(m1_kg, m2_kg, distance_m):
    """Newton's gravitational force between two masses."""
    G = constants.G  # Gravitational constant
    return G * m1_kg * m2_kg / distance_m**2

# Earth-Moon system
earth_mass = 5.972e24   # kg
moon_mass = 7.342e22    # kg
earth_moon_dist = 3.844e8  # meters

force = gravitational_force(earth_mass, moon_mass, earth_moon_dist)
print(f"Gravitational force Earth-Moon: {force:.4e} N")

# Kinetic energy of a car
car_mass = 1500  # kg
car_speed_ms = 30  # m/s (108 km/h)
ke = kinetic_energy(car_mass, car_speed_ms)
print(f"Kinetic energy of car at 108 km/h: {ke:.0f} J = {ke/1000:.1f} kJ")

# ============================================================
# Example 3: Sparse Matrices (scipy.sparse)
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Working with Sparse Matrices")
print("=" * 60)

from scipy import sparse

# Dense matrix: most elements are zero
dense = np.array([
    [1, 0, 0, 0, 5],
    [0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 0, 7, 0],
])

# Convert to sparse (CSR format)
sparse_mat = sparse.csr_matrix(dense)
print(f"Dense matrix memory:  {dense.nbytes} bytes")
print(f"Sparse matrix memory: {sparse_mat.data.nbytes + sparse_mat.indices.nbytes + sparse_mat.indptr.nbytes} bytes")
print(f"Sparsity: {(dense == 0).sum() / dense.size * 100:.0f}% zeros")

# Create a large sparse random matrix
rows, cols = 1000, 1000
density = 0.01  # 1% non-zero
large_sparse = sparse.random(rows, cols, density=density, format="csr")
print(f"\nLarge sparse matrix ({rows}x{cols}):")
print(f"  Non-zero elements: {large_sparse.nnz} / {rows*cols}")
print(f"  Memory saved vs dense: ~{(1 - density) * 100:.0f}%")

# Sparse matrix operations
vec = np.random.randn(cols)
result = large_sparse @ vec  # Sparse matrix-vector multiply
print(f"  Sparse mat-vec result shape: {result.shape}")
print(f"  Result mean: {result.mean():.4f}")

# ============================================================
# Example 4: Basic Linear Algebra with SciPy
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Linear Algebra Basics")
print("=" * 60)

from scipy import linalg

# Solve a system of linear equations: Ax = b
A = np.array([
    [3, 1, -1],
    [1, 4, 2],
    [-1, 2, 5],
])
b = np.array([1, 2, 3])

x = linalg.solve(A, b)
print("Solving Ax = b:")
print(f"  A = \n{A}")
print(f"  b = {b}")
print(f"  x = {x}")

# Verify solution
print(f"  A @ x = {A @ x}  (should equal b = {b})")

# Matrix determinant and inverse
det = linalg.det(A)
print(f"\nDeterminant of A: {det:.4f}")
print(f"Inverse exists: {abs(det) > 1e-10}")

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = linalg.eig(A)
print(f"\nEigenvalues: {eigenvalues}")

# ============================================================
# Example 5: Quick Statistical Summary
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Quick Statistical Summary")
print("=" * 60)

from scipy import stats

np.random.seed(42)
data = np.random.normal(loc=100, scale=15, size=500)

# Descriptive statistics
desc = stats.describe(data)
print(f"Sample size:     {desc.nobs}")
print(f"Mean:            {desc.mean:.2f}")
print(f"Variance:        {desc.variance:.2f}")
print(f"Skewness:        {desc.skewness:.4f}")
print(f"Kurtosis:        {desc.kurtosis:.4f}")
print(f"Min, Max:        [{desc.minmax[0]:.2f}, {desc.minmax[1]:.2f}]")

# Confidence interval for the mean
ci = stats.t.interval(0.95, df=len(data)-1, 
                       loc=np.mean(data), 
                       scale=stats.sem(data))
print(f"\n95% CI for mean: [{ci[0]:.2f}, {ci[1]:.2f}]")

print("\n[OK] You're ready to use SciPy!")
print("   Next: 03-basic-functions.py to explore core functions.")
