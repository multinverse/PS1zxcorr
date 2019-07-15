###################################################################################
# Here, its necessary improve the way of handling the error code=500
# if the error occurs again, it will be need to process until it extracts the data.
# The form implemented here is not yet the most appropriate
###################################################################################

import mastcasjobs
import healpy as hp
import numpy as np
import query as qr
from astropy.io import ascii
from astropy.table import vstack

def handling_exception(params,constraints):
    NSIDEmax = params['NSIDE max']
    vec      = hp.ang2vec(params["ang"][0],params["ang"][1], lonlat=True)
    pixels   = hp.query_disc(NSIDEmax,vec,np.radians(params['r']/3600.), inclusive= True)
    subjobs  = mastcasjobs.MastCasJobs(context="PanSTARRS_DR2")
    
    for pixel in pixels:
        ang,r     = qr.parameters(NSIDEmax,pixel)
        subquery  = sub_query_string(ang[0],ang[1],r)
        accept    = True
        
        while accept:
            try:
                subtab = subjobs.quick(subquery, task_name="python cone search")
                accept = False
            except Exception:
				from time import sleep
				sleep(60)
				pass
               
        subtab    = qr.fixcolnames(ascii.read(subtab))
        subtab    = qr.query_constraints(subtab, constraints)
        
        if pixel == pixels[0]:
            table = subtab
        else:
            table = vstack([table,subtab])

    return table




def sub_query_string(ang0,ang1,r):
        query = """select sot.objID, sot.uniquePspsSTid, sot.ippObjID, sot.surveyID, sot.tessID, sot.projectionID, sot.skyCellID, sot.randomStackObjID, sot.primaryDetection, sot.bestDetection, sot.dvoRegionID, sot.processingVersion,
 sot.gippDetectID, sot.gstackDetectID, sot.gstackImageId, sot.gra, sot.gdec, sot.graErr, sot.gdecErr, sot.gEpoch, sot.gPSFMag, sot.gPSFMagErr, sot.gApMag, sot.gApMagErr, sot.gKronMag, sot.gKronMagErr, sot.ginfoFlag, sot.ginfoFlag2, sot.ginfoFlag3, sot.gnFrames,
 sot.rippDetectID, sot.rstackDetectID, sot.rstackImageId, sot.rra, sot.rdec, sot.rraErr, sot.rdecErr, sot.rEpoch, sot.rPSFMag, sot.rPSFMagErr, sot.rApMag, sot.rApMagErr, sot.rKronMag, sot.rKronMagErr, sot.rinfoFlag, sot.rinfoFlag2, sot.rinfoFlag3, sot.rnFrames,
 sot.iippDetectID, sot.istackDetectID, sot.istackImageId, sot.ira, sot.idec, sot.iraErr, sot.idecErr, sot.iEpoch, sot.iPSFMag, sot.iPSFMagErr, sot.iApMag, sot.iApMagErr, sot.iKronMag, sot.iKronMagErr, sot.iinfoFlag, sot.iinfoFlag2, sot.iinfoFlag3, sot.inFrames,
 sot.zippDetectID, sot.zstackDetectID, sot.zstackImageId, sot.zra, sot.zdec, sot.zraErr, sot.zdecErr, sot.zEpoch, sot.zPSFMag, sot.zPSFMagErr, sot.zApMag, sot.zApMagErr, sot.zKronMag, sot.zKronMagErr, sot.zinfoFlag, sot.zinfoFlag2, sot.zinfoFlag3, sot.znFrames,
 sot.yippDetectID, sot.ystackDetectID, sot.ystackImageId, sot.yra, sot.ydec, sot.yraErr, sot.ydecErr, sot.yEpoch, sot.yPSFMag, sot.yPSFMagErr, sot.yApMag, sot.yApMagErr, sot.yKronMag, sot.yKronMagErr, sot.yinfoFlag, sot.yinfoFlag2, sot.yinfoFlag3, sot.ynFrames
 

 from fGetNearbyObjEq("""+",".join([str(ang0),str(ang1),str(r/60.)])+""") nb
 inner join StackObjectThin sot on sot.objid=nb.objid

 where sot.primaryDetection = 1 
""" 

        return query
