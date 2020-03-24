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
