######################################### IMPORTING LIBRARIES #################################################
import matplotlib.pyplot as plt

def plotting_data(table,top):

    meanW_GDPP = table

    fig = meanW_GDPP.plot(kind='barh', x='country', y='ratio_MUSD').get_figure()
    plt.xlabel('ratio_M')
    plt.ylabel('countries')
    plt.title(f'TOP {top} - Comparing Mean Worth vs GDP per capita by Country')
    plt.grid(True)
    plt.show()
    fig.savefig(f'data/results/TOP{top}-Billionaries_by_Industry.png')

    print(f'Plot has been saved! The file is located in: data/results/TOP{top}-Billionaries_by_Country.png')