import numpy as np
import matplotlib.pyplot as plt
import sys
from math import log

def solver(I, a, T, dt, theta):
    """
    Solve u'=-a*u, u(0)=I, for t in (0,T] with steps of dt.


    >>> u, t = solver(I=0.8, a=1.2, T=4, dt=0.5, theta=0.5)
    >>> for t_n, u_n in zip(t, u):
    ...     print 't=%.1f, u=%.14f' % (t_n, u_n)
    t=0.0, u=0.80000000000000
    t=0.5, u=0.43076923076923
    t=1.0, u=0.23195266272189
    t=1.5, u=0.12489758761948
    t=2.0, u=0.06725254717972
    t=2.5, u=0.03621291001985
    t=3.0, u=0.01949925924146
    t=3.5, u=0.01049960113002
    t=4.0, u=0.00565363137770
    """
    dt = float(dt)              # avoid integer division
    N = int(round(T/dt))        # no of time intervals
    T = N*dt                    # adjust T to fit time step dt
    u = np.zeros(N+1)           # array of u[n] values
    t = np.linspace(0, T, N+1)  # time mesh

    u[0] = I                    # assign initial condition
    for n in range(0, N):       # n=0,1,...,N-1
        u[n+1] = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)*u[n]
    return u, t

def verify_three_steps():
    """
    Run three steps and compare with pre-computed correct values.
    Return True if the computations are right.
    """
    theta = 0.8; a = 2; I = 0.1; dt = 0.8
    factor = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)
    u1 = factor*I
    u2 = factor*u1
    u3 = factor*u2

    N = 3  # number of time steps
    u, t = solver(I=I, a=a, T=N*dt, dt=dt, theta=theta)

    tol = 1E-15  # tolerance for comparing floats
    difference = abs(u1-u[1]) + abs(u2-u[2]) + abs(u3-u[3])
    success = difference <= tol
    return success

def verify_exact_discrete_solution():
    """
    Compare the solution computed by solver
    with a formula for the exact discrete solution.
    Return True if the computations are right.
    """

    def exact_discrete_solution(n, I, a, theta, dt):
        factor = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)
        return I*factor**n

    theta = 0.8; a = 2; I = 0.1; dt = 0.8
    N = int(8/dt)  # no of steps
    u, t = solver(I=I, a=a, T=N*dt, dt=dt, theta=theta)
    u_de = np.array([exact_discrete_solution(n, I, a, theta, dt)
                     for n in range(N+1)])
    difference = np.abs(u_de - u).max()  # max deviation
    tol = 1E-15  # tolerance for comparing floats
    success = difference <= tol
    return success

def exact_solution(t, I, a):
    return I*np.exp(-a*t)

def explore(I, a, T, dt, theta=0.5, makeplot=True):
    """
    Run a case with the solver, compute error measure,
    and plot the numerical and exact solutions (if makeplot=True).

    >>> for theta in 0, 0.5, 1:
    ...    E = explore(I=1.9, a=2.1, T=5, dt=0.1, theta=theta,
    ...                makeplot=False)
    ...    print '%.10E' % E
    ...
    7.3565079236E-02
    2.4183893110E-03
    6.5013039886E-02
    """
    u, t = solver(I, a, T, dt, theta)  # Numerical solution
    u_e = exact_solution(t, I, a)
    e = u_e - u
    E = np.sqrt(dt*np.sum(e**2))
    if makeplot:
        plt.figure()                     # create new plot
        t_e = np.linspace(0, T, 1001)    # very fine mesh for u_e
        u_e = exact_solution(t_e, I, a)
        plt.plot(t,   u,   'r--o')       # red dashes w/circles
        plt.plot(t_e, u_e, 'b-')         # blue line for u_e
        plt.legend(['numerical', 'exact'])
        plt.xlabel('t')
        plt.ylabel('u')
        plt.title('Method: theta-rule, theta=%g, dt=%g' % \
                  (theta, dt))
        theta2name = {0: 'FE', 1: 'BE', 0.5: 'CN'}
        plt.savefig('%s_%g.png' % (theta2name[theta], dt))
        plt.show()
    return E

def define_command_line_options():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--I', '--initial_condition', type=float,
                        default=1.0, help='initial condition, u(0)',
                        metavar='I')
    parser.add_argument('--a', type=float,
                        default=1.0, help='coefficient in ODE',
                        metavar='a')
    parser.add_argument('--T', '--stop_time', type=float,
                        default=3.0, help='end time of simulation',
                        metavar='T')
    parser.add_argument('--makeplot', action='store_true',
                        help='display plot or not')
    parser.add_argument('--dt', '--time_step_values', type=float,
                        default=[0.5], help='time step values',
                        metavar='dt', nargs='+', dest='dt_values')
    return parser

def read_command_line(use_argparse=True):
    """
    Read parameters from the command line and return their
    values as the sequence I, a, T, makeplot, dt_values.

    >>> sys.argv[1:] = '1.2 0.9 4 True 0.1 0.05'.split()
    >>> prms = read_command_line(use_argparse=False)
    >>> print prms
    (1.2, 0.9, 4.0, True, [0.1, 0.05])
    >>> sys.argv[1:] = '--I 1.2 --a 0.9 --T 4 --makeplot '\
                       '--dt 0.1 0.05'.split()
    >>> prms = read_command_line(use_argparse=True)
    >>> print prms
    (1.2, 0.9, 4.0, True, [0.1, 0.05])
    """
    if use_argparse:
        parser = define_command_line_options()
        args = parser.parse_args()
        return args.I, args.a, args.T, args.makeplot, args.dt_values
    else:
        if len(sys.argv) < 6:
            print 'Usage: %s I a on/off dt1 dt2 dt3 ...' % \
                  sys.argv[0]; sys.exit(1)

        I = float(sys.argv[1])
        a = float(sys.argv[2])
        T = float(sys.argv[3])
        makeplot = sys.argv[4] in ('on', 'True')
        dt_values = [float(arg) for arg in sys.argv[5:]]

        return I, a, T, makeplot, dt_values

def main():
    I, a, T, makeplot, dt_values = read_command_line()
    r = {}
    for theta in 0, 0.5, 1:
        E_values = []
        for dt in dt_values:
            E = explore(I, a, T, dt, theta, makeplot=False)
            E_values.append(E)

        # Compute convergence rates
        m = len(dt_values)
        r[theta] = [log(E_values[i-1]/E_values[i])/
                    log(dt_values[i-1]/dt_values[i])
                    for i in range(1, m, 1)]

    for theta in r:
        print '\nPairwise convergence rates for theta=%g:' % theta
        print ' '.join(['%.2f' % r_ for r_ in r[theta]])
    return r

def verify_convergence_rate():
    """
    Compute empirical convergence rates and compare with
    the expected ones. Return True if they are within a
    tolerance of 0.1.
    """
    r = main()
    tol = 0.1
    expected_rates = {0: 1, 1: 1, 0.5: 2}
    for theta in r:
        r_final = r[theta][-1]
        diff = abs(expected_rates[theta] - r_final)
        if diff > tol:
            return False
    return True  # all tests passed

if __name__ == '__main__':
    main()
