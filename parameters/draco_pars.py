## Magnitudes and Color keys
obj_name = "draco"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=18.5
max_mag_cut=25
min_color_cut=-0.5
max_color_cut=1.0
sharp = 1.0
chi = 2

## Obj
obj_radius = 9.37 #half-light radius, arcmin
cluster_distance=76.0e3 #pc
pos = (260.0684, 57.9185)

## Cluster stars distribution
cl_rad = 10 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((258.35, 258.7), (261.4, 261.8))
bkg_dec = ((57.1, 58.75), (57.1, 58.75))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 2

## Counting stars
delta_ra = 1.0/60 #degrees
delta_dec = 1.0/60 #degrees
ra_min_alpha_center = -0.9
ra_max_alpha_center = 0.9
dec_min_alpha_center = -0.9
dec_max_alpha_center = 0.9 #all in degrees
contour_levels = [1, 2, 3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
