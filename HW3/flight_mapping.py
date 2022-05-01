from cProfile import label
from turtle import color
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


def extract_data():
    """
    Extract cordinates from airports information
    Return: 2x 3-dimension lists of post data and current data
    """
    # Store Post covid flights dataframe
    df_post = pd.read_csv('CSV/post_covid_flights.csv', sep=';')
    # Store Current flights dataframe
    df_curr = pd.read_csv('CSV/curr_flights.csv', sep=';')
    # Store Airports information dataframe
    df_airports = pd.read_csv('CSV/airports.csv', sep=',')

    # Store each IATA codes
    post_IATA = df_post['IATA'].tolist()
    curr_IATA = df_curr['IATA'].tolist()

    # Find Mutched IATA and Area(Europe) from Airports DF and store cordinates
    post_crdn = []
    for iata in post_IATA:
        tmp = df_airports[df_airports['IATA'].str.contains(
            iata, regex=False) & df_airports['DZ'].str.contains('Europe', regex=False)]
        if len(tmp) == 0:
            continue
        crdn = []
        crdn.append(tmp['City'].values[0])
        crdn.append(tmp['Longitude'].values[0])
        crdn.append(tmp['Latitude'].values[0])
        post_crdn.append(crdn)

    curr_crdn = []
    for iata in curr_IATA:
        tmp = df_airports[df_airports['IATA'].str.contains(
            iata, regex=False) & df_airports['DZ'].str.contains('Europe', regex=False)]
        if len(tmp) == 0:
            continue
        crdn = []
        crdn.append(tmp['City'].values[0])
        crdn.append(tmp['Longitude'].values[0])
        crdn.append(tmp['Latitude'].values[0])
        curr_crdn.append(crdn)

    # print(post_crdn)
    # print(curr_crdn)
    return post_crdn, curr_crdn


def plot_data(post_crdn, curr_crdn):
    """
    Plot cordinates on the map of Europe
    """
    # Get Cordinate of TLL and remove it
    tll_crdn = post_crdn[0]
    post_crdn.pop()
    curr_crdn.pop()

    proj = ccrs.Miller()
    ax = plt.axes(projection=proj)
    ax.set_extent([-13, 45, 30, 70])
    ax.stock_img()
    ax.add_feature(cf.COASTLINE, lw=2)
    ax.add_feature(cf.BORDERS)

    # Plot post covid flights with blue color
    for crdn in post_crdn:
        ax.plot([tll_crdn[1], crdn[1]], [tll_crdn[2], crdn[2]],
                color='blue', linewidth=2, marker='o',
                transform=ccrs.Geodetic(),)
        plt.text(crdn[1], crdn[2] - 0.5, crdn[0],
                 horizontalalignment='right',
                 transform=ccrs.Geodetic(),)

    # Plot post covid flights with red color
    for crdn in curr_crdn:
        ax.plot([tll_crdn[1], crdn[1]], [tll_crdn[2], crdn[2]],
                color='red', linewidth=2, marker='o',
                transform=ccrs.Geodetic(),)
        plt.text(crdn[1], crdn[2] - 0.5, crdn[0],
                 horizontalalignment='right',
                 transform=ccrs.Geodetic())

    blue = mpatches.Patch(facecolor='blue', label='Post Covid19 Flights')
    red = mpatches.Patch(facecolor='red', label='Current Flights')
    legend = plt.legend(
        handles=[
            blue,
            red],
        loc=4,
        fontsize='small',
        fancybox=True)
    plt.title("Flights from Tallinn: Post Covid19 and Current")
    # Make figure larger
    plt.gcf().set_size_inches(20, 10)
    # Save figure as PNG
    plt.savefig("FlightMap.png")


def main():
    post_crdn, curr_crdn = extract_data()
    plot_data(post_crdn, curr_crdn)


if __name__ == '__main__':
    main()
