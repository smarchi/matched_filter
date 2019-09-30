## Magnitudes and Color keys
obj_name = "ret2"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=18
max_mag_cut=24
min_color_cut=-0.2
max_color_cut=0.7
sharp = 1.0
chi = 2

## Obj
obj_radius = 5.59 #half-light radius, arcmin
cluster_distance=30.0e3 #pc
pos = (53.9203, -54.0513)

## Cluster stars distribution
cl_rad = 6 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((53.421, 54.42),(53.421, 54.42))
bkg_dec = ((-54.55, -54.35),(-53.8, -53.552))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 3

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.3
ra_max_alpha_center = 0.3
dec_min_alpha_center = -0.3
dec_max_alpha_center = 0.3 #all in degrees
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
