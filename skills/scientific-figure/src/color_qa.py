"""Accessibility preview generation; no perceptual PASS is attested."""
from PIL import Image,ImageOps
import numpy as np
def previews(p,out):
 im=Image.open(p).convert('RGB');ImageOps.grayscale(im).save(out/'grayscale.png',dpi=(300,300))
 a=np.asarray(im,dtype=float)/255;linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
 mat=np.array([[.367322,.860646,-.227968],[.280085,.672501,.047413],[-.01182,.04294,.968881]])
 b=np.clip(linear@mat.T,0,1);b=np.where(b<=.0031308,12.92*b,1.055*b**(1/2.4)-.055)
 Image.fromarray(np.uint8(np.clip(b,0,1)*255)).save(out/'cvd_deuteranopia_approx.png',dpi=(300,300))
 return {'COLOR_PREVIEWS_GENERATED':True,'evaluation':'NOT_CHECKED','method':'linear RGB matrix deuteranopia approximation; not clinical simulation','files':['grayscale.png','cvd_deuteranopia_approx.png']}
