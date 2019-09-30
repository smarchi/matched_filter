class Hess(object):
    """
    A class for creating a Color-Magnitude Diagram (CMD) for member and background
    stars.

    Attributes
    ----------
    obj_name: str
        Name of the object
    type: str
        Specifies if the CMD is for the member ('cl') or  background ('bkg')
        stars.
    mag_key: str
        Magnitude key for extracting data from database. Example: 'g'
    color_key: str
        Color key for extracting data from database. Example: 'g-r'
    delta_mag: float
        Initial bin size for magnitude axis
    delta_color: float
        Initial bin size for color axis
    mag_bins: numpy 1D array
        Initial magnitude bin limits
    color_bins: numpy 1D array
        Initial color bin limits
    delta_mag_interp: float
        Interpolation bin size for magnitude
    delta_color_interp: float
        Interpolation bin size for color
    mag_bins_interp: numpy 1D array
        Interpolation bin limits for magnitude
    color_bins_interp: numpy 1D array
        Interpolation bin limits for color
    area: float
        If type = 'bkg', area occupied by background. By default is None.
    hess: numpy 2D array
        Hess diagram.

    Methods
    -------
    smooth_interp(delta_interp_color, delta_interp_mag, new_color_bins,
                    new_mag_bins, err_func, s = 0, error_factor = 1,
                    boxsize = 1, kx = 1, ky = 1, method = '1D')
        Smooths and interpolates the original CMD.

    plot(self, title = '', save_plot = False, save_path = '~'):
        Plots the CMD.
    """

    def __init__(self, obj_name, data, mag_key, color_key, mag_lims, color_lims,
                 delta_mag, delta_color, normed = False, type_hess = 'cl',
                 bkg_area = None):

        """
        Parameters
        ----------
        obj_name: str
            Name of the object
        data: Pandas dataframe
            Dataframe thta contains the magnitude and color of each star.
        mag_key: str
            Magnitude key for extracting data from database. Example: 'g'
        color_key: str
            Color key for extracting data from database. Example: 'g-r'
        mag_lims: tuple
            Contains the minimum and maximum magnitude values to use when
            building the CMD.
        color_lims: tuple
            Contains the minimum and maximum color values to use when building
            the CMD.
        delta_mag: float
            Initial bin size for magnitude axis
        delta_color: float
            Initial bin size for color axis
        normed: boolean
            If True normalizes the CMD. If False, do nothing. Default is False.
        type_hess: str
            Specifies if the CMD is for the member ('cl') or  background ('bkg')
            stars.
        bkg_area: float
            If type = 'bkg', area occupied by background. Default is None.
        """

        import numpy as np

        #Attributes to be used later
        self.obj_name = obj_name
        self.type = type_hess
        self.mag_key = mag_key
        self.color_key = color_key

        self.mag_bins = np.arange(mag_lims[0],mag_lims[1]+delta_mag,delta_mag)
        self.color_bins = np.arange(color_lims[0],color_lims[1]+delta_color,
                                  delta_color)
        self.delta_mag = delta_mag
        self.delta_color = delta_color

        mag = data[mag_key]
        color = data[color_key]

        #generate Hess diagram
        H,junk,junk=np.histogram2d(mag,color,
                                   bins = (self.mag_bins,self.color_bins),
                                   normed = normed)

        #if it is background cmd, normalize bins by area to have number density
        #per square degree
        if self.type == 'bkg':
            self.area = bkg_area
            self.hess = H/bkg_area

        #if it is object cmd, do not normalize by area.
        elif self.type == 'cl':
            self.hess = H

    def smooth_interp(self, delta_interp_color, delta_interp_mag,
                      new_color_bins, new_mag_bins, err_func, s = 0,
                      error_factor = 1, boxsize = 1, kx = 1, ky = 1,
                      method = '1D'):

        """
        Parameters
        ----------
        delta_interp_color: float
            Interpolation bin size color
        delta_interp_mag: float
            Interpolation bin size magnitude
        new_color_bins: numpoy 1D array
            Interpolation bin limits for color
        new_mag_bins: numpoy 1D array
            Interpolation bin limits for magnitude
        err_func: function
            Relates magnitude (independent variable) with color error (response).
        s: integer
            ???. Default is 0.
        error_factor: float
            Factor that amplifies effect of error when doing convolution.
        boxsize: integer
            Defines the number of rows when building 1D portion for convolution.
            Only valid when method = 1D.
        kx: integer
            ???
        ky: integer
            ???
        method: str
            Defines the method to use for convolution. '1D' first divides the
            magnitude axis in portions and apply a 2D convolution on them using
            kernels of different size for each case. '2D' uses a single 2D
            kernel over the entire CMD.
        """

        import numpy as np

        mag_points = (self.mag_bins[0:-1] + self.mag_bins[1:])*0.5

        err_col = np.sqrt(2*err_func(mag_points)**2)
        err_col_size = np.ceil(err_col/self.delta_color)*error_factor

        ##Gauss Kernel smoothing
        from astropy.convolution import Gaussian2DKernel, convolve

        H_smooth_aux = np.copy(self.hess)

        if method == '1D':
            for i in range(np.shape(self.hess)[0]):
                kernel = Gaussian2DKernel(x_stddev = err_col_size[i],
                                          y_stddev = err_col_size[i]/np.sqrt(2.))

                try:
                    aux = convolve(H_smooth_aux[i:i+boxsize,:], kernel,
                                   boundary = 'extend')
                    H_smooth_aux[i:i+boxsize,:] = aux
                except:
                    aux = convolve(H_smooth_aux[i:,:], kernel, boundary = 'extend')
                    H_smooth_aux[i:,:] = aux

        elif method == '2D':
            kernel = Gaussian2DKernel(error_factor)
            H_smooth_aux = convolve(H_smooth_aux, kernel)

        H_smooth1d = np.copy(H_smooth_aux)

        ##Interpolation
        from scipy import interpolate

        r = (self.color_bins[0:-1] + self.color_bins[1:]) * 0.5
        m = (self.mag_bins[0:-1] + self.mag_bins[1:]) * 0.5

        H_interp = interpolate.RectBivariateSpline(m,r,H_smooth1d,
                                                     kx = kx,ky = ky,s = s)

        newr = (new_color_bins[0:-1] + new_color_bins[1:]) * 0.5
        newm = (new_mag_bins[0:-1] + new_mag_bins[1:]) * 0.5

        #interpolate
        H_smooth_interp = np.zeros(len(newr)*len(newm)).reshape(len(newm),len(newr))
        for j in range(0,len(newm)):
            for i in range(0,len(newr)):
                H_smooth_interp[j,i] = H_interp.ev(newm[j],newr[i])

        if self.type == 'cl':
            #self.hess_interp = np.ma.masked_less(H_smooth_interp, 0.0)
            self.hess_interp = H_smooth_interp
        elif self.type == 'bkg':
            self.hess_interp = np.ma.masked_less_equal(H_smooth_interp, 0.0)
            #self.hess_interp = H_smooth_interp

        self.mag_bins_interp = new_mag_bins
        self.color_bins_interp = new_color_bins
        self.delta_mag_interp = delta_interp_mag
        self.delta_color_interp = delta_interp_color

    def plot(self, title = '', save_plot = False,
             save_path = '~'):

        """
        Parameters
        ----------
        title: str
            'object' or 'background'. Final title is obj_name + title +
            ' distribution'. Default is ''
        save_plot: boolean.
            If True, save plot. If False, do not save. Default is False
        save_path: str
            Path to save the plot. Default is '~'.
        """

        from matplotlib import pyplot as plt
        import numpy as np

        fig = plt.figure(figsize=(8,8))

        if self.type == 'cl':
            max_contour = np.max(np.log(self.hess_interp))
            c = np.arange(-5,max_contour,0.35)
            plt.contour(np.log(self.hess_interp),
                        levels=c,
                        extent=[self.color_bins[0], self.color_bins[-1],
                                self.mag_bins[0], self.mag_bins[-1]],
                        interpolation='none',aspect=0.1)

        elif self.type == 'bkg':
            max_contour = np.max(self.hess_interp)
            delta_c = max_contour/22.
            c=np.arange(0,max_contour+delta_c,delta_c)
            plt.contour(self.hess_interp,
                        levels=c,
                        extent=[self.color_bins[0], self.color_bins[-1],
                                self.mag_bins[0], self.mag_bins[-1]],
                        interpolation='none',aspect=0.1)

        plt.gca().invert_yaxis()
        #plt.title(self.obj_name + ' ' + title + ' distribution' )
        plt.xlabel(self.color_key)
        plt.ylabel(self.mag_key)

        if save_plot:
            plt.savefig(save_path + self.obj_name + '_' + title +'_dist.pdf')
        else:
            plt.show()
