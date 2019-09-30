def apply_mask (df, isoc_mag1, isoc_mag2, mag_key = 'g', color_key = 'g-r',
                err_cols = ('gerr', 'rerr'), save_plot = False, obj_name = ''):

    import numpy as np
    from scipy import interpolate
    from astropy.io import ascii
    from matplotlib import pyplot as plt
    from mf_code import colormag_error
    import importlib
    importlib.reload(colormag_error)

    color_keys = color_key.split('-')
    color = df[color_keys[0]] - df[color_keys[1]]
    mag = df[mag_key]
    color_err = np.sqrt(df[err_cols[0]]**2 + df[err_cols[1]]**2)

    popt,pcov,err_func = colormag_error.error_func(mag, color_err,
                                    xlab = mag_key, ylab = color_key, plot = True)

    err_func2 = lambda x: err_func(x, *popt)

    ##mask creation
    isoc_color = isoc_mag1 - isoc_mag2
    lim = 4.0
    delta_color = lim*err_func2(isoc_mag1)
    isoc_min_color = isoc_color - delta_color
    isoc_max_color = isoc_color + delta_color

    msto_mag = 21.5
    delta_mag = np.copy(delta_color)
    delta_mag[isoc_mag1 > msto_mag] = 0
    isoc_min_mag = isoc_mag1 - delta_mag
    isoc_max_mag = isoc_mag1 + delta_mag

    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon

    cmd_points = zip(mag,color)
    polygon_points_min = sorted(zip(isoc_min_mag, isoc_min_color))
    polygon_points_max = sorted(zip(isoc_max_mag, isoc_max_color),
                                reverse = True)
    polpoints = polygon_points_min + polygon_points_max
    polygon = Polygon(polpoints)

    isinside = list(map(lambda p: polygon.contains(Point(p)), cmd_points))
    df_cut = df.loc[isinside, :]


    #Plot applied mask
    color = df[color_keys[0]] - df[color_keys[1]]
    mag = df[mag_key]
    plt.figure(figsize=(10,10))
    plt.plot(color,mag,ls='none',marker='o',ms=2)
    plt.plot(isoc_color,isoc_mag1)
    plt.plot(isoc_min_color,isoc_min_mag,color='red')
    plt.plot(isoc_max_color,isoc_max_mag,color='red')
    plt.xlim(min(color), max(color))
    plt.ylim(min(mag), max(mag))
    plt.gca().invert_yaxis()
    plt.ylabel(mag_key)
    plt.xlabel('{}'.format(color_key))
    plt.title('Stars selected by isochrone mask')

    if save_plot:
        plt.savefig('Results/' + obj_name + '_mask.pdf')
    else:
        plt.show()

    return df_cut, popt, err_func2
