# -*- coding: utf-8 -*-

import numpy as np
import pywph as pw
import astropy.io.fits as fits

from wph_quijote.wph_syntheses.wph_operator_wrapper import WPHOp_quijote

M, N = 256, 256
J = 6
L = 8
dn = 2
norm = "auto"

data = fits.open('data/Q_1.fits')[0].data[::2, ::2] + 1j*fits.open('data/U_1.fits')[0].data[::2, ::2]

for norm in [None, "auto"]:
    wph_op = pw.WPHOp(M, N, J, L=L, dn=dn, device=0)
    wph_pywph = wph_op(data, norm=norm, ret_wph_obj=True)
    wph_op.to("cpu")
    
    stat_params = {"J": J, "L": L, "delta_j": J - 1, "delta_l": 4, "delta_n": dn,
                   "scaling_function_moments": [0, 1, 2, 3], "nb_chunks": 15}
    wph_quijote_op = WPHOp_quijote(M, N, stat_params)
    wph_quijote = wph_quijote_op.apply(data, norm=norm)
    wph_quijote_op.stat_op.cpu()

    assert np.allclose(wph_pywph.wph_coeffs, wph_quijote.wph)
    assert np.allclose(wph_pywph.sm_coeffs, wph_quijote.wph_lp)