## Magnitudes and Color keys
obj_name = "booii"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=19
max_mag_cut=25
min_color_cut=0.1
max_color_cut=0.7
sharp = 1.0
chi = 2

## Obj
obj_radius = 3.07 #half-light radius, arcmin
cluster_distance=42.0e3 #pc
pos = (209.5141, 12.8553)

## Cluster stars distribution
cl_rad = 3 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((209, 210), (209, 210))
bkg_dec = ((12.42, 12.55),(13.2, 13.39))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 2

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.12
ra_max_alpha_center = 0.12
dec_min_alpha_center = -0.12
dec_max_alpha_center = 0.12 #all in degrees
contour_levels = [3,4,5,6,7,10,15,20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
