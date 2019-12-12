import os
import sys
import aplpy
from math import *
from numpy import *
from pylab import *
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif'],'size':14})
from astropy.io import ascii
import aplpy
from autoview import *
import time

dim = 3 # arcmin
filename = 'skyview_slim.txt'
d = ascii.read('samples/nvssgama9_100mJy.csv')
print (d.keys())

# Logfile
out = open('processed.txt','a')
e = ascii.read('processed.txt')

for i in range(0,len(d)):

	# ensure that this coord is decimal coordinates in current format!
	coord1,coord2 = d['_RAJ2000'][i],d['_DEJ2000'][i]
	field = str(coord1)+'_'+str(coord2)

	# Check if processed
	if field in e['field']:
		print ('Processed!')
		continue

	# Make the call to autoview, and write to file when done
	tottime = autoview(field,coord1,coord2,dim,filename)
	out.write('%s %.2f\n' % (field,tottime))
	out.flush()
