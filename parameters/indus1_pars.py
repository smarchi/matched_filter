## Magnitudes and Color keys
obj_name = "indus1"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=20.5
max_mag_cut=25.5
min_color_cut=0.0
max_color_cut=0.8
sharp = 1.0
chi = 2

## Obj
obj_radius = 0.87 #half-light radius, arcmin
cluster_distance=100e3 #pc
pos = (317.2020, -51.1671)

## Cluster stars distribution
cl_rad = 2.5 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((316.703, 317.00), (317.4, 317.6))
bkg_dec = ((-51.666, -50.668),(-51.4, -51.05))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 5

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.1
ra_max_alpha_center = 0.1
dec_min_alpha_center = -0.1
dec_max_alpha_center = 0.1 #all in degrees
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
