import matplotlib.pyplot as plt
import numpy as np
import hsluv
import matplotlib.colors as col
##

class imshow_multiple():
    def __init__(self,figsize = (7,7),cmap = 'hot', **kwargs):
        '''
        Initialize the imshow multiple class which allows to display quantitative figures while keeping the same scale between them.
        Using this method you can conveniently add more images to show and the class will automatically update the color scale of the whole set of images.
        
        Parameters
        ----------
        figsize = (7,7)

        cmap = 'hot'

         **kwargs:
            img_stack: a stack of images to display
        '''
        self.figsize = figsize
        self.axes = []
        self.figures = []
        self.images = []
        self.cax = []
        self.cbar = []
        self.cmap = cmap
        if 'img_stack' in kwargs:
            for image in kwargs['img_stack']:
                self.add_new(image)
                
    def add_new(self,image):
        '''
        Add a new image to the class, plot it and updates the other plots and colorbars
        
        Parameters
        ----------
        image: a new image to plot
        '''

        fig,ax = plt.subplots()
        self.figures.append(fig)
        self.axes.append(ax)
        self.images.append(image)
        self.cax.append(1)
        self.cbar.append(1)
        self.replot(image)
        self.harmonize()
            
    def replot(self,image):
        '''
        Takes the given image and plot it into a new figure, adapts the scale to previous images and replot them if the new image goes beyond.
        Parameters
        ----------
        image: a new image to plot
        '''


        replot_flag = False
        if len(self.axes) <=1:
            self.vmin = np.min(image)
            self.vmax = np.max(image)
        else:
            if np.min(image) < self.vmin:
                self.vmin = np.min(image)
                replot_flag = True
            if np.max(image) > self.vmax:
                self.vmax = np.max(image)
                replot_flag = True
        if replot_flag:
            for j,ax in enumerate(self.axes):
                self.cax[j] = self.axes[j].imshow(self.images[j],vmin = self.vmin, vmax = self.vmax,cmap = self.cmap)
                # self.figures[j].colorbar(self.cax[j])
                if self.cbar[j] == 1:
                    self.cbar[j] = self.figures[j].colorbar(self.cax[j])
                else:
                    self.cbar[j].set_clim(vmin = self.vmin, vmax = self.vmax)
        else:
            self.cax[-1] = self.axes[-1].imshow(self.images[-1],vmin = self.vmin, vmax = self.vmax,cmap = self.cmap)
            self.cbar[-1] = self.figures[-1].colorbar(self.cax[-1])

    def harmonize(self):
        '''
        Harmonizes the colorbars so that they actually correspond to the graphs.
        '''

        for j,cbar in enumerate(self.cbar):
            self.cbar[j].remove()
            self.cbar[j] = self.figures[j].colorbar(self.cax[j])



    def set_titles(self, title_list):
        '''
        Plot the titles associated to each image

        Parameters
        ----------
        title_list: list of titles to use for the images (has to be ordered)
        '''

        for j,title in enumerate(title_list):
            self.axes[j].set_title(title)

    def save_figs(self, name_list):
        '''
        saves the images into file of name inside the name_list

        Parameters
        ----------
        name_list: list of save_files to use as location for the images (has to be ordered)
        '''
        for j,save_name in enumerate(name_list):
            self.figures[j].savefig(save_name)






