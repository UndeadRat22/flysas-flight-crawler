package org.deadrat22;

import com.gargoylesoftware.htmlunit.*;
import com.gargoylesoftware.htmlunit.html.*;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import java.util.logging.Level;

public class FlysasBrowser {
    //airports
    private String idDepartureLocation = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_predictiveSearch_hiddenFrom";
    private String idArrivalLocation = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_predictiveSearch_hiddenTo";
    //dates
    private String idDepartureDate = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepCalendar_hiddenOutbound";
    private String idReturnDate = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepCalendar_hiddenReturn";
    //passengers
    private String idAdultCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeAdult";
    private String idChildCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeChild211";
    private String idInfantCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeInfant";
    //search button
    private String idButton = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_Searchbtn_ButtonLink";

    private WebClient webClient;

    public FlysasBrowser() {
        java.util.logging.Logger.getLogger("com.gargoylesoftware").setLevel(Level.OFF);

        webClient = new WebClient(BrowserVersion.CHROME);

        webClient.getOptions().setJavaScriptEnabled(true);
        webClient.getOptions().setThrowExceptionOnScriptError(false);
        webClient.getOptions().setThrowExceptionOnFailingStatusCode(false);
        webClient.getOptions().setRedirectEnabled(true);
    }

    public void loadPage(String url, long javascriptTime) throws IOException{
        webClient.getPage(url);
        webClient.waitForBackgroundJavaScript(javascriptTime);
    }

    public void startSearch(long javascriptTime) throws IOException {
        HtmlElement button = (HtmlElement) currentPage().getElementById(idButton);
        button.click();
        webClient.setAjaxController(new NicelyResynchronizingAjaxController());
        webClient.waitForBackgroundJavaScript(javascriptTime);
        webClient.waitForBackgroundJavaScriptStartingBefore(javascriptTime);
    }

    public void selectPassengerCount(int adult, int child, int infant) throws NullPointerException{
        String adultstr = Integer.toString(adult);
        String childstr = Integer.toString(child);
        String infantstr = Integer.toString(infant);
        HtmlPage page = currentPage();
        ((HtmlSelect) page.getElementById(idAdultCount)).getOptionByValue(adultstr);
        ((HtmlSelect) page.getElementById(idChildCount)).getOptionByValue(childstr);
        ((HtmlSelect) page.getElementById(idInfantCount)).getOptionByValue(infantstr);
    }

    public void selectAirports(String departure, String arrival) throws NullPointerException{
        HtmlPage page = currentPage();
        ((HtmlHiddenInput) page.getElementById(idDepartureLocation)).setValueAttribute(departure);
        ((HtmlHiddenInput) page.getElementById(idArrivalLocation)).setValueAttribute(arrival);
    }

    public void selectDates(String departure, String return_) throws NullPointerException{
        HtmlPage page = currentPage();
        ((HtmlHiddenInput) page.getElementById(idDepartureDate)).setValueAttribute(departure);
        ((HtmlHiddenInput) page.getElementById(idReturnDate)).setValueAttribute(return_);
    }

    public HtmlPage currentPage() throws NullPointerException{
        return (HtmlPage) webClient.getWebWindows().get(0).getEnclosedPage();
    }

    public void writeCurrentPageToFile(String filename) throws IOException{
        String html = currentPage().asXml();
        BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
        writer.write(html);
        writer.flush();
        writer.close();
    }

}
