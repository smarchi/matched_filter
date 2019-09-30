## Magnitudes and Color keys
obj_name = "ngc5694"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=17.5
max_mag_cut=24
min_color_cut=-0.4
max_color_cut=0.8
sharp = 1.0
chi = 2

## Obj
obj_radius = 0.42 #half-light radius, arcmin
cluster_distance = 35.0e3 #pc
pos = (219.9019, -26.5390)

## Cluster stars distribution
cl_rad = 3 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1

## Background stars distribution
bkg_ra = ((219.35, 219.60), (220.20, 220.45))
bkg_dec = ((-26.999, -25.962), (-26.999, -25.962))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 5

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.2
ra_max_alpha_center = 0.2
dec_min_alpha_center = -0.2
dec_max_alpha_center = 0.2 #all in degrees
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
