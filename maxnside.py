import os
import mastcasjobs
import requests
import os, sys, re
import json
import numpy as np
import healpy as hp
import query as qr

def maxnside(user,pwd):
    
    theta,phi = 0.,0.#in degree
    nsides    = [2**x for x in range(12)][1:]
    nsides    = np.flip(nsides)
    
    for nside in nsides:
        pix         = hp.ang2pix(nside,theta = theta,phi = phi, lonlat=True) 
        ang, radius = qr.parameters(nside,pix)
        query       = qr.query_string(theta,phi,radius)
        jobs        = mastcasjobs.MastCasJobs(context="PanSTARRS_DR2")
    
        try:
            jobs.quick(query, task_name="python cone search")
            pass
        except Exception:
            return nside
