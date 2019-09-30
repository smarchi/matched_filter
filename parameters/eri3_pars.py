## Magnitudes and Color keys
obj_name = "eri3"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=21.5
max_mag_cut=24
min_color_cut=0.0
max_color_cut=1.0
sharp = 1.0
chi = 2

## Obj
obj_radius = 0.29 #half-light radius, arcmin
cluster_distance=87.0e3 #pc
pos = (35.6952, -52.2838)

## Cluster stars distribution
cl_rad = 1.0 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((35.196, 35.5),(35.9,36.1))
bkg_dec = ((-52.78, -51.784),(-52.78, -51.784))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 3

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
