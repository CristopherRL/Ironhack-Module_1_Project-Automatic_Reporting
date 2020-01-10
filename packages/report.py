######################################### IMPORTING LIBRARIES #################################################
import matplotlib.pyplot as plt

def plotting_data(table,top): ### IF I HAVE PROBLEMS WITH TOP, DELETE IT
    meanW_GDPP = table
    x = list(meanW_GDPP.country)
    y = list(meanW_GDPP.ratio_MUSD)

    fig = meanW_GDPP.plot(kind='barh', x='country', y='ratio_MUSD').get_figure()

    plt.xlabel('ratio_MUSD')
    plt.title(f'Top {top}_Comparing Billionaries with GDP by Industry')
    plt.grid(True)

    path = f'../data/results/Top{top}_Billionaries_by_Industry.pdf'
    fig.savefig(path)

    #return plot ## ???