class subplots_arrangement():
    def __init__(self, figsize = (7,7), ptype = 'plot', **kwargs):
        '''
        subplots arrangement: a class to automatically generate subplots in the best arrangement possible
        while keeping the quantitative information preserved by displaying the information in the same scales.
        
                
        Parameters
        ----------
        figsize = (7,7)
        
        ptype = 'plot': choose between plot and imshow to display graphs or arrays/images
        '''
        self.figsize = figsize
        self.axes = []
        self.images = []
        self.cax = []
        self.cbar = []
        self.type = ptype
        if 'cmap' in kwargs:
            self.cmap = kwargs['cmap']
        else:
            self.cmap = 'hot'
        # if ptype == 'plots':
        #     function = 

    def plot_all(self, stack_elements, xs = None):
        '''
        Takes a stack of elements to plot or imshow and generate the best subplot pattern and display
        the elements while keeping the scale between them
        
        Parameters
        ----------
        stack_elements: list or np array (along dim 0) of elements to display
        
        xs: list or np array (along dim 0) of the x coordinate to use when using the plot mode
        '''
        
        num_elements = len(stack_elements)
        grid_y = np.int(np.round(np.sqrt(num_elements)))
        if xs:
            assert len(xs) == len(stack_elements)
        if grid_y**2 < num_elements:

            grid_x = np.int(np.ceil(num_elements/grid_y))
        else:
            grid_x = grid_y
        self.fig, self.ax = plt.subplots(grid_y,grid_x, figsize = self.figsize)
        self.ax = self.ax.ravel()
        max_val = np.max([np.max(element) for element in stack_elements]) #np.max(stack_elements)
        min_val = np.min([np.min(element) for element in stack_elements])

        for i,element in enumerate(stack_elements):
            if self.type == 'plot':
                if not(xs):
                    xs = [np.arange(len(element)) for element in stack_elements]
                self.ax[i].plot(xs[i],element)
                self.ax[i].set_ylim(min_val,max_val) 
            elif self.type == 'imshow':
                self.ax[i].imshow(element,vmin = min_val,vmax = max_val,cmap = self.cmap)




