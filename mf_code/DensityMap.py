class DensityMap:

    def __init__(self, obj_name, cl, bkg, ra_lims, dec_lims,
                 delta_ra, delta_dec):

        import numpy as np

        #determine cmd of all stars per solid angle
        self.obj_name = obj_name
        self.ra_delta = delta_ra
        self.dec_delta = delta_dec

        self.ra_bins = np.arange(ra_lims[0],ra_lims[1] + self.ra_delta,
                                 self.ra_delta)
        self.dec_bins = np.arange(dec_lims[0], dec_lims[1] + self.dec_delta,
                                  self.dec_delta)

        self.cl = cl.hess_interp
        self.bkg = bkg.hess_interp
        self.delta_interp_mag = cl.delta_mag_interp
        self.delta_interp_color = cl.delta_color_interp
        self.mag_key = cl.mag_key
        self.color_key = cl.color_key
        self.mag_bins_interp = cl.mag_bins_interp
        self.color_bins_interp = cl.color_bins_interp

        self.total_bins = (len(self.ra_bins) - 1)*(len(self.dec_bins) - 1)
        self.alpha = np.zeros((len(self.dec_bins) - 1, len(self.ra_bins) - 1))

    def count_stars(self, df, df_ra = 'ra', df_dec = 'dec'):

        import numpy as np
        from tqdm import tqdm

        H_cl = self.cl
        H_bs = self.bkg*self.ra_delta*self.dec_delta
        delta_mag = self.delta_interp_mag
        delta_color = self.delta_interp_color

        int1 = np.sum(H_cl*delta_mag*delta_color)
        int2 = np.sum((H_cl**2/H_bs)*delta_mag*delta_color)

        print("Counting cluster stars...")

        with tqdm(total=self.total_bins, unit='Bin') as pbar:

            dec_bins = self.dec_bins
            ra_bins = self.ra_bins

            for i in range(len(dec_bins) - 1):
                for j in range(len(ra_bins) - 1):
                    cond_ra = (df[df_ra] >= ra_bins[j]) & (df[df_ra] <= ra_bins[j+1])
                    cond_dec = (df[df_dec] >= dec_bins[i]) & (df[df_dec] <= dec_bins[i+1])
                    df_sel = df.loc[cond_ra & cond_dec, :]

                    mag = np.array(df_sel[self.mag_key])
                    color = np.array(df_sel[self.color_key])
                    H_all,_,_ = np.histogram2d(mag,color,
                                               bins=(self.mag_bins_interp,
                                                     self.color_bins_interp))

                    if np.greater(np.unique(H_all), 1).any():
                        print("Warning. More than one star per bin.")
                        print(np.max(np.unique(H_all)))


                    self.alpha[i,j] = (np.sum((H_cl/H_bs)*H_all) - int1)/int2

                    pbar.update()

        print("Finished")

        #mask less than zero values in alpha
        less_0 = self.alpha < 0
        self.alpha[less_0] = 0

    def convolve_interp(self, kernel, nclip = 3):

        from astropy.convolution import convolve
        from scipy import interpolate
        import numpy as np
        self.alpha_conv = convolve(self.alpha, kernel)

        #calculate sigma and mean for alpha bkg
        size = np.shape(self.alpha_conv)[0]*np.shape(self.alpha_conv)[1]
        aux = np.reshape(self.alpha_conv, size)

        #sigma clipping
        import matplotlib.pyplot as plt
        if nclip != 0:
            #from astropy.stats import sigma_clip
            #aux = sigma_clip(aux, nclip)
            #self.alpha_bkg_mean = np.mean(aux[~aux.mask])
            #self.alpha_bkg_sigma = np.std(aux[~aux.mask])

            from sklearn.mixture import GaussianMixture
            model = GaussianMixture(2)
            X = np.reshape(aux,(size,1))
            model.fit(X)
            self.alpha_bkg_mean = model.means_[0][0]
            self.alpha_bkg_sigma = np.sqrt(model.covariances_[0][0][0])

            plt.figure()
            #plt.hist(aux[~aux.mask], bins = 30)
            plt.hist(aux, bins = 30)
            plt.show()

        else:
            from sklearn.mixture import GaussianMixture
            model = GaussianMixture(1)
            X = np.reshape(aux,(size,1))
            model.fit(X)
            print(model.means_)
            print(model.covariances_)
            self.alpha_bkg_mean = model.means_[0][0]
            self.alpha_bkg_sigma = np.sqrt(model.covariances_[0][0][0])

            plt.figure()
            plt.hist(aux, bins = 30)
            plt.show()


    def plot(self, contour_levels,
             pos = (0,0), save_plot = False,
             save_path = '~',
             name = None):

        from matplotlib import pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize = (11,11))

        #ra_bins = (self.ra_bins - pos[0])*np.cos(np.pi*pos[1]/180.)
        #dec_bins = (self.dec_bins - pos[1])
        ra_bins = self.ra_bins
        dec_bins = self.dec_bins

        sigma = self.alpha_bkg_sigma
        mean = self.alpha_bkg_mean

        ax.imshow((self.alpha_conv-mean)/sigma,
                   extent = [ra_bins[0], ra_bins[-1],
                             dec_bins[-1], dec_bins[0]],
                   aspect = 1.0,
                   cmap = 'Greys')

        c = contour_levels

        cs = ax.contour((self.alpha_conv-mean)/sigma,
                        levels=c,
                        extent = [ra_bins[0], ra_bins[-1],
                                  dec_bins[0], dec_bins[-1]])

        #cb = fig.colorbar(cs, ticks = c)
        labels = c
        for i in range(len(labels)):
            cs.collections[i].set_label(labels[i])

        label_size=21
        tick_size=19
        legend_font_size = 12

        ax.legend(loc='upper left', title = 'Sigma level',
            fontsize = legend_font_size, title_fontsize = legend_font_size)

        ax.set_xlabel('RA (degrees)', fontsize=label_size)
        ax.set_ylabel('DEC (degrees)', fontsize=label_size)
        ax.tick_params(axis='both',labelsize=tick_size)
        ax.invert_xaxis()
        ax.invert_yaxis()

        #plot Milky Way center arrow
        ra_mw = (266.41683333 - pos[0])*np.cos(np.pi*pos[1]/180.)
        dec_mw = -29.00780556 - pos[1]

        import math
        ang = math.atan(dec_mw/ra_mw) #in radians
        #draw arrow
        r = abs(ra_bins[1]-ra_bins[-1])/12
        plt.arrow(min(ra_bins)+r,max(dec_bins)-r,r*math.cos(ang),
        r*math.sin(ang), color = 'r',head_width = 0.2*r)

        #add name of object
        if name != None:
            plt.text(0.5, 0.9, name, horizontalalignment='center',
                     verticalalignment = 'center',
                     transform=ax.transAxes, fontsize = label_size)

        #save figure
        if save_plot:
            plt.savefig(save_path + self.obj_name + '_alpha.pdf')

    def bootstrap(self, cl, bkg, df, ra_boot_lims, dec_boot_lims, nboot = 9,
                  df_ra = 'ra', df_dec = 'dec', method = "sample"):

        from astropy.stats import bootstrap
        import numpy as np

        if method == 'sample':
            radec = np.array(list(zip(df[df_ra], df[df_dec])))
            radec_boot = bootstrap(radec, bootnum = nboot)

        self.boot_dict = {}
        self.ra_boot_lims = ra_boot_lims
        self.dec_boot_lims = dec_boot_lims

        for i in range(nboot):
            print("Counting stars for bootstrap " + str(i+1) + ' of ' +
                  str(nboot))

            data_aux = df.copy()

            if method == "sample":
                data_aux.loc[:,df_ra] = radec_boot[i][:,0]
                data_aux.loc[:,df_dec] = radec_boot[i][:,1]

            elif method == "uniform":
                ra_aux = np.random.uniform(low = ra_boot_lims[0],
                                           high = ra_boot_lims[1],
                                           size = len(df))
                dec_aux = np.random.uniform(low = dec_boot_lims[0],
                                            high = dec_boot_lims[1],
                                            size = len(df))

                data_aux.loc[:,df_ra] = ra_aux
                data_aux.loc[:,df_dec] = dec_aux


            density_map_boot = DensityMap(self.obj_name, cl, bkg,
                                          ra_boot_lims, dec_boot_lims,
                                          self.ra_delta, self.dec_delta)

            density_map_boot.count_stars(data_aux)

            self.boot_dict['boot'+str(i+1)] = density_map_boot

    def bootstrap_convolve_interp(self, kernel, nclip = 0):

        boot_dict_aux = self.boot_dict.copy()

        for i, density_map_boot in boot_dict_aux.items():

            density_map_boot.convolve_interp(kernel, nclip = nclip)

            self.boot_dict[i] = density_map_boot

    def plot_bootstrap(self, contour_levels, pos = (0,0), save_plot = False, save_path = '~'):

        ##plot bootstrap Results
        from matplotlib import pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(nrows=3, ncols=3, figsize = (11,11), sharex=True, sharey=True)

        k=0
        j=0
        #nboot = len(self.boot_dict)
        for i,d in self.boot_dict.items():
            #ax = fig.add_subplot(2,nboot/2,sp)

            ra_bins = np.arange(self.ra_boot_lims[0],
                                self.ra_boot_lims[1] + self.ra_delta,
                                self.ra_delta)
            dec_bins = np.arange(self.dec_boot_lims[0],
                                 self.dec_boot_lims[1] + self.dec_delta,
                                 self.dec_delta)

            #ra_bins = (ra_bins - pos[0])*np.cos(np.pi*pos[1]/180.)
            #dec_bins = (dec_bins - pos[1])

            import matplotlib as mpl
            norm = mpl.colors.Normalize(vmin=np.min(d.alpha_conv),vmax=np.max(d.alpha_conv))
            ax[k][j].imshow(d.alpha_conv,
                      extent = [ra_bins[0], ra_bins[-1],
                                dec_bins[-1], dec_bins[0]],
                      aspect = 1.0,
                      cmap = 'Greys_r',
                      norm = norm)

            mean = d.alpha_bkg_mean
            sigma = d.alpha_bkg_sigma

            #countours
            c = contour_levels

            cs = ax[k][j].contour((d.alpha_conv-mean)/sigma,
                            levels=c,
                            vmax = c[-1],
                            vmin = c[0],
                            extent = [ra_bins[0], ra_bins[-1],
                                      dec_bins[0], dec_bins[-1]])

            #fig.colorbar(cs, extend = 'both', cax = ax)ç
            #labels = c
            #for i in range(len(labels)):
            #    cs.collections[i].set_label(labels[i])

            label_size=21
            tick_size=19
            legend_font_size = 12

            #ax[k][j].legend(loc='upper left', title = 'Sigma level',fontsize = legend_font_size, title_fontsize = legend_font_size)

            ax[k][j].tick_params(axis='both',labelsize=tick_size)

            if j==0:
                ax[k][j].set_ylabel('DEC (degrees)', fontsize=label_size)
            if k==2:
                ax[k][j].set_xlabel('RA (degrees)', fontsize=label_size)

            ax[k][j].invert_xaxis()
            ax[k][j].invert_yaxis()
            j+=1
            if j==3:
                j=0
                k+=1

        #plt.tight_layout()
        plt.subplots_adjust(hspace=0.05, wspace = 0.05)

        if save_plot:
            plt.savefig(save_path + self.obj_name + '_boot.pdf')

        plt.show()

        ##median
        '''median_alpha = []
        for v in self.boot_dict.values():
            median_alpha.append(v.alpha_interp)

        self.boot_median_alpha = np.mean(median_alpha, axis=0)
        ra_bins = np.arange(self.ra_boot_lims[0],
                            self.ra_boot_lims[1] + self.ra_delta,
                            self.ra_delta)
        dec_bins = np.arange(self.dec_boot_lims[0],
                             self.dec_boot_lims[1] + self.dec_delta,
                             self.dec_delta)
        ra_bins = (ra_bins - pos[0])*np.cos(np.pi*pos[1]/180.)
        dec_bins = (dec_bins - pos[1])

        fig = plt.figure(figsize = (10,5))
        plt.imshow(self.boot_median_alpha,
                  extent = [ra_bins[0], ra_bins[-1],dec_bins[-1], dec_bins[0]],
                  aspect = 1.0,
                  cmap = 'Greys')

        size = np.shape(self.boot_median_alpha)[0]*np.shape(self.boot_median_alpha)[1]
        aux = np.reshape(self.boot_median_alpha, size)

        from astropy.stats import sigma_clip
        aux = sigma_clip(aux, nclip)
        mean = np.mean(aux[~aux.mask])
        sigma = np.std(aux[~aux.mask])

        #countours
        c = np.array([3, 4, 5, 6, 7, 10, 15, 20])*sigma + mean

        plt.contour(self.boot_median_alpha,
                   levels=c,
                   extent = [ra_bins[0], ra_bins[-1],
                             dec_bins[0], dec_bins[-1]])

        plt.xlabel('ra')
        plt.ylabel('dec')
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.show()'''
