import os,sys
    
def file_verification(path,filename,directory):
	
	if type(directory)==int or type(directory)==float:
		directory = str(directory)
	elif type(directory)==str:
		pass	
	else:
		raise(sys.exc_info()[0])
		
	if os.path.isdir(path):
		path = os.path.join(path,directory) 
		if os.path.isdir(path):
			path = os.path.join(path,filename)
			if os.path.isfile(path):
				os.remove(path)
		else:
			os.mkdir(path)
	else:
		os.mkdir(path)
		os.mkdir(os.path.join(path,directory))

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

def exist_or_not_file(params,restart):
	if not restart:
		str_npix      = str(params['NPIX'])
		str_nside     = str(params['NSIDE'])
		str_pix       = str(int(params['pixel']))
		len_str_npix  = len(str_npix)
		len_str_pix   = len(str_pix)
		len_zero      = len_str_npix - len_str_pix
		file_ = "_".join(("PixelFit",str_nside,"0"*len_zero+str_pix))
		file_ = ".".join((file_,"fits"))
		path = os.getcwd()
		path = os.path.join(path,"FITS",str_nside,file_)
		return os.path.isfile(path)
	elif restart:
		return False
	else:
		raise NameError
