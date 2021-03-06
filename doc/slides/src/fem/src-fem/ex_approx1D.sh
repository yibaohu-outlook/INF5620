#!/bin/sh -x

python ex_approx1D.py run_Lagrange_interp_poly 2 2
python ex_approx1D.py run_quadratic_interp_parabola

python ex_approx1D.py run_Lagrange_interp_abs 11
python ex_approx1D.py run_Lagrange_interp_abs_Cheb 11
doconce combine_images Lagrange_basis_12.png Lagrange_basis_Cheb_12.png Lagrange_basis_unif_Cheb_12.png
doconce combine_images Lagrange_basis_12.pdf Lagrange_basis_Cheb_12.pdf Lagrange_basis_unif_Cheb_12.pdf

python ex_approx1D.py run_Lagrange_interp_abs 7
python ex_approx1D.py run_Lagrange_interp_abs 14 -3.5 2

doconce combine_images Lagrange_interp_abs_8.pdf Lagrange_interp_abs_15.pdf Lagrange_interp_abs_8_15.pdf
doconce combine_images Lagrange_interp_abs_8.png Lagrange_interp_abs_15.png Lagrange_interp_abs_8_15.png

python ex_approx1D.py run_Lagrange_interp_abs_Cheb 7
python ex_approx1D.py run_Lagrange_interp_abs_Cheb 14

doconce combine_images Lagrange_interp_abs_Cheb_8.pdf Lagrange_interp_abs_Cheb_15.pdf Lagrange_interp_abs_Cheb_8_15.pdf
doconce combine_images Lagrange_interp_abs_Cheb_8.png Lagrange_interp_abs_Cheb_15.png Lagrange_interp_abs_Cheb_8_15.png

python ex_approx1D.py run_Lagrange_interp_sin 3
python ex_approx1D.py run_Lagrange_leastsq_sin 3
doconce combine_images Lagrange_ls_sin_4.pdf Lagrange_interp_sin_4.pdf Lagrange_ls_interp_sin_4.pdf
doconce combine_images Lagrange_ls_sin_4.png Lagrange_interp_sin_4.png Lagrange_ls_interp_sin_4.png

python ex_approx1D.py run_linear_leastsq_parabola
python ex_approx1D.py run_linear_interp1_parabola
python ex_approx1D.py run_linear_interp2_parabola
doconce combine_images parabola_interp1_linear.pdf parabola_interp2_linear.pdf parabola_inter.pdf
doconce combine_images parabola_interp1_linear.png parabola_interp2_linear.png parabola_inter.png

python ex_approx1D.py run_sines_leastsq_parabola help=False
python ex_approx1D.py run_sines_leastsq_parabola help=True

doconce combine_images parabola_ls_sines4.pdf parabola_ls_sines12.pdf parabola_ls_sines4_12.pdf
doconce combine_images parabola_ls_sines4.png parabola_ls_sines12.png parabola_ls_sines4_12.png
doconce combine_images parabola_ls_sines4_wfterm.pdf parabola_ls_sines12.pdf parabola_ls_sines4_12_wfterm.pdf
doconce combine_images parabola_ls_sines4_wfterm.png parabola_ls_sines12.png parabola_ls_sines4_12_wfterm.png

# This one takes time:
#python approx1D.py run_Lagrange_leastsq_abs 8






