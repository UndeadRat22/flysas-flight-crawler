from flightinfo import FlightInfo
#pyquery doesn't seem to be able to parse the file
#something breaks internally
#from pyquery import PyQuery
from bs4 import BeautifulSoup
import re

def scrape_data(html, table_index):
    __soup = BeautifulSoup(html, "html.parser")
    #get departure table
    __table_id = "WDSEffect_table_" + str(table_index)
    __table = __soup.find("table", class_ = "WDSEffect_table", id = __table_id).find("tbody").find_all("tr")

    all_data = {}
    __id = None
    for departure_container in __table:
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
            all_data[__id] = prices
            continue
        
        if ((c == ["flight", "segments", "EffectOff", "EffectOff_nofamily"])
        or (c == ['flight', 'segments', 'SelectedEffectOff', 'SelectedEffectOff_family1'])):
            connection_airport = get_stop(departure_container)
            all_data[__id].append(connection_airport)
            continue
    
    return all_data

def construct_flight_infos(flights, price_map):
    infos = []
    for _id, attribs in flights.items():
        price = min_from_list(attribs[0])
        dep_time = attribs[1]
        arr_time = attribs[2]
        dep_port = attribs[3]
        arr_port = attribs[4]
        con_port = attribs[5]
        tax = price_map[price]
        infos.append(FlightInfo(dep_time, arr_time, price, tax, dep_port, arr_port, con_port))
    return infos

def min_from_list(list):
    _min = list[0]
    for num in list:
        _min = min(_min, num)
    return _min

def create_price_dict(html):
    #the Most Magnificent Regex
    recs = re.findall(r"recommendation\[\'ADT\'\] = \{\'price\':\'[0-9]*\.[0-9]*\',\'tax\':\'[0-9]*\.[0-9]*\',\'priceWithoutTax\':\'[0-9]*\.[0-9]*\',\'fee\':\'[0-9]*\.[0-9]\'", html)
    _dict = {}
    for rec in recs:
        nums = re.findall(r"[0-9]*\.[0-9]*", rec)
        _dict[nums[0]] = nums[1]
    return _dict

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
        if not price:
            continue
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
    with open("D:\\temp\\index.html", "r") as html_file:
        html = html_file.read()
    #less s* to parse 1000kb -> 800kb
    html = html.replace("\n", "").replace("Â", "")
    
    #TODO all of the scraping could be done in parallel
    price_map = create_price_dict(html)
    
    out_scraped = scrape_data(html, 0)
    ret_scraped = scrape_data(html, 1)
    print("_______________________________\n|---outbound------------------|\n_______________________________")
    outbound = construct_flight_infos(out_scraped, price_map)
    for info in outbound:
        print(str(info))
    
    returns = construct_flight_infos(ret_scraped, price_map)
    print("_______________________________\n|---return--------------------|\n_______________________________")
    for info in returns:
        print(str(info))
