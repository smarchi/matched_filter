## Magnitudes and Color keys
obj_name = "umai"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=20.7
max_mag_cut=25
min_color_cut=-0.3
max_color_cut=0.8
sharp = 1.0
chi = 2

## Obj
obj_radius = 8.13 #half-light radius, arcmin
cluster_distance=97.2e3 #pc
pos = (158.7706, 51.9479)

## Cluster stars distribution
cl_rad = 5 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((159.2, 160.0), (158.45, 160.0))
bkg_dec = ((51.54, 51.7),(52.3, 52.5))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 5

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.15
ra_max_alpha_center = 0.6
dec_min_alpha_center = -0.45
dec_max_alpha_center = 0.45
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
