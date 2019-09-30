## Magnitudes and Color keys
obj_name = "fornax"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=19
max_mag_cut=25.5
min_color_cut=-0.4
max_color_cut=1.0
sharp = 1.0
chi = 2

## Obj
obj_radius = 18.4 #half-light radius, arcmin
cluster_distance = 147e3 #pc
pos = (39.9583, -34.4997)

## Cluster stars distribution
cl_rad = 10 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((40.35, 40.487), (39.51, 39.65))
bkg_dec = ((-34.83, -34.7), (-34.2, -34.07))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 2

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.3
ra_max_alpha_center = 0.3
dec_min_alpha_center = 0.3
dec_max_alpha_center = 0.3 #all in degrees
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
nboot = 8 #numer of iterations
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
