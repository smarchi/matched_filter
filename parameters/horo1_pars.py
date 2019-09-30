## Magnitudes and Color keys
obj_name = "horo1"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=21
max_mag_cut=23.5
min_color_cut=-0.2
max_color_cut=0.65
sharp = 1.0
chi = 2

## Obj
obj_radius = 1.54 #half-light radius, arcmin
cluster_distance=79.0e3 #pc
pos = (43.8813, -54.1160)

## Cluster stars distribution
cl_rad = 1.0 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((43.382, 43.65),(44.1, 44.38))
bkg_dec = ((-54.61, -53.734),(-54.5, -53.9))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 3

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.15
ra_max_alpha_center = 0.15
dec_min_alpha_center = -0.15
dec_max_alpha_center = 0.15 #all in degrees
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
