__author__ = "Igor Andreoni"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def createGanttChart(filename, bandNames, posBands):
    """Create a Gantt chart of observatories with their timelines.

    Parameters
    ----------
    filename: str
        file name with a list of observatories, with upper and lower
        boundaries (int) for the timeline and the type of band.
        Example of three lines in the file:
        A-LIGO,2023,2050,gw
        A-Virgo,2023,2050,gw
        Keck,2018,2050,oir
    bandNames: list of str
        List of names of the messenger or EM band
    posBands: list of float
        List of positions for the bands in the plot
    """
    # Initialize some variables for lists
    ylabels = []
    customDates = []

    # Read the input file
    try:
        textlist = open(filename).readlines()
    except FileNotFoundError:
        print(f"Input file {filename} not found")
        return

    for tx in textlist:
        if not tx.startswith('#'):
            ylabel, startdate, enddate, band = tx.split(',')
            ylabels.append(ylabel)
            customDates.append([int(startdate), int(enddate),
                                band.replace("\n", '')])
    ilen = len(ylabels)
    pos = np.arange(0.5, ilen*0.5+0.5, 0.5)
    facility_dates = {}
    for i, facility in enumerate(ylabels):
        facility_dates[facility] = customDates[i]

    # Initiate the plot
    fig = plt.figure(figsize=(17, 20))

    # Band names
    fig.subplots_adjust(wspace=0, hspace=0)
    ax2 = plt.subplot2grid((1, 5), (0, 4), rowspan=1, colspan=1)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    # Add band names
    for b, p in zip(bandNames, posBands):
        ax2.text(0.1, 1-p/10., b, fontsize=20)

    # Timeline
    ax = plt.subplot2grid((1, 5), (0, 0), rowspan=1, colspan=4)
    for i in range(len(ylabels)):
        start_date, end_date, b = facility_dates[ylabels[i]]

        if b == 'gw':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='purple',
                    color='purple', alpha=0.8, label='Gravitational Waves')
        if b == 'cr':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='black',
                    color='white', alpha=0.8, label='Cosmic Rays')
        if b == 'n':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='grey',
                    color='grey', alpha=0.8, label='Neutrinos')
        if b == 'g':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='blue',
                    color='blue', alpha=0.8, label='Gamma-Rays')
        if b == 'x':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='green',
                    color='green', alpha=0.8, label='X-Rays')
        if b == 'oir':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='brown',
                    color='yellow', alpha=0.8, label='Optical/IR')
        if b == 'mm':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='orange',
                    color='orange', alpha=0.8, label='Millimeter')
        if b == 'r':
            ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date,
                    height=0.3, align='center', edgecolor='red',
                    color='red', alpha=0.7, label='Radio')

    # Plot labels
    locsy, labelsy = plt.yticks(pos, ylabels)
    plt.setp(labelsy, fontsize=20)

    # Add a grid
    ax.grid(color='grey', linestyle=':')

    # Axis labels
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=30, fontsize=20)
    ax.set_xlim([2024, 2040])

    # Invert the Y axis
    ax.invert_yaxis()

    # Make the tick labels integers (years)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Add credits
    ax2.text(0.3, -0.025, "Created by", color='grey', fontsize=15)
    ax2.text(0.3, -0.04, "I. Andreoni (JSI)", color='grey', fontsize=15)

    plt.savefig('gantt.pdf', bbox_inches='tight')

    # Open the image
    import os
    os.system("open gantt.pdf&")


if __name__ == '__main__':
    filename = "timeline.txt"

    # List of with Multi-Messenger band names
    bandNames = ['Gravitational', 'Waves', 'Cosmic Rays', 'Neutrinos',
                 'Gamma-Rays', 'X-Rays', 'Ultraviolet', 'Optical',
                 'Infrared', 'Millimeter', 'Radio']
    # Position of the bands in the plot
    posBands = [0.9, 1.1, 2.0, 3., 4.2, 5.3, 6.7, 7.0, 7.3, 8.43, 9.1]

    # Call the main function to generate the Gantt chart
    createGanttChart(filename, bandNames, posBands)
