from . my_ras_utils import * 
from . run_system_command import *

import numpy as np
from scipy.stats.stats import nanmean
from math import isnan, sqrt
import matplotlib.pyplot as plt
from matplotlib import colors, cm
import matplotlib as mpl

def ascii_reader( filename):
    """
    Usage:
    dem, ncols, nrows, xllcorner, yllcorner, cellsize = ascii_reader( filename)
    """
    with open(filename,'r') as f:    
        ncolsTxt, ncols               = f.readline().split()
        ncols=int(ncols)    
        nrowsTxt, nrows               = f.readline().split()
        nrows=int(nrows)
        xllcornerTxt, xllcorner       = f.readline().split()
        xllcorner=float(xllcorner)
        yllcornerTxt, yllcorner       = f.readline().split()
        yllcorner=float(yllcorner)
        cellsizeTxt, cellsize         = f.readline().split()
        cellsize=float(cellsize)
        nodataTxt, nodata = f.readline().split()
        nodata=float(nodata)
        dem = np.genfromtxt((f.readlines()),dtype='float').reshape(nrows,ncols)
    return dem, ncols, nrows, xllcorner, yllcorner, cellsize


def ascii_writer(filename, DEM, xllcorner, yllcorner, cellsize):
    """
    Usage:
    ascii_writer(filename, DEM, xllcorner, yllcorner, cellsize)
    """
    nrows,ncols=DEM.shape    
    with  open(filename,'w') as f:
        f.write("ncols         %d\n"%ncols)
        f.write("nrows         %d\n"%nrows)
        f.write("xllcorner     %f\n"%xllcorner)
        f.write("yllcorner     %f\n"%yllcorner)
        f.write("cellsize      %f\n"%cellsize)
        f.write("nodata        -9999\n")
        f.write('\n'.join( [' '.join(map(str, r_ows )) for r_ows in DEM.tolist()]  )) ;
    return

def calc_f1(obsMat, actMat, thresholD, obsTrue, obsFalse):
    """
    Usage:
    F1 = calc_f1(observed_matrix, actual_matrix, threshold, obs_true_value, obs_false_value)
    """
    a,b,c=[],[],[]    
    tempA = np.logical_and(obsMat == obsTrue, actMat > thresholD)
    tempB = np.logical_and(obsMat == obsFalse, actMat > thresholD)
    tempC = np.logical_and(obsMat == obsTrue, actMat < thresholD)
    a = float(np.sum(tempA[:]))
    b = float(np.sum(tempB[:]))
    c = float(np.sum(tempC[:]))    
    return (a/(a+b+c))

def write_bdy_file(filename, q_hyd):
    '''
    Usage:
    write_bdy_file(filename, q_hydrograph)
    '''    
    f = open(filename, 'w')
    f.write('QTBDY\nupstream\n')
    f.write('%d\tseconds\n'%(len(q_hyd[0])))
    for cnt in range(len( q_hyd[0] )):
        f.write('%f\t%f\n'%(q_hyd[1][cnt], q_hyd[0][cnt]))        
    f.close()
    
def write_steady_bci(filename, q_steady_value):
    '''
    Usage:
    write_steady_bci(filename, q_steady_value)
    '''
    f = open(filename,'r')
    tlines = f.readlines()
    f.close()

    f = open(filename,'w')    
    for line in tlines:
        temp = line.split()
        if temp[3] == 'QFIX':
            f.write('%s\t\t%s\t\t%s\t\t%s\t\t%s\n'%(temp[0],
                temp[1],temp[2],temp[3],str(q_steady_value)))
        else:
            f.write('%s\t\t%s\t\t%s\t\t%s\t\t%s\n'%(temp[0],
                temp[1],temp[2],temp[3],temp[4]))        
    f.close()
    
def write_nch2pram(filename, n_ch ):
    '''
    Usage:
    write_nch2pram(filename, n_ch )
    ## write_pram_file(filename, ch_type, ch_par_r, ch_par_p, n_ch )
    '''
    
    f = open(filename,'r')
    tlines = f.readlines()
    f.close()

    f = open(filename, 'w')
    f.write(tlines[0])
    tline = tlines[1].split()
    for k in range((len(tline))-1):
        f.write('%s '%tline[k]),
    f.write('%f\n'%n_ch)
    f.close()
    
def write_par(parfile, n_ch, n_fp):
    
    f = open(parfile,'r')
    tlines = f.readlines()
    f.close()

    f = open(parfile,'w')
    for tlin in tlines:        
        temp = tlin.replace('\n','').split()
        if len(temp) == 0:
            f.write('\n')
        else:
            if temp[0] == 'fpfric':
                f.write('%s\t\t\t%f\n'%(temp[0],n_fp))
            elif temp[0] == 'SGCn':
                f.write('%s\t\t\t%f\n'%(temp[0],n_ch))
            else:
                if len(temp) == 2:
                    f.write('%s\t\t\t%s\n'%(temp[0],temp[1]))
                else:
                    f.write('%s\n'%temp[0])
    f.close()


