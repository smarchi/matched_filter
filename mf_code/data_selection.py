def data_sel(data_path, obj_pos, mag_key, color_key,
             mag_lims, color_lims, sharp = 1, chi = 2):

    import pandas as pd
    import numpy as np
    #keys = ["id", "ra", "dec", "g", "gerr", "r", "rerr", "chi", "sharp", "rd",
    #        "l", "b", "egr", "ag", "ar"]
    keys = ["id", "ra", "dec", "g", "gerr", "r", "rerr", "chi", "sharp"]

    data = pd.read_table(data_path, delimiter="\s+", header=None)
    data.columns = keys

    data['g-r'] = data['g'] - data['r']

    data['rd'] = np.sqrt((data['ra'] - obj_pos[0])**2 + (data['dec'] - obj_pos[1])**2)*60

    min_mag_cut = mag_lims[0]
    max_mag_cut = mag_lims[1]
    min_color_cut = color_lims[0]
    max_color_cut = color_lims[1]

    cond_color = (data[color_key] <= max_color_cut) & (data[color_key] >=
                                                       min_color_cut)

    cond_mag = (data[mag_key] >= min_mag_cut) & (data[mag_key] <= max_mag_cut)
    cond_sharp = abs(data['sharp'] <= sharp)
    cond_chi = data['chi'] < chi

    return data.loc[cond_color & cond_mag & cond_sharp & cond_chi, :]
