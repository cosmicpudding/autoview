import os
import sys
import aplpy
from math import *
from numpy import *
from pylab import *
import pyfits
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif'],'size':16})
from astropy.io import ascii
import time

# Make an image
def makeimage(fitsname,name,field,ra,dec):

	f = aplpy.FITSFigure(fitsname)
	f.show_colorscale(cmap='Greys',pmin=2.5,pmax=97.5)
	#f.show_markers(ra,dec,marker='o',facecolor='',edgecolor='r',alpha=0.5,s=4000,linewidth=3)
	f.show_circles(ra, dec, 30/3600., facecolor='',edgecolor='r',alpha=0.5,linewidth=4)
	title('%s' % (name))
	f.add_colorbar()
	savefig('results/%s_%s.png' % (field,name),bbox_inches='tight',transparent=True,dpi=200)

def makergbimage(rgbarray,iname,field,ra,dec):

	os.system('rm -rf rgbcube.fits rgbcube2.fits rgbcube_2d.fits')
	aplpy.make_rgb_cube(rgbarray, 'rgbcube.fits')
	aplpy.make_rgb_image('rgbcube.fits', '%s_%s.png' % (field,iname), pmax_r=95., pmax_g=95., pmax_b=95.)
		# # # Set a CTYPE
	d = pyfits.open('rgbcube.fits')
	hdr,data = d[0].header,d[0].data
	hdr['CTYPE3'] = 'VELO-LSR'
	pyfits.writeto('rgbcube2.fits',data,hdr)
	f = aplpy.FITSFigure('rgbcube2.fits',dimensions=[0, 1], slices=[0])
	f.show_rgb('%s_%s.png' % (field,iname))
	f.show_circles(ra, dec, 30/3600.,facecolor='',edgecolor='w',alpha=0.5,linewidth=4)
	#f.show_markers(ra,dec,marker='o',facecolor='',edgecolor='w',alpha=0.5,s=4000,linewidth=3)
	savefig('results/%s_%s_rgb.png' % (field,iname),bbox_inches='tight',transparent=True,dpi=200)
	os.system('rm -rf %s_%s.png' % (field,iname))

def autoview(field,coord1,coord2,dim,filename):

	start = time.time()

	file = open(filename,'r')
	dim = dim/60.

	# set the coordinates
	ra,dec = coord1,coord2

	# Loop over the surveys of interest
	for line in file:
		col = line.split()
		if len(col) < 2:
		    continue
		name = col[0]
		fits = name.lower()
		print('Currently processing survey: %s\n\n' % name)

		os.system('java -jar skyview.jar coordinates=J2000 projection=Sin position=%s,%s size=%s,%s pixels=1000,1000 survey="%s" output="results/%s_%s.fits"' % (ra,dec,dim,dim,name,field,fits))
		try:
			makeimage("results/%s_%s.fits" % (field,fits),name,field,ra,dec)
		except:
			continue

	# # Try making the 3 colour images
	# if 'first' not in filename:
	# 	makergbimage(['results/%s_2massk.fits' % field,'results/%s_2massj.fits' % field,'results/%s_2massh.fits' % field],'2MASS',field,ra,dec)
	# 	makergbimage(['results/%s_wise12.fits' % field,'results/%s_wise4.6.fits' % field,'results/%s_wise3.4.fits' % field],'WISE',field,ra,dec)

	end = time.time()
	tottime = (end-start)/60.

	return tottime
