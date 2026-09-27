import os
from typing import List, Dict
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


class SearchService:
    def search(self, query: str) -> List[Dict]:
        raise NotImplementedError


class SerpAPISearchService(SearchService):

    BASE_URL = "https://serpapi.com/search"

    TRUSTED_DOMAINS = {
        
  "reuters.com": "High",
  "apnews.com": "High",
  "bbc.com": "High",
  "who.int": "Very High",
  "cdc.gov": "Very High",
  "nih.gov": "Very High",
  "nasa.gov": "Very High",
  "factcheck.org": "High",
  "snopes.com": "High",
  "politifact.com": "High",
  "fullfact.org": "High",
  "afp.com": "High",
  "bloomberg.com": "High",
  "nature.com": "Very High",
  "science.org": "Very High",
  "nejm.org": "Very High",
  "thelancet.com": "Very High",
  "pnas.org": "Very High",
  "pubmed.ncbi.nlm.nih.gov": "Very High",
  "jstor.org": "Very High",
  "sciencedirect.com": "Very High",
  "springer.com": "Very High",
  "wiley.com": "Very High",
  "ox.ac.uk": "Very High",
  "cam.ac.uk": "Very High",
  "mit.edu": "Very High",
  "harvard.edu": "Very High",
  "stanford.edu": "Very High",
  "un.org": "Very High",
  "worldbank.org": "Very High",
  "imf.org": "Very High",
  "oecd.org": "Very High",
  "wto.org": "Very High",
  "wmo.int": "Very High",
  "ipcc.ch": "Very High",
  "noaa.gov": "Very High",
  "usgs.gov": "Very High",
  "fda.gov": "Very High",
  "epa.gov": "Very High",
  "loc.gov": "Very High",
  "archives.gov": "Very High",
  "census.gov": "Very High",
  "bls.gov": "Very High",
  "statista.com": "High",
  "ourworldindata.org": "High",
  "pewresearch.org": "High",
  "gallup.com": "High",
  "poynter.org": "High",
  "ifcncodeofprinciples.poynter.org": "High",
  "leadstories.com": "High",
  "checkyourfact.com": "High",
  "climatefeedback.org": "High",
  "healthfeedback.org": "High",
  "sciencefeedback.co": "High",
  "africacheck.org": "High",
  "altnews.in": "High",
  "boomlive.in": "High",
  "verafiles.org": "High",
  "chequeado.com": "High",
  "factcheckni.org": "High",
  "theferret.scot": "High",
  "correctiv.org": "High",
  "lemonde.fr": "High",
  "faz.net": "High",
  "dw.com": "High",
  "france24.com": "High",
  "wsj.com": "High",
  "ft.com": "High",
  "economist.com": "High",
  "nytimes.com": "High",
  "washingtonpost.com": "High",
  "theguardian.com": "High",
  "npr.org": "High",
  "pbs.org": "High",
  "c-span.org": "High",
  "theconversation.com": "High",
  "scientificamerican.com": "High",
  "newscientist.com": "High",
  "nationalgeographic.com": "High",
  "smithsonianmag.com": "High",
  "aljazeera.com": "High",
  "cbc.ca": "High",
  "abc.net.au": "High",
  "kyodonews.net": "High",
  "propublica.org": "High",
  "icij.org": "High",
  "occrp.org": "High",
  "bellingcat.com": "High",
  "cfr.org": "High",
  "brookings.edu": "High",
  "csis.org": "High",
  "rand.org": "High",
  "chathamhouse.org": "High",
  "carnegieendowment.org": "High",
  "india.gov.in": "Very High",
  "pib.gov.in": "Very High",
  "factcheck.pib.gov.in": "Very High",
  "mygov.in": "Very High",
  "isro.gov.in": "Very High",
  "drdo.gov.in": "Very High",
  "rbi.org.in": "Very High",
  "eci.gov.in": "Very High",
  "main.sci.gov.in": "Very High",
  "nic.in": "Very High",
  "meity.gov.in": "Very High",
  "mea.gov.in": "Very High",
  "mha.gov.in": "Very High",
  "finmin.nic.in": "Very High",
  "mohfw.gov.in": "Very High",
  "icmr.gov.in": "Very High",
  "education.gov.in": "Very High",
  "moef.gov.in": "Very High",
  "upsc.gov.in": "Very High",
  "cbse.gov.in": "Very High",
  "ugc.gov.in": "Very High",
  "aicte-india.org": "Very High",
  "nta.ac.in": "Very High",
  "incometax.gov.in": "Very High",
  "gst.gov.in": "Very High",
  "uidai.gov.in": "Very High",
  "passportindia.gov.in": "Very High",
  "parliamentofindia.nic.in": "Very High",
  "sansad.in": "Very High",
  "presidentofindia.nic.in": "Very High",
  "pmindia.gov.in": "Very High",
  "censusindia.gov.in": "Very High",
  "mospi.gov.in": "Very High",
  "niti.gov.in": "Very High",
  "data.gov.in": "Very High",
  "epfindia.gov.in": "Very High",
  "sebi.gov.in": "Very High",
  "trai.gov.in": "Very High",
  "irda.gov.in": "Very High",
  "cci.gov.in": "Very High",
  "nhrc.nic.in": "Very High",
  "ncw.nic.in": "Very High",
  "ndma.gov.in": "Very High",
  "imd.gov.in": "Very High",
  "bis.gov.in": "Very High",
  "fssai.gov.in": "Very High",
  "lawmin.gov.in": "Very High",
  "indiacode.nic.in": "Very High",
  "egazette.gov.in": "Very High",
  "prasarbharati.gov.in": "High",
  "newsonair.gov.in": "High",
  "ddnews.gov.in": "High",
  "ptinews.com": "High",
  "aninews.in": "High",
  "thehindu.com": "High",
  "thehindubusinessline.com": "High",
  "indianexpress.com": "High",
  "hindustantimes.com": "High",
  "timesofindia.indiatimes.com": "High",
  "economictimes.indiatimes.com": "High",
  "livemint.com": "High",
  "business-standard.com": "High",
  "financialexpress.com": "High",
  "ndtv.com": "High",
  "indiatoday.in": "High",
  "aajtak.in": "High",
  "abplive.com": "High",
  "news18.com": "High",
  "cnbctv18.com": "High",
  "zeenews.india.com": "High",
  "wionews.com": "High",
  "theprint.in": "High",
  "thewire.in": "High",
  "scroll.in": "High",
  "newslaundry.com": "High",
  "factchecker.in": "High",
  "vishvasnews.com": "High",
  "thip.media": "High",
  "newschecker.in": "High",
  "logicallyfacts.com": "High",
  "digitallibrary.un.org": "Very High",
  "ec.europa.gov": "Very High",
  "oas.org": "Very High",
  "interpol.int": "Very High",
  "icj-cij.org": "Very High",
  "wipo.int": "Very High",
  "unesco.org": "Very High",
  "unicef.org": "Very High",
  "unhcr.org": "Very High",
  "undp.org": "Very High",
  "iom.int": "Very High",
  "iaea.org": "Very High",
  "ilo.org": "Very High",
  "bis.org": "Very High",
  "oecd-ilibrary.org": "Very High",
  "worldbank.org/en/research": "Very High",
  "royalsocietypublishing.org": "Very High",
  "cell.com": "Very High",
  "jamanetwork.com": "Very High",
  "bmj.com": "Very High",
  "tandfonline.com": "Very High",
  "frontiersin.org": "Very High",
  "mdpi.com": "High",
  "plos.org": "Very High",
  "arxiv.org": "High",
  "biorxiv.org": "High",
  "medrxiv.org": "High",
  "ssrn.com": "High",
  "nber.org": "Very High",
  "cepr.org": "Very High",
  "iiss.org": "High",
  "sipri.org": "Very High",
  "transparency.org": "High",
  "amnesty.org": "High",
  "hrw.org": "High",
  "rsf.org": "High",
  "cpj.org": "High",
  "freedomhouse.org": "High",
  "eiu.com": "High",
  "statcan.gc.ca": "Very High",
  "ons.gov.uk": "Very High",
  "abs.gov.au": "Very High",
  "destatis.de": "Very High",
  "insee.fr": "Very High",
  "scmp.com": "High",
  "japantimes.co.jp": "High",
  "straitstimes.com": "High",
  "koreaherald.com": "High",
  "sbs.com.au": "High",
  "globo.com": "High",
  "elpais.com": "High",
  "corriere.it": "High",
  "spiegel.de": "High",
  "zeit.de": "High",
  "swissinfo.ch": "High",
  "nzz.ch": "High",
  "rtve.es": "High",
  "svt.se": "High",
  "nrk.no": "High",
  "yle.fi": "High",
  "channelnewsasia.com": "High",
  "southasiamonitor.org": "High",
  "wikipedia.org": "Medium",
  "wikiquote.org": "Medium",
  "wikidata.org": "Medium"


    }

    def _credibility(self, url: str) -> str:
        try:
            domain = urlparse(url).netloc.lower().replace("www.", "")

            if domain.endswith(".gov"):
                return "Official"

            if domain.endswith(".edu"):
                return "Academic"

            return self.TRUSTED_DOMAINS.get(domain, "Unknown")

        except Exception:
            return "Unknown"

    def _google_search(self, query: str):

        response = requests.get(
            self.BASE_URL,
            params={
                "engine": "google",
                "q": query,
                "api_key": SERPAPI_KEY,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def _google_news(self, query: str):

        response = requests.get(
            self.BASE_URL,
            params={
                "engine": "google_news",
                "q": query,
                "api_key": SERPAPI_KEY,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def search(self, query: str) -> List[Dict]:

        evidence = []
        seen = set()

        try:
            google = self._google_search(query)

            for item in google.get("organic_results", []):

                url = item.get("link")

                if not url or url in seen:
                    continue

                seen.add(url)

                evidence.append(
                    {
                        "title": item.get("title", ""),
                        "url": url,
                        "snippet": item.get("snippet", ""),
                        "source": urlparse(url).netloc.replace("www.", ""),
                        "published_date": "",
                        "credibility": self._credibility(url),
                    }
                )

        except Exception as e:
            print("Google Search Error:", e)

        try:
            news = self._google_news(query)

            for item in news.get("news_results", []):

                url = item.get("link")

                if not url or url in seen:
                    continue

                seen.add(url)

                evidence.append(
                    {
                        "title": item.get("title", ""),
                        "url": url,
                        "snippet": item.get("snippet", ""),
                        "source": item.get("source") or urlparse(url).netloc.replace("www.", ""),
                        "published_date": item.get("date", ""),
                        "credibility": self._credibility(url),
                    }
                )

        except Exception as e:
            print("Google News Error:", e)

        return evidence[:10]


search_service = SerpAPISearchService()
