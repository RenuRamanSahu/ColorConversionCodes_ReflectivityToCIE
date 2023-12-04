import numpy as np
import matplotlib.pyplot as plt
import R2cie #### self made library for colorimetry
from  mpl_toolkits.axes_grid1.inset_locator  import (inset_axes, InsetPosition, mark_inset)
from matplotlib.patches import Rectangle


filename = "sample3"#+"_afterWash"
data = np.loadtxt(filename+'.txt')
wavelength =  data[:, 0][100:]
R = data[:, 1][100:]

def scale(x):
    minx = 0.15
    maxx = 0.60
    x = minx +(maxx-minx)*(x-min(x))/(max(x) - min(x))
    return x


#Smoothing Data
N = 15
wavelength = np.convolve(wavelength, np.ones(N)/N, 'valid')
R1 = np.convolve(R, np.ones(N)/N, 'valid')



fig, (ax1, ax2) = plt.subplots(1,2, figsize=(9, 4.5))
ax1.plot(wavelength, R1, lw = 3)
# ax1.plot(wavelength2, R2, lw = 3, label = "After one year")
ax1.legend(fontsize = 16)
ax1.set_xlabel(r'$\lambda$ (nm)', fontweight = "bold", fontsize = 16)
ax1.set_ylabel('R (Arb. units)', fontweight = "bold", fontsize = 16)
ax1.tick_params(axis = 'both',  direction = 'in', labelsize = 16)
plt.sca(ax1)
plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')


I = plt.imread("CIE_xyY40percent.tiff")
I = I[100:1000, 0:800 ]
ax2.imshow(I, extent = [0.1, 0.8, 0, 0.9])
ax2.set_xlabel('CIE x', fontweight = "bold", fontsize = 16)
ax2.set_ylabel('CIE y', fontweight = "bold", fontsize = 16)
x, y, Y = R2cie.Reflectivity2cie(wavelength, R1)
ax2.plot(x, y, '.', color = 'black', alpha = 1)
ax2.text(0.40, 0.80, "\n("+str("{:.2f}".format(x))+", "+str("{:.2f}".format(y))+")", fontweight = "bold",  fontsize = 16)
# ax2.text(0.43, 0.80, "After:\n("+str("{:.2f}".format(0.29))+", "+str("{:.2f}".format(0.37))+")",  fontsize = 13)

Y = 0.45


ax2.tick_params(axis = 'both',  direction = 'in', labelsize = 16)
plt.sca(ax2)
plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')




rgb = R2cie.xyY_to_rgb(x, y, Y)
HSV = R2cie.RGB_to_HSV(rgb[0],rgb[1], rgb[2])
ax3 = plt.axes([0, 0, 1, 1])
ip = InsetPosition(ax2, [0.65,0.700,0.16,0.12])
ax3.set_axes_locator(ip)
ax3.set_xticks([])
ax3.set_yticks([])
ax3.set_frame_on(False)
rect = Rectangle((0, 0), 1, 1, facecolor = rgb, edgecolor = rgb)
ax3.add_patch(rect)


plt.tight_layout()
plt.savefig(filename+".svg", format = "svg")
plt.show()
