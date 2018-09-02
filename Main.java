package org.deadrat22;

public class Main {

    public static final String URL = "https://classic.flysas.com/en/us/";

    public static void main(String[] args) throws Exception {

        FlysasBrowser browser = new FlysasBrowser();
        browser.loadPage(URL, 5000);

        browser.selectAirports("ARN", "LHR");
        browser.selectDates("2018-10-08", "2018-10-14");
        browser.selectPassengerCount(1, 0, 0);

        System.out.println("Search Start");
        browser.startSearch(5000);
        System.out.println("Search Done");

        browser.writeCurrentPageToFile("D:\\temp\\index.html");
        Cmd cmd = new Cmd();
        cmd.run();
    }
}
