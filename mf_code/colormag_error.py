def error_func(x, y, xlab = '', ylab = '', title = '', plot = False):

    import numpy as np
    from scipy import optimize
    from matplotlib import pyplot as plt

    def err_func(x,a,b,c,d):
        return a*np.exp(b*(x-c))+d

    #color error function
    popt,pcov = optimize.curve_fit(err_func,x,y,p0=(1.0,1e-2,20,0.001))

    if popt[3] < 0.001:
        popt[3] = 0.001

    if plot:
        deltax = 0.001
        x_range = np.append(np.arange(np.min(x),np.max(x),deltax),
                              np.max(x))
        plt.figure(figsize=(10,10))
        plt.plot(x,y,ls='none',marker='o',ms=4)
        plt.plot(x_range,err_func(x_range,*popt),color='red')
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.show()

    err_func2 = lambda x: err_func(x,*popt)
    return err_func2
