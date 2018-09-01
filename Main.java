package org.deadrat22;

import java.io.IOException;

public class Main {

    public static final String URL = "https://classic.flysas.com/en/us/";

    public static void main(String[] args) throws IOException {

        FlysasBrowser browser = new FlysasBrowser();
        browser.loadPage(URL, 5000);

        browser.selectAirports("ARN", "LHR");
        browser.selectDates("2018-10-08", "2018-10-14");
        browser.selectPassengerCount(1, 0, 0);

        System.out.println("Starting search");
        browser.startSearch();
        System.out.println("Done");
    }
}
