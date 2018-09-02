# flysas-flight-crawler
task:
- You need to collect departure airport, arrival airport, connection airport, departure time, arrival time, cheapest price and taxes for all flight combinations from ARN (Stockholm) to LHR (London) departing 2018-10-08 and returning 2018-10-14. Only data for flights that are direct or have a connection at Oslo should be accepted.

workflow:
- the java program manages all of the work.
- the java program downloads the webpage with given parameters
- the java program saves the page to a location on the HDD (set to "D:\temp\index.html")
- the java calls python through windows cmd (python code path is set to "D:\_root\programming\Python\infare\flysas\")
- the python program parses the html file using BeautifulSoup and regular expressions and outputs to cmd
- the java program reads the python output and redirects to stdout
