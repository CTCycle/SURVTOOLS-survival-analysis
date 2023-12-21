import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


# define class for grid data plotting 
#==============================================================================
#==============================================================================
#============================================================================== 
class PlotBoard:

    def save_plot(self, path):        
        plt.savefig(path, bbox_inches='tight', format='jpeg', dpi=600)        
        plt.close()
    
    
    #==========================================================================
    def bar_graph(self, labels, values, y_name, title, color, path):
        plt.figure()
        plt.bar(labels, values, color = color, edgecolor='black')        
        plt.ylabel(y_name)        
        plt.title(title, y=1.2)
        plt.xticks(rotation=45, ha='right', va='top')
        plot_loc = os.path.join(path, '{}.jpeg'.format(title))
        plt.tight_layout()
        self.save_plot(plot_loc)

    #==========================================================================
    def multiple_boxplots(self, df, x, y, plot_title, y_label, filename, path, hue=None):
        
        df_melted = pd.melt(df, id_vars=[x], value_vars=y)        
        if hue is None:
            sns.boxplot(data=df_melted, x='variable', y='value', orient='v', palette='rainbow')
        else:
            sns.boxplot(data=df_melted, x='variable', y='value', hue=hue, orient='v', palette='rainbow')
        plt.ylabel(y_label)               
        plt.title(plot_title, y=1.2)    
        if hue is not None:
            plt.legend(loc='upper right', title=hue)        
        plt.xticks(rotation=0, ha='right', va='top')    
        plot_loc = os.path.join(path, '{}.jpeg'.format(filename))
        plt.tight_layout()
        plt.savefig(plot_loc, bbox_inches = 'tight', format ='jpeg', dpi = 600)       
        plt.close()


    #==========================================================================
    def scatter_plot(self, x_values, y_values, x_label, y_label, title, color, path):
        plt.figure()
        plt.scatter(x_values, y_values, color=color)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plot_loc = os.path.join(path, '{}.jpeg'.format(title))
        self.save_plot(plot_loc)

    #==========================================================================
    def heatmap_2D(self, df, col1, col2, title, path):
        cross_tab = pd.crosstab(df[col1], df[col2])
        plt.figure(figsize=(10, 7))
        sns.heatmap(cross_tab, annot=True, cmap="YlGnBu")
        plt.title(title)
        plot_loc = os.path.join(path, '{}.jpeg'.format(title))
        self.save_plot(plot_loc)