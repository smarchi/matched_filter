## Magnitudes and Color keys
obj_name = "cvnii"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=20.3
max_mag_cut=25
min_color_cut=-0.4
max_color_cut=0.8
sharp = 1.0
chi = 2

## Obj
obj_radius = 1.51 #half-light radius, arcmin
cluster_distance=160.0e3 #pc
pos = (194.2927, 34.3226)

## Cluster stars distribution
cl_rad = 1.51 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1
boxsize_cl = 3

## Background stars distribution
bkg_ra = ((193.7, 194), (194.6, 194.87))
bkg_dec = ((33.87, 34.89),(33.84, 34.7))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 1
boxsize_bkg = 3

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center=-0.10
ra_max_alpha_center=0.10
dec_min_alpha_center=-0.10
dec_max_alpha_center=0.10
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
