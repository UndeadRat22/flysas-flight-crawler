from flightinfo import FlightInfo
#pyquery doesn't seem to be able to parse the file
#something breaks internally
#from pyquery import PyQuery
from bs4 import BeautifulSoup
import re

def scrape_data(filename):
    with open(filename, "r") as html_file:
        html = html_file.read()
    #less s* to parse ~200kb/1k
    html = html.replace("\n", "").replace("Â", "")
    
    soup = BeautifulSoup(html, "html.parser")
    #get departure table
    departure_table = soup.find("table", class_ = "WDSEffect_table", id = "WDSEffect_table_0").find("tbody").find_all("tr")

    all_prices = {}
    for departure_container in departure_table:
        if "id" not in departure_container.attrs:
            continue
        __id = departure_container.attrs["id"]
        prices_wrapper = departure_container.find_all("td", class_ = "fare")
        flight_prices = []
        for wrapped_price in prices_wrapper:
            price = wrapped_price.find("div", class_ = "choice")
            price = price.find("span", class_ = "price")
            price = price.find("span", class_ = "number")

            price_string = price.attrs["data-price"]
            flight_prices.append(price_string)
        if len(flight_prices) > 0:
            all_prices[__id] = flight_prices

    for f in all_prices.items():
        print(f)
        #print(departure_container.text)

    #dep_table_soup = BeautifulSoup(departure_table.html(), "html.parser")
    #trs = dep_table_soup.find_all("tr")
    #for tr in trs:
    #    print(tr.text())


if __name__ == "__main__":
    scrape_data("D:\\temp\\index.html")