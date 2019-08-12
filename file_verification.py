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

def name2pixel(name):
	pix = int(name.split("_")[-1].split(".")[0])
	return pix

def lastpix(nside, wpix="last"): #wpix = what pixel?
	path      = os.getcwd()
	pathfits  = os.path.join(path,"FITS",str(nside))
	try:
		files     = os.listdir(pathfits)
		paths     = [os.path.join(pathfits,name) for name in files]
		nfits     = len(paths)
		
		if   wpix == "last":
			lastfits  = max(paths, key=os.path.getctime)
			print("There are {} fits files in : {}".format(nfits,pathfits))
			last      = name2pixel(lastfits)
			print("The last pix in directory is: {}".format(last))
			return last
		elif wpix == "first":
			firstfits = min(paths, key=os.path.getctime)
			print("There are {} fits files in : {}".format(nfits,pathfits))
			first     = name2pixel(firstfits)
			print("The first pix in directory is: {}".format(first)) 
			return first
		else:
			raise Exception("Invalid command.")
	except:
		print("There aren't files in: {}".format(pathfits))
		return False
