using NHtmlUnit;
using NHtmlUnit.Html;

namespace deadrat22
{
    class Program
    {
        static void Main(string[] args)
        {
            string url = "https://classic.flysas.com/en/us/";
            FlysasClient browser = new FlysasClient(url);
            browser.SetAdultCount(1);
            browser.SetInfantCount(0);
            browser.SetChildCount(0);

            browser.SetDepartureAirport("ARN");
            browser.SetArrivalAirport("LHR");
            browser.SetDepartureDate("2018-10-08");
            browser.SetReturnDate("2018-10-14");

            browser.SubmitSearchForm();

            //var html = browser.CurrentPage.AsXml();
            //System.Console.WriteLine(html);
        }
    }
}
