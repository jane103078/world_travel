# ***************************************************************
# Author: (Hsing-E Tsai)
# Lab: (Week6 Database)
# Date: (10/29/2025)
# Description: read database
# ***************************************************************


from logic.ContinentLists import ContinentLists

if __name__ == '__main__':
    all_cities, all_continentlists = ContinentLists.read_data()

    print()
    print("All cities:")
    for city in all_cities:
        print(city)
    print()
    print("All continentlists:")
    for continentlist in all_continentlists:
        print(continentlist)
