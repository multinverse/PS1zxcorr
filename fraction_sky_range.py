def divideSKY(divideSKYrange,strips):
    import numpy as np
    npix_strips = len(strips)
    n           = int(np.floor(npix_strips/divideSKYrange['Nparts']))
    rest        = npix_strips - n*divideSKYrange['Nparts']
    pixs        = np.arange(0,n*divideSKYrange['Nparts']).reshape(divideSKYrange['Nparts'],n)[divideSKYrange["part"]-1]
    
    if rest>0:
        if 1<=divideSKYrange['part']<=rest:
            pix_add = strips[-rest:][divideSKYrange['part']-1]
            pixs    = np.hstack((strips[pixs],pix_add))
            strips = pixs
        else:
            strips = strips[pixs]
    else:
        strips = strips[pixs]
    return strips
    
'''
def divideSKY(divideSKYrange,strips):
    import numpy as np
    ran   = strips#np.arange(start = 0, stop = NPIX, step = 1)
    try:
        strips = np.split(ran,divideSKYrange['Nparts'])[divideSKYrange['part']-1]
    except:
        div = float(len(strips))/divideSKYrange['Nparts']
        Slice = np.arange(start = strips[0], stop = strips[-1], step = div)
        
        if divideSKYrange['part'] != divideSKYrange['Nparts']:
            strips = strips[np.where((ran<Slice[divideSKYrange['part']])*(ran>=Slice[divideSKYrange['part']-1]))]
        elif divideSKYrange['part']==divideSKYrange['Nparts']:
            strips = strips[np.where(ran>=Slice[divideSKYrange['part']-1])]
        else:
            raise ValueError
    return strips


'''
