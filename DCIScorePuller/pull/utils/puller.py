import requests
import sys
import re
import urllib
from bs4 import BeautifulSoup

class DciScorePuller:
    def __init__(self, season=2023):
        self.season = season
        self.shows_url = """https://www.dci.org/scores?season=%d""" % season
        self.full_recap_scores_url = """https://www.dci.org/scores/recap"""
        self.final_overview_scores_url = """https://www.dci.org/scores/final-scores"""

    def get_html_bytes(self, url):
        orginal_stdout = sys.stdout
        with urllib.request.urlopen(url) as WebPageResponse:
            contents = WebPageResponse.read()
            sys.stdout = orginal_stdout
        return contents

    def get_shows(self):
        shows = []

        soup = BeautifulSoup(self.get_html_bytes(url=self.shows_url), "html5lib")
        pagination = soup.find_all("div", {"class": "pagination"})
        total_pagination = int(pagination[0].find_all("span", {"class": "total"})[0].text)

        for page in range(1, total_pagination + 1):
            page_n = f"{self.shows_url}&page=%d" % page
            soup = BeautifulSoup(self.get_html_bytes(url=page_n), "html5lib")
            show_tables = soup.find_all("div", {"class": "scores-table scores-listing"})
            for table in show_tables:
                table_rows = table.find_all("tr")
                for row in table_rows[1:-1]:
                    row_values = row.find_all("td")
                    try:
                        shows.append(row_values[0].text)
                    except:
                        pass
        shows = [show for show in shows if show != '']
        self.shows = shows

        return self

    def format_show_titles(self):
        formatted_shows = []
        for show in self.shows:
            formatted_shows.append(f"{self.season}-" + re.sub(r" +", " ", re.sub(r"[^A-Za-z ]", "", show)).replace(" ", "-").lower())
        self.formatted_shows = formatted_shows
        return self
    
    def save_files(self):
        for show in self.formatted_shows:
            show_recap_url = f"{self.full_recap_scores_url}/%s" % show
            try:
                recap_html = self.get_html_bytes(show_recap_url)
                with open(f"RECAP_HTML/{show}-recap.html", "w") as full_recap_html_file:
                    full_recap_html_file.write(str(recap_html))
            except Exception as recap_pull_exception:
                print(f"Could not save full recap html for {show}!\n\t{recap_pull_exception}")
    
    def testing_full_recap_data_pulls(self):
        for show in self.formatted_shows:
            with open(f"RECAP_HTML/{show}-recap.html", "rb") as full_recap_html_file:
                full_recap_html = full_recap_html_file.read()
                print("FILE OPENED SUCCESSFULY! ATTT")
                soup = BeautifulSoup(full_recap_html, "html5lib")
                print(f"EAT THAT DAMN SOUP! {show}")


    def get_full_recap(self):
        """
        {
            corp1: { recap vals },
            corp2: { recap vals },
            . . . . . . . . . . .
        }
        """
        RECAP = {}

        for show in self.formatted_shows[0:1]:
            show_recap_url = f"{self.full_recap_scores_url}/%s" % show
            try:
                pass
            except:
                print(f"Could not grab full recap for {show}!")

