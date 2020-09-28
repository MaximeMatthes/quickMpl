import matplotlib.pyplot as plt
import numpy as np

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