def stage_read(file_name):
    '''
    Usage:
    stagedata = readstage(file_name)
    ''' 
    with open(file_name) as f:
        for i in range(7):
            f_contents = f.readline()
        stations_no = int((f_contents.split('to'))[1].replace('\n',''))
        f_contents = f.readlines()        
    stagedata = [[]]    
    for stn in range(stations_no):
        stagedata.append([])            
    for itm in f_contents:
        temp = itm.replace('\n','').split()
        for i, rec in enumerate(temp):
            stagedata[i].append(float(rec))            
    return stagedata

def nse_calc(obs, sim):
    '''
    Usage:
    NSE = nse_calc(obs, sim)
    '''
    N = len(obs)
    mean_val = nanmean(obs)
    num, den, N1 = 0., 0., 0.
    for i in range(N):
        if (not isnan(obs[i])) and (not isnan(sim[i])):
            num += ( obs[i] - sim[i] ) * ( obs[i] - sim[i] )
            den += ( sim[i] - mean_val ) * ( sim[i] - mean_val )
            N1 += 1
    return 1 - ((num / float(N1)) / (den / float(N1)))

def rmse_calc(obs, sim):
    '''
    Usage:
    rmse = rmse_calc(obs, sim)
    '''
    N = len(obs)
    mean_val = nanmean(obs)
    num, N1 = 0., 0.
    for i in range(N):
        if (not isnan(obs[i])) and (not isnan(sim[i])):
            num += ((obs[i] - sim[i])*(obs[i] - sim[i]))            
            N1 += 1
    return sqrt(num / float(N1))

def likelihood_weights(obj_fn):
    obj_fn = np.array(obj_fn)
    max_fn = obj_fn.max()
    min_fn = obj_fn.min()
    return [ (float(max_fn) - float(xx))/(float(max_fn) - float(min_fn))  for xx in obj_fn]
    
def plot_ascii_map(filename, thetitle):
    dem, ncols, nrows, xllcorner, yllcorner, cellsize = ascii_reader(filename)
    cmap = mpl.cm.jet
    #cmap.set_over('k')
    cmap.set_under('w')
    norm = mpl.colors.Normalize(vmin=np.nanargmin(dem)+1e-6, vmax=dem.max()-1e-6)
    ticks_at=np.linspace(np.nanargmin(dem), dem.max()-1e-6, 4)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax = fig.add_axes([0.1, 0.1, 0.65, 0.7])
    #ax1= fig.add_axes([0.85, 0.1, 0.02, 0.7])
    ax.set_title(thetitle)
    cax = ax.imshow(dem, interpolation='nearest',cmap=cmap, norm=norm)#, alpha=.5)
    # setting the x-axis
    ax.set_xlim((0,ncols))
    ax.set_xticks((0, ncols))
    ax.set_xticklabels((xllcorner,(xllcorner+(ncols)*cellsize)),size='small')
    ax.set_xlabel('x-coordinate')

    # setting the y-axis
    ax.set_ylim((nrows,0))
    ax.set_yticks((0,nrows))
    ax.set_yticklabels(((yllcorner+(nrows)*cellsize),yllcorner),size='small')
    ax.set_ylabel('y-coordinate')

    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    cbar = fig.colorbar(cax,ticks=ticks_at,format='%5.1f',fraction=.02)

    #fig.tight_layout()
    plt.show()           


    
def plot_raster_matrix(dem, ncols, nrows, xllcorner, yllcorner, cellsize, thetitle):
    # working on the colors        
    cmap = mpl.cm.jet
    #cmap.set_over('k')
    cmap.set_under('w')
    try:
        thevmin = dem[dem>0].min()
        thevmax = dem.max()
    except:
        thevmin = 0
        thevmax = dem.max()       

    if thevmin == thevmax:
        print 'zero matrix, nothing to plot'
    else:
        norm = mpl.colors.Normalize(vmin=thevmin, vmax=thevmax)
        #ticks_at=np.linspace(thevmin, thevmax-1e-6, 4)

        ticks_at=np.linspace(thevmin, thevmax, 4)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(thetitle )

        #cax = ax.imshow(dem, interpolation='nearest',cmap=cmap, norm=norm)#, alpha=.5)
        cax = ax.imshow(dem, interpolation='nearest',cmap=cmap, norm=norm)

        # setting the x-axis
        ax.set_xlim((0,ncols))  
        ax.set_xticks((0, ncols))
        ax.set_xticklabels((xllcorner,(xllcorner+(ncols)*cellsize)),size='small')
        ax.set_xlabel('x-coordinate')
         
        # setting the y-axis
        ax.set_ylim((nrows,0))
        ax.set_yticks((0,nrows))
        ax.set_yticklabels(((yllcorner+(nrows)*cellsize),yllcorner),size='small')
        ax.set_ylabel('y-coordinate')

        # Add colorbar, make sure to specify tick locations to match desired ticklabels
        cbar = fig.colorbar(cax,ticks=ticks_at,format='%5.1f',fraction=.02)
        #fig.tight_layout()
        plt.show()
    

