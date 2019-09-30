## Magnitudes and Color keys
obj_name = "hercules"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=21.7
max_mag_cut=24.6
min_color_cut=0.1
max_color_cut=0.67
sharp = 1.0
chi = 2

## Obj
obj_radius = 5.83 #half-light radius, arcmin
cluster_distance = 132e3 #pc
pos = (247.7722, 12.7852)

## Cluster stars distribution
cl_rad = 4.5 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 1
boxsize_cl = 4

kx_cl = 3
ky_cl = 3

## Background stars distribution
bkg_ra = ((246.92, 247.2), (248.3, 248.6))
bkg_dec = ((12.42, 13.35), (12.2, 13.1))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 1
boxsize_bkg = 3

kx_bkg = 1
ky_bkg = 1

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.25 #degrees from center
ra_max_alpha_center = 0.25
dec_min_alpha_center = -0.25 #degrees from center
dec_max_alpha_center = 0.25
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
