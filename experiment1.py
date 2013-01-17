from __future__ import division
from uncertainties import ufloat
from numpy import pi, sqrt, array
from bestfit import plot_with_bars_and_line

def B_from_current(I_total):
    I_earths = [0.257,0.218,0.226,0.256,0.240,0.263,0.218,0.226,0.228,0.223]
    #I_earths = [ufloat((I,0.003)) for I in I_earths]
    I_earth = average(I_earths)
    print 'THe earth avg is', I_earth
    return 8*(4*pi*10**(-7))*72*(I_total-I_earth)/(0.33*sqrt(125))

def average(B_values):
    return sum(B_values)/len(B_values)

## TODO
I_ucert = 0.02
V_ucert = 0.05

## TODO
I_values = [
                [2.706,2.306,2.006,1.775,1.602],
                [3.260,2.760,2.410,2.140,1.917],
                [3.739,3.162,2.741,2.430,2.186],
                [4.137,3.494,3.141,2.680,2.418],
                [4.327,3.658,3.176,2.806,2.515]
            ]

for row in I_values:
    for val  in row:
        print str(val)+' & ',
    print '\\\\'

## DONE -- don't change
V_values = [20,30,40,50,55.2]
V_values = [ufloat((V,V_ucert)) for V in V_values]
R_values = array([0.0325,0.039,0.045,0.0515,0.0575])


B_values = array([B_from_current(ufloat((average(I_val),I_ucert))) for I_val in I_values])

BR_square = (B_values**2*R_values**2).tolist()


slope,inter = plot_with_bars_and_line(BR_square,V_values,'name.png',
                        label='$V$ (Volts) vs $BR^2$ (units)',
                        format='.',
                        xlabel='$V$ (Volts)',
                        ylabel='$(BR)^2$ (units)')

ratio = 4*slope
print ratio