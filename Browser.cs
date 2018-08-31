using NHtmlUnit;
using NHtmlUnit.Html;
using NHtmlUnit.Javascript.Host.Events;

namespace deadrat22
{
    class FlysasClient
    {

        private string idDepartureLocation = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_predictiveSearch_hiddenFrom";
        private string idArrivalLocation = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_predictiveSearch_hiddenTo";
        private string idAdultCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeAdult";
        private string idChildCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeChild211";
        private string idInfantCount = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepPassengerTypes_passengerTypeInfant";
        private string idDepartureDate = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepCalendar_hiddenOutbound";
        private string idReturnDate = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_cepCalendar_hiddenReturn";

        private string idButton = "ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_Searchbtn_ButtonLink";

        private WebClient webClient;

        private HtmlPage currentPage;
        public HtmlPage CurrentPage { get { return currentPage; } }

        public FlysasClient(string url)
        {
            webClient = new WebClient(BrowserVersion.EDGE);

            webClient.Options.JavaScriptEnabled = true;
            webClient.Options.RedirectEnabled = true;
            webClient.Options.ThrowExceptionOnScriptError = false;
            webClient.Options.ThrowExceptionOnFailingStatusCode = false;

            webClient.WaitForBackgroundJavaScript(10000);

            currentPage = webClient.GetPage(url) as HtmlPage;
        }

        public void SetDepartureAirport(string airport)
        {
            ((HtmlHiddenInput)currentPage.GetElementById(idDepartureLocation)).SetValueAttribute(airport);
        }
        public void SetArrivalAirport(string airport)
        {
            ((HtmlHiddenInput)currentPage.GetElementById(idArrivalLocation)).SetValueAttribute(airport);
        }
        public void SetDepartureDate(string date)
        {
            ((HtmlHiddenInput)currentPage.GetElementById(idDepartureDate)).SetValueAttribute(date);
        }
        public void SetReturnDate(string date)
        {
            ((HtmlHiddenInput)currentPage.GetElementById(idReturnDate)).SetValueAttribute(date);
        }
        public void SetAdultCount(int count)
        {
            ((HtmlSelect)currentPage.GetElementById(idAdultCount)).GetOptionByValue(count.ToString());
        }
        public void SetChildCount(int count)
        {
            ((HtmlSelect)currentPage.GetElementById(idChildCount)).GetOptionByValue(count.ToString());
        }
        public void SetInfantCount(int count)
        {
            ((HtmlSelect)currentPage.GetElementById(idInfantCount)).GetOptionByValue(count.ToString());

        }

        public void SubmitSearchForm()
        {
            var button = currentPage.GetHtmlElementById("ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_Searchbtn_ButtonLink");
            if (button == null)
                return;
            currentPage = (button.Click() as HtmlPage);
            webClient.AjaxController = new NicelyResynchronizingAjaxController();
            webClient.WaitForBackgroundJavaScript(1500);
            webClient.WaitForBackgroundJavaScriptStartingBefore(1500);
            System.Threading.Thread.Sleep(5000);

            var windows = webClient.WebWindows;
            foreach (var w in windows)
            {
                var html = w.EnclosedPage as HtmlPage;
                System.Console.WriteLine(html.AsXml());
            }
        }
    }
}
