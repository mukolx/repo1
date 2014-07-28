import matplotlib as mpl
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt

try:
    from osgeo import gdal
except ImportError:
    import gdal

def get_raster_info(filename):
    dataset = gdal.Open(filename , gdal.GA_ReadOnly )
    geotransform = dataset.GetGeoTransform()
    xllcorner = geotransform[0]
    yul = geotransform[3]
    cellsize = geotransform[1]
    ncols = dataset.RasterXSize
    nrows = dataset.RasterYSize
    yllcorner = yul-nrows*cellsize
    dem=dataset.GetRasterBand(1).ReadAsArray()
    dataset = None
    return dem, ncols, nrows, xllcorner, yllcorner, cellsize
    
def plot_raster(filename, thetitle):
    dataset = gdal.Open(filename , gdal.GA_ReadOnly )
    geotransform = dataset.GetGeoTransform()
    xllcorner = geotransform[0]
    yul = geotransform[3]
    cellsize = geotransform[1]
    ncols = dataset.RasterXSize
    nrows = dataset.RasterYSize
    yllcorner = yul-nrows*cellsize
    dem=dataset.GetRasterBand(1).ReadAsArray()
    #dataset = None
    # working on the colors        
    cmap = cm.jet
    #cmap.set_over('k')
    cmap.set_under('w')
    try:
        thevmin = dem[dem>0].min()
        thevmax = dem.max()
    except:
        thevmin = 0
        thevmax = dem.max()
        

    if thevmin == thevmax:
        pass
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