def make_anglemap( N = 256, use_hpl = True ):
    '''
    Allows to create a nice cyclic colormap, useful to display phase for example
    '''

    h = np.ones(N) # hue
    h[:N//2] = 11.6 # red 
    h[N//2:] = 258.6 # blue
    s = 100 # saturation
    l = np.linspace(0, 100, N//2) # luminosity
    l = np.hstack( (l,l[::-1] ) )

    colorlist = np.zeros((N,3))
    for ii in range(N):
        if use_hpl:
            colorlist[ii,:] = hsluv.hpluv_to_rgb( (h[ii], s, l[ii]) )
        else:
            colorlist[ii,:] = hsluv.hsluv_to_rgb( (h[ii], s, l[ii]) )
    colorlist[colorlist > 1] = 1 # correct numeric errors
    colorlist[colorlist < 0] = 0 
    return col.ListedColormap( colorlist )


def complex_array_to_hsv(cpx_array, theme='dark', rmax=None):
    '''Takes an array of complex numbers cpx_array and converts it to an array of [r, g, b],
    where phase gives hue and saturaton/value are given by the absolute value.
    Especially for use with imshow for complex plots.'''
    absmax = rmax or np.abs(cpx_array).max()
    Y = np.zeros(cpx_array.shape + (3,), dtype='float')
    Y[..., 0] = np.angle(cpx_array) / (2 * np.pi) % 1
    if theme == 'light':
        Y[..., 1] = np.clip(np.abs(cpx_array) / absmax, 0, 1)
        Y[..., 2] = 1
    elif theme == 'dark':
        Y[..., 1] = 1
        Y[..., 2] = np.clip(np.abs(cpx_array) / absmax, 0, 1)
    Y = matplotlib.colors.hsv_to_rgb(Y)
    return Y

def imshow_hsv(cpx_array,theme = 'dark',rmax = 'None'):
    '''
    Displays a cpx_array in hsv thanks to complex_array_to_hsv function
    '''
    fig = plt.figure()
    plt.imshow(complex_array_to_hsv(cpx_array))
    return fig



def img_nav(img_stack, cmap = 'hot', **kwargs):
    '''
    A class used to conveniently navigate through a stack of images img_stack with the keyboard arrows.
    '''
    class ChangeFig:
        def __init__(self,n,img,img_stack, **kwargs):
            self.curr_pos = 0
            self.img_stack = img_stack
            self.length= n
            self.img = img
            self.cid = img.figure.canvas.mpl_connect('key_press_event',self)
            if 'img_names' in kwargs and len(kwargs['img_names']) == len(img_stack):
                self.custom_names = True
                self.img_names = kwargs['img_names']
            else:
                self.custom_names = False


        def __call__(self,event):
            
            if event.key == "right":
                self.curr_pos = self.curr_pos + 1
            elif event.key == "left":
                self.curr_pos = self.curr_pos - 1
            elif event.key == "up":
                self.curr_pos = self.curr_pos + 100    
            elif event.key == "down":
                self.curr_pos = self.curr_pos - 100
            self.curr_pos = self.curr_pos % self.length

            self.img.set_data(self.img_stack[self.curr_pos])
            if self.custom_names:
                self.img.axes.set_title(f'{self.img_names[self.curr_pos]}')
            else:
                self.img.axes.set_title("Image number : %d" % self.curr_pos)

            self.img.figure.canvas.draw()

    if 'img_names' in kwargs and len(kwargs['img_names']) == len(img_stack):
        custom_names = True
    else:
        custom_names = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
    img = ax.imshow(img_stack[0],vmin = np.min(img_stack), vmax = np.max(img_stack),cmap = cmap)
    if custom_names:
        ax.set_title(f"{kwargs['img_names'][0]}")
    else:
        ax.set_title("Image number : 0")
    
    
    change_fig = ChangeFig(len(img_stack),img,img_stack, **kwargs)
    plt.show()
    
    
    
    
    
    
    
    
    
    
    

def plot_nav(plot_stack, color = 'r', **kwargs):
    '''
    A class used to conveniently navigate through a stack of images img_stack with the keyboard arrows.
    '''
    class ChangeFig:
        def __init__(self,n,curr_plot,plot_stack, **kwargs):
            self.curr_pos = 0
            self.plot_stack = plot_stack
            self.length= n
            self.curr_plot = curr_plot
            self.cid = curr_plot[0].figure.canvas.mpl_connect('key_press_event',self)
            if 'img_names' in kwargs and len(kwargs['plot_names']) == len(plot_stack):
                self.custom_names = True
                self.plot_names = kwargs['plot_names']
            else:
                self.custom_names = False


        def __call__(self,event):
            
            if event.key == "right":
                self.curr_pos = self.curr_pos + 1
            elif event.key == "left":
                self.curr_pos = self.curr_pos - 1
            elif event.key == "up":
                self.curr_pos = self.curr_pos + 100    
            elif event.key == "down":
                self.curr_pos = self.curr_pos - 100
            self.curr_pos = self.curr_pos % self.length

            self.curr_plot[0].set_data(np.arange(len(self.plot_stack[self.curr_pos])),self.plot_stack[self.curr_pos])
            if self.custom_names:
                self.curr_plot[0].axes.set_title(f'{self.plot_names[self.curr_pos]}')
            else:
                self.curr_plot[0].axes.set_title("Image number : %d" % self.curr_pos)

            self.curr_plot[0].figure.canvas.draw()

    if 'img_names' in kwargs and len(kwargs['plot_names']) == len(plot_stack):
        custom_names = True
    else:
        custom_names = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
    curr_plot = ax.plot(plot_stack[0], color = color)
    if 'xaxis' in kwargs:
        ax.set_xlim(kwargs['xaxis'][0], kwargs['xaxis'][1])
    if 'yaxis' in kwargs:
        ax.set_ylim(kwargs['yaxis'][0], kwargs['yaxis'][1])
    else:
        ax.set_ylim(np.min(plot_stack.ravel()), np.max(plot_stack.ravel()))
    if custom_names:
        ax.set_title(f"{kwargs['plot_names'][0]}")
    else:
        ax.set_title("Plot number : 0")
    
    
    change_fig = ChangeFig(len(plot_stack),curr_plot,plot_stack, **kwargs)
    plt.show()
    
    
    