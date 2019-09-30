#!/usr/bin/env python3

import os, pickle
import pandas as pd
from mf_code import data_selection, colormag_error, Hess, DensityMap
import numpy as np
from astropy.convolution import Gaussian2DKernel

def dist_modulus(M,d):
    import numpy as np

    return 5.0*np.log10(d)-5.0+M

## List of data files
cat_path = "catalogues"

#check which files have already been analized
mf_log = pd.read_table('mf_log.txt', delimiter = '\t')
pending = mf_log.loc[mf_log['Status'] == 'pending', ['Name']]

for obj_name in pending['Name']:

    try:
        print("Analyzing object " + obj_name)

        ## Read parameters
        print("Reading parameters...")
        p_file = obj_name + "_pars"
        import importlib
        import parameters
        p = importlib.import_module('parameters.' + p_file)


        ## Read and apply selection cuts
        print("Applying cuts...")
        data_path = cat_path + '/' + obj_name + ".dat"
        data = data_selection.data_sel(data_path, p.pos, p.mag_key, p.color_key,
                                       (p.min_mag_cut, p.max_mag_cut),
                                       (p.min_color_cut, p.max_color_cut),
                                       sharp = p.sharp, chi = p.chi)

        #calculate error
        err_func2 = 0
        if p.error_function != None: #if error function is predifined
            err_func2 = p.error_function

        else: # error fucntion is calculated from data
            mag = data[p.mag_key]
            color_err = np.sqrt(data[p.color_key[0] + 'err']**2 +
                                data[p.color_key[2] + 'err']**2)

            popt,pcov,err_func = colormag_error.error_func(mag, color_err,
                                                           xlab = p.mag_key,
                                                           ylab = p.color_key)

            err_func2 = lambda x: err_func(x, *popt)

        ## Select star clusters and
        data_mask = data[data['rd'] < p.cl_rad]

        ## Creation of 2D density for cluster stars
        print("----------------------")
        print("Creating cluster 2D distribution...")
        cl = Hess.Hess(obj_name, data_mask, p.mag_key, p.color_key,
                       (p.min_mag, p.max_mag), (p.min_color, p.max_color),
                       p.delta_mag_gs, p.delta_color_gs, normed = True)

        mag_err = data_mask[p.mag_key + 'err']
        color_err = np.sqrt(data_mask[p.color_key[0]+'err']**2 +
                            data_mask[p.color_key[2]+'err']**2)

        cl.smooth_interp(p.delta_interp_color,
                         p.delta_interp_mag, err_func2, s = p.smooth_cl)

        cl.plot(title = 'cluster', save_plot = True)

        pickle.dump(cl, open( "Results/" + obj_name + "_cl.p", "wb" ))

        ## Creation of 2D background distribution
        print("----------------------")
        print("Creating background 2D distrbution...")

        cond_ra1 = (data['ra'] > p.bkg_ra[0][0]) & (data['ra'] < p.bkg_ra[0][1])
        cond_ra2 = (data['ra'] > p.bkg_ra[1][0]) & (data['ra'] < p.bkg_ra[1][1])
        cond_dec1 = (data['dec'] > p.bkg_dec[0][0]) & (data['dec'] <
                                                       p.bkg_dec[0][1])
        cond_dec2 = (data['dec'] > p.bkg_dec[1][0]) & (data['dec'] <
                                                       p.bkg_dec[1][1])
        cond = (cond_ra1 & cond_dec1) | (cond_ra2 & cond_dec2)

        bkg_stars = data.loc[cond.values, :]

        area1 = (p.bkg_ra[0][1] - p.bkg_ra[0][0]) * (p.bkg_dec[0][1] -
                                                     p.bkg_dec[0][0])
        area2 = (p.bkg_ra[1][1] - p.bkg_ra[1][0]) * (p.bkg_dec[1][1] -
                                                     p.bkg_dec[1][0])
        bkg_area = area1 + area2

        bkg = Hess.Hess(obj_name, bkg_stars, p.mag_key, p.color_key,
                        (p.min_mag, p.max_mag),
                        (p.min_color, p.max_color),
                        p.delta_mag_bkg, p.delta_color_bkg,
                        bkg_area = bkg_area, type_hess = 'bkg')

        bkg.smooth_interp(p.delta_interp_color, p.delta_interp_mag,
                          err_func2, s = p.smooth_bkg,
                          error_factor = p.bkg_error_factor)

        bkg.plot(title = 'bkg', save_plot = True)

        pickle.dump(bkg, open( "Results/" + obj_name + "_bkg.p", "wb" ))

        ##Calculate density map
        print("----------------------")
        ra_bins = np.arange(p.ra_min_alpha,
                            p.ra_max_alpha + p.delta_ra,
                            p.delta_ra)

        dec_bins = np.arange(p.dec_min_alpha,
                             p.dec_max_alpha + p.delta_dec,
                             p.delta_dec)

        density_map = DensityMap.DensityMap(obj_name, cl, bkg, ra_bins,
                                            dec_bins)
        density_map.count_stars(data)

        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(30,20))
        gauss_kernel_size = np.reshape(p.gauss_kernel_size, (2,3))

        for i,row in enumerate(gauss_kernel_size):
            for j,col in enumerate(row):
                kernel = Gaussian2DKernel(col)
                density_map.convolve_interp(kernel, p.delta_interp_ra,
                                            p.delta_interp_dec)

                ## contours
                ax[i,j].set_title(str(col*p.delta_ra*60) + ' arcmin convolution')
                density_map.plot(ax = ax[i,j], pos = p.pos)

        plt.savefig('Results/' + obj_name + '_density_map.pdf')

        ##Bootstrap of density map
        print("----------------------")
        if p.bootstrap:
            cond_ra = (data['ra'] > p.ra_boot_lims[0]) & (data['ra'] <
                                                          p.ra_boot_lims[1])
            cond_dec = (data['dec'] > p.dec_boot_lims[0]) & (data['dec'] <
                                                             p.dec_boot_lims[1])
            data_boot = data.loc[cond_ra & cond_dec, :]

            density_map.bootstrap(cl, bkg, data_boot, p.ra_boot_lims,
                                  p.dec_boot_lims, nboot = p.nboot)
            density_map.plot_bootstrap(save_plot = True)

            pickle.dump(density_map,
                        open( "Results/" + obj_name + "_density_map.p", "wb" ))

        mf_log.loc[mf_log['Name'] == obj_name, 'Status'] = 'Done'
        mf_log.to_csv('mf_log.txt', sep = '\t', index = False)

        print("Analysis of " + obj_name + ' finished.')
        print('\n')
        print('\n')

    except Exception as e:
        print(e)
        print("Analysis of " + obj_name + ' failed. Please check error log.')
        print("Moving to next object...")
        print('\n')

        #save error in log
        error_file = open("error_log.txt", "a")
        error_file.write(obj_name + '\n')
        error_file.write(str(e) + '\n')
        error_file.close()
