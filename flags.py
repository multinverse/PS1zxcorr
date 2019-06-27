import os
import numpy as np
from math import *

def hex2bin(hexa):
    return bin(int(hexa))[2:]



def flags_verification(params_flags, params_hexa): #Check which flags are enabled
    flags = []
    for i in range(params_flags['num flags']):
        bin_flagi = hex2bin(params_flags['datas'][i])
        len_flagi = len(bin_flagi)
        
        for j in range(len_flagi):
            bin_q = params_hexa['binary hexa'][-j-1]
            bin_f = bin_flagi[-j-1]
            
            if bin_f=="1" and bin_q=="1":
                flags = np.append(flags,params_flags['names'][i][:-1])
                break
        if len_flagi+1>params_hexa['length hexa']: return flags#break
        
        
        
def hexa2flags(hexa,file_names,file_datas): #input one (hexa)decimal and return the flags are enabled, of a certain table.
    bin_query    = hex2bin(hexa)
    len_query    = len(bin_query)
    
    file_names   = os.path.join("FLAGS",file_names)
    file_datas   = os.path.join("FLAGS",file_datas)
    
    file_        = open(file_names,'r')
    names        = file_.readlines()
    file_.close()
    datas        = np.loadtxt(file_datas)
    num_flags    = len(datas)
    
    params_flags = {"names":names, "file":file_names,"datas":datas,"num flags":num_flags}
    params_hexa  = {"length hexa":len_query, "binary hexa":bin_query}
    
    return flags_verification(params_flags,params_hexa)



def accept_data(flags_table, flags_input):
    if set(flags_input).intersection(set(flags_table))==set():
        return True
    else:
        return False



def flags_constraints(tab,hexa_query,params):
    
    file_names = "".join(("FLAGS",str(params["table"]),".txt"))
    file_datas = "".join(("DATA_FLAGS",str(params["table"]),".txt"))
    
    params["bands"] = ["g","r","i","z","y"]
    lbands          = len(params["bands"])
    flags_query     = hexa2flags(hexa_query,file_names,file_datas)
    
    if params["table"]: flag_tab = tab["".join((params["bands"][0],"infoFlag"))]
    else: flag_tab = tab["".join((params["bands"][0],"infoFlag",str(params["table"])))]
    pos = []
    
    for j in range(len(flag_tab)):
        flags_tab    = hexa2flags(flag_tab[j],file_names,file_datas)
        if accept_data(flags_tab,flags_query): pos = np.append(pos,j)
        else: pass
    
    if lbands-1:           
        for i in range(lbands-1): 
            i+=1
            if params["table"]: flag_tab = tab["".join((params["bands"][i],"infoFlag"))]
            else: flag_tab = tab["".join((params["bands"][i],"infoFlag",str(params["table"])))]
            pos2 = []
            for j in range(len(flag_tab)):
                flags_tab    = hexa2flags(flag_tab[j],file_names,file_datas)
                if accept_data(flags_tab,flags_query):
                    pos2 = np.append(pos2,j)
                else: pass
            pos = set(pos).intersection(set(pos2))
    pos = map(int,list(pos))
    return  tab[pos]
