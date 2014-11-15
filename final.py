#!/usr/bin/env python

'''
change send pixel

'''


import opc
import time
import random
import subprocess
import os

import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.io import wavfile # get the api
from scipy.fftpack import fft
from scipy import signal


# pixel map
pixels_map = [[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)],[(0,0,255),(0,0,255),(0,0,255),(0,255,0),(0,255,0),(0,255,0),(255,0,0),(255,0,0),(255,0,0),(255,255,255)]]

pixel_off = [(0,0,0)]*100

# connect to beagle
ADDRESS = '192.168.7.2:7890'

# Create a client object
client = opc.Client(ADDRESS)

# Test if it can connect
if client.can_connect():
    print 'connected to %s' % ADDRESS
else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
    print 'WARNING: could not connect to %s' % ADDRESS


# data analyze
MUSIC = 'mario.wav'
formal_fft = []
grid = []
col = [0,0,0,0,0,0,0,0,0,0]
colNormalize = [0,0,0,0,0,0,0,0,0,0]
col_rfft = [0,0,0,0,0,0,0,0,0,0]
fs, data = wavfile.read(MUSIC) # load the data
a = data.T[0]
a_downsize = a.reshape(-1,4).mean(axis=1)

refresh = 0.1; #in seconds
refreshrate = 1/refresh; 

subprocess.Popen(["aplay",MUSIC,"&"])

number = int( math.floor(len(a_downsize)/((fs/4)/refreshrate)))
for i in range(0,number):
	send_pixel = [(0,0,0)]*100
        tmp_arr = a_downsize[((fs/4)/refreshrate)*i : (((fs/4)/refreshrate)*(i+1)-1)]
        tmp_pre_fft = [(ele/2**8.)*2-1 for ele in tmp_arr]
        tmp_fft = np.fft.rfft(tmp_pre_fft)
	fftlength = (fs/4)/refreshrate;
	tmp_fft_right = abs(tmp_fft[:(fftlength-1)])
	maxfft = max(tmp_fft_right);
	x_segment= int(math.floor(len(tmp_fft_right)/10))
	for j in range (0,10):
		col[j] = np.mean(tmp_fft_right[j*x_segment:x_segment*(j+1)-1])
	fftmax = max(col);
	for k in range (0,10):
		col_avg = np.mean(col)
		if(col[k] < col_avg):
			colNormalize[k] = (5 - math.floor(((abs(col[k]-col_avg)/col_avg)*50/10)))
		else:
			colNormalize[k] = (5 + math.floor(((abs(col[k]-col_avg)/col_avg)*50/10)))
#		colNormalize[k] = math.ceil(col[k]/fftmax*10)
#
	
#	print col;
#	print colNormalize;
	
# send pixel
	x = 0
	for n in range(0,10):
		if (colNormalize[n] > 10):
			range_max = 10
		else:
			range_max = int(colNormalize[n])
		for m in range(0,range_max):
			send_pixel[n*10+m] = pixels_map[n][m]
	
	client.put_pixels(send_pixel, channel=0)

			




