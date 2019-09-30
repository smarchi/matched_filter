## Magnitudes and Color keys
obj_name = "cvni"
mag_key='g'
color_key='g-r'

## Color and mag limits for cuts
min_mag_cut=20
max_mag_cut=26
min_color_cut=-0.5
max_color_cut=1.0
sharp = 1.0
chi = 2

## Obj
obj_radius = 7.48 #half-light radius, arcmin
cluster_distance=218.0e3 #pc
pos = (202.0091, 33.5521)

## Cluster stars distribution
cl_rad = 4.5 #arcminutes
error_function = None

delta_mag_gs=0.1
delta_color_gs=0.01
delta_interp_mag=0.01
delta_interp_color=0.001

smooth_cl = 5
boxsize_cl = 2

kx_cl = 3
ky_cl = 3

## Background stars distribution
bkg_ra = ((201.43, 202.6), (201.43, 202.6))
bkg_dec = ((33.15, 33.25),(33.95, 34.05))
delta_mag_bkg=0.1
delta_color_bkg=0.01
smooth_bkg = 0
bkg_error_factor = 5
boxsize_bkg = 1

kx_bkg = 1
ky_bkg = 1

## Counting stars
delta_ra = 0.5/60 #degrees
delta_dec = 0.5/60 #degrees
ra_min_alpha_center = -0.45
ra_max_alpha_center = 0.45 #all in degrees
dec_min_alpha_center = -0.45
dec_max_alpha_center = 0.45
contour_levels = [3, 4, 5, 6, 7, 10, 15, 20]

#bootstrap parameters
ra_boot_lims_center = (ra_min_alpha_center, ra_max_alpha_center) #solid angle to bootstrap
dec_boot_lims_center = (dec_min_alpha_center, dec_max_alpha_center)
