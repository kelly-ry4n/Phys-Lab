from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import doctest          # We need to perform the unit tests indicated 


def best_fit( x, y ) :
    """
    Accepts two iterables, x and y, and returns two floats, a and b, 
    which are the coefficients for the least-squares best-fit line, y=ax+b. If the inputs have
    ufloat type, so will the output
    """

    n = len(x)

    S_x =   sum([x_i for x_i in x])
    S_y =   sum([y_i for y_i in y])
    S_xx =  sum([x_i**2 for x_i in x])
    S_yy =  sum([y_i**2 for y_i in y])
    S_xy =  sum([x_i*y_i for x_i, y_i in zip(x,y)])

    a = ( n*S_xy - S_x*S_y ) / ( n*S_xx - S_x**2 )

    b = (S_y - a*S_x)/n

    line_label = 'Best Fit $y=%sx + %s$\n$ \, \sigma _{max} = \pm %s\
                ,\, \sigma _{slope} = \pm %s \, \sigma _{intercept}\
                 = \pm %s$'                                % (sig_dig(a.nominal_value, 3),
                                                             sig_dig(a.nominal_value, 3),
                                                             sig_dig((a + b).std_dev(), 2),
                                                             sig_dig(a.std_dev(),3),
                                                             sig_dig(b.std_dev(),3))

    return a, b, line_label

def is_line_good(line):
    try:
        return line[0] != '#'
    except IndexError:
        return False

def get_data_with_uncert(filename):
    ''' Loads main data from csv, which is separated into data/uncert pairs, and returns
    an array of ufloats of this data'''
    from uncertainties import ufloat

    with open(filename) as f:
        txt = f.read()
    lines = txt.split('\n')
    lines = filter(is_line_good, lines)
    nums = [line.split(',') for line in lines]
    out = []
    for group in nums:
        ucerts= [num.split('/') for num in group]
        out.append([ufloat( (float(i[0].strip()),float(i[1].strip()) ) ) for i in ucerts])

    return out

def polyplot(a,min_val,max_val,label='polyplot label'):

    plot_range = np.linspace(min_val, max_val ,100)
    y_values = [y.nominal_value for y in np.polyval(a,plot_range)]

    plt.plot(plot_range,y_values,'k', label=label)

def sig_dig(number, sigfig):
    from math import floor, log10
    return float(("%.15f" % (round(number,
            int(-1 * floor(log10(number)) + (sigfig - 1))))).rstrip("0").rstrip("."))

def sig_dig(number, sigfig):
    return number

def plot_with_bars_and_line(xs,ys,filename, label='$X$ (units) vs $Y$ (units)',
                             format='.', xlabel='X', ylabel='Y'):

    fig = plt.figure()
    ax = plt.subplot(111)
    x_val = [x.nominal_value for x in xs]
    x_unc = [x.std_dev() for x in xs]

    y_val = [y.nominal_value for y in ys]
    y_unc = [y.std_dev() for y in ys]


    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    a,b,line_label = best_fit(xs,ys)
    polyplot([a,b],0, max(x_val), label=line_label)

    ax.errorbar(x_val,y_val, xerr=x_unc, yerr=y_unc, color='k', ecolor='r', fmt=format,
                    label="%s VS %s" % (xlabel, ylabel))


    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07),
          fancybox=True, shadow=True, ncol=1)

    plt.show()

    return a, b

def main():

    filename = 'testcsv.csv'

    nums = get_data_with_uncert(filename)

    plot_with_bars_and_line(nums[0],nums[1],'file.png', xlabel="Test x (meters)",
                            ylabel="derp (seconds)")

if __name__ == '__main__':
    main()