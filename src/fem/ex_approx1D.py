"""
Examples on approximating functions by global basis functions,
using the least_squares_1D.py module.
"""
from approx1D import *
from Lagrange import *
from scitools.std import figure
import sympy as sm
import sys
x = sm.Symbol('x')


def sines(x, N):
    return [sm.sin(sm.pi*(i+1)*x) for i in range(N+1)]

def cosines(x, N):
    return [sm.cos(sm.pi*i*x) for i in range(N+1)]

def sines_cosines(x, N):
    c = [sm.cos(sm.pi*i*x) for i in range(N+1)]
    s = [sm.sin(sm.pi*i*x) for i in range(1, N+1)]
    return c + s

def taylor(x, N):
    return [x**i for i in range(N+1)]


# ----------------------------------------------------------------------

def run_linear():
    f = 10*(x-1)**2 - 1
    phi = [1, x]
    Omega = [1, 2]
    u = least_squares(f, phi, Omega)
    comparison_plot(f, u, Omega, 'parabola_ls_linear.eps')

def run_linear2(N=2):
    """
    Test Taylor approx to a parabola and exact symbolics vs
    ill-conditioned numerical approaches.
    """
    f = 10*(x-1)**2 - 1
    u = least_squares(f, phi=[x**i for i in range(N+1)], Omega=[1, 2])
    # Note: in least_squares there is extra code for numerical solution
    # of the systems
    print 'f:', sm.expand(f)
    print 'u:', sm.expand(u)
    comparison_plot(f, u, [1, 2], 'parabola_ls_taylor%d.eps' % N)

def run_sines(help=False):
    for N in (4, 12):
        f = 10*(x-1)**2 - 1
        phi = sines(x, N)
        Omega = [0, 1]
        if help:  # u = 9 + sum
            u = 9 + least_squares_orth(f-9, phi, Omega)
        else:
            u = least_squares_orth(f, phi, Omega)
        figure()
        comparison_plot(f, u, Omega, 'parabola_ls_sines%d.eps' % N)


def run_sine_by_powers(N):
    f = sm.sin(x)
    phi = taylor(x, N)
    Omega=[0, 2*sm.pi]
    u = least_squares(f, phi, Omega)
    comparison_plot(f, u, Omega)

def run_Lagrange_poly(N):
    # Test of symbolic and numeric evaluation of Lagrange polynomials
    phi, points = Lagrange_polynomials_01(x, N)
    print phi
    print points
    x = 0.5
    phi, points = Lagrange_polynomials_01(x, N)
    print phi
    print points


def run_Lagrange_sin(N):
    # Least-squares use of Lagrange polynomials
    f = sm.sin(2*sm.pi*x)
    phi, points = Lagrange_polynomials_01(x, N)
    Omega=[0, 1]
    u = least_squares(f, phi, Omega)
    comparison_plot(f, u, Omega, filename='Lagrange_ls_sin_%d.eps' % (N+1),
                    plot_title='Least squares approximation by '\
                    'Lagrange polynomials of degree %d' % N)

def run_Lagrange_abs(N):
    """Least-squares with of Lagrange polynomials for |1-2x|."""
    f = sm.abs(1-2*x)
    # This f will lead to failure of sympy integrate, fallback on numerical int.
    phi, points = Lagrange_polynomials_01(x, N)
    Omega=[0, 1]
    u = least_squares(f, phi, Omega)
    comparison_plot(f, u, Omega, filename='Lagrange_ls_abs_%d.eps' % (N+1),
                    plot_title='Least squares approximation by '\
                    'Lagrange polynomials of degree %d' % N)

def run_linear_interpolation1():
    f = 10*(x-1)**2 - 1
    phi = [1, x]
    Omega = [1, 2]
    points = [1 + sm.Rational(1,3), 1 + sm.Rational(2,3)]
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega, 'parabola_interp1_linear.eps')


def run_linear_interpolation2():
    f = 10*(x-1)**2 - 1
    phi = [1, x]
    Omega = [1, 2]
    points = [1, 2]
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega, 'parabola_interp2_linear.eps')


def run_poly_interp_sin(N):
    f = sm.sin(sm.pi*x)
    phi = taylor(x, N)
    Omega = [1, 2]
    import numpy as np
    points = np.linspace(1, 2, N+1)
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega, 'sin_interp_poly%d.eps' % N)


def run_Lagrange_interp_sin(N):
    f = sm.sin(2*sm.pi*x)
    phi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_sin_%d.eps' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N)

def run_Lagrange_interp_poly(n, N):
    f = x**n
    phi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_p%d_%d.eps' % (n, N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N)

def run_Lagrange_interp_abs(N, ymin=None, ymax=None):
    f = abs(1-2*x)
    phi, points = Lagrange_polynomials_01(x, N)
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_abs_%d.eps' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N, ymin=ymin, ymax=ymax)
    # Make figures of Lagrange polynomials (phi)
    figure()
    xcoor = linspace(0, 1, 1001)
    for i in (2, (N+1)/2+1):
        fn = lambdify([x], phi[i])
        ycoor = fn(xcoor)
        plot(xcoor, ycoor)
        legend(r'\phi_%d' % i)
        hold('on')
        plot(points, [fn(xc) for xc in points], 'ro')
    #if ymin is not None and ymax is not None:
    #    axis([xcoor[0], xcoor[-1], ymin, ymax])
    savefig('Lagrange_basis_%d.eps' % (N+1))

def run_Lagrange_interp_abs_Cheb(N, ymin=None, ymax=None):
    f = abs(1-2*x)
    phi, points= Lagrange_polynomials(x, N, [0, 1],
                                      point_distribution='Chebyshev')
    u = interpolation(f, phi, points)
    comparison_plot(f, u, Omega=[0, 1],
                    filename='Lagrange_interp_abs_Cheb_%d.eps' % (N+1),
                    plot_title='Interpolation by Lagrange polynomials '\
                    'of degree %d' % N, ymin=ymin, ymax=ymax)

def run_Lagrange_interp_abs_conv(N=[3, 6, 12, 24]):
    f = sm.abs(1-2*x)
    f = sm.sin(2*sm.pi*x)
    fn = lambdify([x], f, modules='numpy')
    resolution = 50001
    import numpy as np
    xcoor = np.linspace(0, 1, resolution)
    fcoor = fn(xcoor)
    Einf = []
    E2 = []
    h = []
    for _N in N:
        phi, points = Lagrange_polynomials_01(x, _N)
        u = interpolation(f, phi, points)
        un = lambdify([x], u, modules='numpy')
        ucoor = un(xcoor)
        e = fcoor - ucoor
        Einf.append(e.max())
        E2.append(np.sqrt(np.sum(e*e/e.size)))
        h.append(1./_N)
    print Einf
    print E2
    print h
    print N
    # Assumption: error = CN**(-N)
    print 'convergence rates:'
    for i in range(len(E2)):
        C1 = E2[i]/(N[i]**(-N[i]/2))
        C2 = Einf[i]/(N[i]**(-N[i]/2))
        print N[i], C1, C2
    # Does not work properly...


if __name__ == '__main__':
    functions = \
        [eval(fname) for fname in dir() if fname.startswith('run_')]
    from scitools.misc import function_UI
    cmd = function_UI(functions, sys.argv)
    eval(cmd)
