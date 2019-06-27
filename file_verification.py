import os
    
def file_verification(path,file,nside):
    if os.path.isdir(path):
        path = os.path.join(path,str(nside)) 
        if os.path.isdir(path): 
            path = os.path.join(path,file) 
            if os.path.isfile(path): 
                os.remove(path)
        else:
            os.mkdir(path)
    else:
        os.mkdir(path)
        os.mkdir(os.path.join(path,str(nside)))
