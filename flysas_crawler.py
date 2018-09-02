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
    __id = None
    for departure_container in departure_table:
        #check if there's a class name, if not, we skippedy skip
        if "class" not in departure_container.attrs:
            continue
        c = departure_container.attrs["class"]
        #ignore the empty containers
        if "empty" in c:
            continue
        #set the __id variable if we're working on some obj
        if "id" in departure_container.attrs:
            __id = departure_container.attrs["id"]
        if ((c == ["flight", "EffectOff", "EffectOff_nofamily", "segmented"])
        or (c == ['flight', 'segmented', 'SelectedEffectOff', 'SelectedEffectOff_family1'])):
            prices = get_flightdata(departure_container)
            all_prices[__id] = prices
            continue
        
        if ((c == ["flight", "segments", "EffectOff", "EffectOff_nofamily"])
        or (c == ['flight', 'segments', 'SelectedEffectOff', 'SelectedEffectOff_family1'])):
            connection_airport = get_stop(departure_container)
            all_prices[__id].append(connection_airport)
            continue
    #TODO use [a-zA-z] and {x} instead of this badboi
    recommends = get_recommendation_list(html, r"recommendation\[\'ADT\'\] = \{\'price\':\'[0-9]*\.[0-9]*\',\'tax\':\'[0-9]*\.[0-9]*\',\'priceWithoutTax\':\'[0-9]*\.[0-9]*\',\'fee\':\'[0-9]*\.[0-9]\'")
    for departure in all_prices.items():
        print(departure)
    for r in recommends:
        print(r)
    
def get_recommendation_list(html_text, block_pattern):
    return re.findall(block_pattern, html_text)


def get_stop(container):
    stop_wrapper = container.find("td").find("div").find("table").find("tbody")
    flightinfos = stop_wrapper.find_all("tr", class_ = "flightInfo")
    for info in flightinfos:
        stop = info.find("td", class_ = "stopover")
        if not stop:
            continue
        stop = stop.find("div").find("span", class_ = "label")
        if not stop:
            continue
        pattern = "Stop over at: [A-Z].*[a-z]"
        text = stop.text
        stop_port = re.findall(pattern, text)[0].replace("Stop over at: ", "")
        return stop_port

def get_flightdata(container):
    prices_wrapper = container.find_all("td", class_ = "fare")
    flight_prices = []
    for wrapped_price in prices_wrapper:
        price = wrapped_price.find("div", class_ = "choice")
        price = price.find("span", class_ = "price")
        price = price.find("span", class_ = "number")

        if "data-price" not in price.attrs:
            continue
        price_string = price.attrs["data-price"]
        flight_prices.append(price_string)
    time_wrapper = container.find("td", class_ = "time")
    times = time_wrapper.find_all("span", class_ = "time")
    starttime = times[0].text.replace(" ", "")
    endtime = times[1].text.replace(" ", "")

    airport_wrapper = container.find("td", class_ = "airport")
    airports = airport_wrapper.find_all("acronym", class_ = "airport")
    #haven't seen any spaces but just incase
    startport = airports[0].text.replace(" ", "")
    endport = airports[1].text.replace(" ", "")

    return [flight_prices, starttime, endtime, startport, endport]

if __name__ == "__main__":
    scrape_data("D:\\temp\\index.html")