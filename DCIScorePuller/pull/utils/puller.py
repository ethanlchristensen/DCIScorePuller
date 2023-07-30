import requests
import sys
import re
import urllib
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

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

    def get_html_bytes_from_file(self, formatted_show):
        with open(f"./RECAP_HTML/{formatted_show}.html", "rb") as html_file:
            html_byte_content = html_file.read()
            return html_byte_content

    def get_competitions(self):
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

    def format_competition_titles(self):
        formatted_shows = []
        for show in self.shows:
            formatted_shows.append(f"{self.season}-" + re.sub(r" +", " ", re.sub(r"[^A-Za-z ]", "", show)).replace(" ", "-").lower())
        self.formatted_shows = formatted_shows
        self.formatted_shows_mapping = {formatted:orig for formatted, orig in zip(self.formatted_shows, self.shows)}
        return self
    
    def save_files(self):
        for show in self.formatted_shows:
            show_recap_url = f"{self.full_recap_scores_url}/%s" % show
            try:
                if not os.path.exists(f"RECAP_HTML/{show}-recap.html"):
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

    def get_competition_recap(self, show):
        FULL_RECAP = {}

        show_recap_url = f"{self.full_recap_scores_url}/%s" % show
        try:
            
            FULL_RECAP[show] = {}
            FULL_RECAP[show]["shows"] = {}

            show_score_recap_content = self.get_html_bytes(url=show_recap_url)
            soup = BeautifulSoup(show_score_recap_content, "html5lib")

            tables = soup.find_all("div", {"class": "wrap-scores-details-table"})
            table_header_date = soup.find_all("div", {"class": "table-header"})[0].find_all("div", {"class": "details"})[0].find_all("span")[0].text

            FULL_RECAP[show]["date"] = datetime.strptime(table_header_date, "%B %d, %Y")
            FULL_RECAP[show]["Correct Competition Name"] = self.formatted_shows_mapping[show]

            for table_idx, table in enumerate(tables):
                
                header = table.find_all("h4")

                if header[0].text == "All Age Class": break

                sticky_corps = table.find_all("div", {"class": "sticky-corps"})[0]
                corps = sticky_corps.find_all("li")
                for corp in corps:
                    FULL_RECAP[show]["shows"][corp.text] = {}
                
                corps_names = [corp.text for corp in corps]
                scores = table.find_all("div", {"class": "data-table"})
                try:
                    for i, score in enumerate(scores[1:]):
                        
                        current_corp = corps_names[i]

                        score_groups = score.find_all("div", {"class":"cell"})
                        general_effect = score_groups[0]
                        visual = score_groups[1]
                        music = score_groups[2]

                        # GE
                        ge_column = general_effect.find_all("div", {"class":"column"})
                        if len(ge_column) == 3:
                            ge_1 = ge_column[0]
                            ge_2 = ge_column[1]
                            ge_total = ge_column[2]

                            ge_1_scores = ge_1.find_all("span")
                            ge_1_rep = ge_1_scores[0].text
                            ge_1_perf = ge_1_scores[2].text
                            ge_1_total = ge_1_scores[4].text

                            ge_2_scores = ge_2.find_all("span")
                            ge_2_rep = ge_2_scores[0].text
                            ge_2_perf = ge_2_scores[2].text
                            ge_2_total = ge_2_scores[4].text

                            ge_total_scores = ge_total.find_all("span")
                            ge_total_score = ge_total_scores[0].text

                            FULL_RECAP[show]["shows"][current_corp]["General Effect"] = {
                                "General Effect 1": {
                                    "Rep": float(ge_1_rep),
                                    "Perf": float(ge_1_perf),
                                    "Total": float(ge_1_total)
                                },
                                "General Effect 2": {
                                    "Rep": float(ge_2_rep),
                                    "Perf": float(ge_2_perf),
                                    "Total": float(ge_2_total)
                                },
                                "Total": float(ge_total_score)
                            }
                        else:
                            ge_1_1 = ge_column[0]
                            ge_1_2 = ge_column[1]
                            ge_2_1 = ge_column[2]
                            ge_2_2 = ge_column[3]
                            ge_total = ge_column[4]

                            ge_1_1_scores = ge_1_1.find_all("span")
                            ge_1_1_rep = ge_1_1_scores[0].text
                            ge_1_1_perf = ge_1_1_scores[2].text
                            ge_1_1_total = ge_1_1_scores[4].text

                            ge_1_2_scores = ge_1_2.find_all("span")
                            ge_1_2_rep = ge_1_2_scores[0].text
                            ge_1_2_perf = ge_1_2_scores[2].text
                            ge_1_2_total = ge_1_2_scores[4].text

                            ge_2_1_scores = ge_2_1.find_all("span")
                            ge_2_1_rep = ge_2_1_scores[0].text
                            ge_2_1_perf = ge_2_1_scores[2].text
                            ge_2_1_total = ge_2_1_scores[4].text

                            ge_2_2_scores = ge_2_2.find_all("span")
                            ge_2_2_rep = ge_2_2_scores[0].text
                            ge_2_2_perf = ge_2_2_scores[2].text
                            ge_2_2_total = ge_2_2_scores[4].text

                            ge_total_scores = ge_total.find_all("span")
                            ge_total_score = ge_total_scores[0].text

                            FULL_RECAP[show]["shows"][current_corp]["General Effect"] = {
                                "General Effect 1 - 1": {
                                    "Rep": float(ge_1_1_rep),
                                    "Perf": float(ge_1_1_perf),
                                    "Total": float(ge_1_1_total)
                                },
                                "General Effect 1 - 2": {
                                    "Rep": float(ge_1_2_rep),
                                    "Perf": float(ge_1_2_perf),
                                    "Total": float(ge_1_2_total)
                                },
                                "General Effect 2 - 1": {
                                    "Rep": float(ge_2_1_rep),
                                    "Perf": float(ge_2_1_perf),
                                    "Total": float(ge_2_1_total)
                                },
                                "General Effect 2 - 2": {
                                    "Rep": float(ge_2_2_rep),
                                    "Perf": float(ge_2_2_perf),
                                    "Total": float(ge_2_2_total)
                                },
                                "Total": float(ge_total_score)
                            }


                        # VISUAL
                        vi_column = visual.find_all("div", {"class": "column"})
                        vp = vi_column[0]
                        va = vi_column[1]
                        cg = vi_column[2]
                        vi_total = vi_column[3]

                        vp_scores = vp.find_all("span")
                        vp_cont = vp_scores[0].text
                        vp_achv = vp_scores[2].text
                        vp_total = vp_scores[4].text

                        va_scores = va.find_all("span")
                        va_cont = va_scores[0].text
                        va_achv = va_scores[2].text
                        va_total = va_scores[4].text

                        cg_scores = cg.find_all("span")
                        cg_cont = cg_scores[0].text
                        cg_achv = cg_scores[2].text
                        cg_total = cg_scores[4].text

                        vi_total_scores = vi_total.find_all("span")
                        vi_total_score = vi_total_scores[0].text

                        FULL_RECAP[show]["shows"][current_corp]["Visual"] = {
                            "Visual Proficiency": {
                                "Cont": float(vp_cont),
                                "Achv": float(vp_achv),
                                "Total": float(vp_total)
                            },
                            "Visual Analysis": {
                                "Cont": float(va_cont),
                                "Achv": float(va_achv),
                                "Total": float(va_total)
                            },
                            "Color Guard": {
                                "Cont": float(cg_cont),
                                "Achv": float(cg_achv),
                                "Total": float(cg_total)
                            },
                            "Total": float(vi_total_score)
                        }

                        # MUSIC
                        music_column = music.find_all("div", {"class": "column"})

                        if len(music_column) == 4:
                            mu_brass = music_column[0]
                            mu_analysis = music_column[1]
                            mu_percussion = music_column[2]
                            mu_total = music_column[3]

                            mu_brass_scores = mu_brass.find_all("span")
                            mu_b_cont = mu_brass_scores[0].text
                            mu_b_achv = mu_brass_scores[2].text
                            mu_b_total = mu_brass_scores[4].text

                            mu_analysis_scores = mu_analysis.find_all("span")
                            mu_a_cont = mu_analysis_scores[0].text
                            mu_a_achv = mu_analysis_scores[2].text
                            mu_a_total = mu_analysis_scores[4].text

                            mu_perc_scores = mu_percussion.find_all("span")
                            mu_p_cont = mu_perc_scores[0].text
                            mu_p_achv = mu_perc_scores[2].text
                            mu_p_total = mu_perc_scores[4].text

                            mu_total_scores = mu_total.find_all("span")
                            mu_total_score = mu_total_scores[0].text

                            FULL_RECAP[show]["shows"][current_corp]["Music"] = {
                                "Music Brass": {
                                    "Cont": float(mu_b_cont),
                                    "Achv": float(mu_b_achv),
                                    "Total": float(mu_b_total)
                                },
                                "Music Analysis - 1": {
                                    "Cont": float(mu_a_cont),
                                    "Achv": float(mu_a_achv),
                                    "Total": float(mu_a_total)
                                },
                                "Music Percussion": {
                                    "Cont": float(mu_p_cont),
                                    "Achv": float(mu_p_achv),
                                    "Total": float(mu_p_total)
                                },
                                "Total": float(mu_total_score),
                            }
                        # otherwise we have two Music Analysis Columns
                        else:
                            mu_brass = music_column[0]
                            mu_analysis_1 = music_column[1]
                            mu_analysis_2 = music_column[2]
                            mu_percussion = music_column[3]
                            mu_total = music_column[4]

                            mu_brass_scores = mu_brass.find_all("span")
                            mu_b_cont = mu_brass_scores[0].text
                            mu_b_achv = mu_brass_scores[2].text
                            mu_b_total = mu_brass_scores[4].text

                            mu_analysis_1_scores = mu_analysis_1.find_all("span")
                            mu_a_1_cont = mu_analysis_1_scores[0].text
                            mu_a_1_achv = mu_analysis_1_scores[2].text
                            mu_a_1_total = mu_analysis_1_scores[4].text

                            mu_analysis_2_scores = mu_analysis_2.find_all("span")
                            mu_a_2_cont = mu_analysis_2_scores[0].text
                            mu_a_2_achv = mu_analysis_2_scores[2].text
                            mu_a_2_total = mu_analysis_2_scores[4].text

                            mu_perc_scores = mu_percussion.find_all("span")
                            mu_p_cont = mu_perc_scores[0].text
                            mu_p_achv = mu_perc_scores[2].text
                            mu_p_total = mu_perc_scores[4].text

                            mu_total_scores = mu_total.find_all("span")
                            mu_total_score = mu_total_scores[0].text

                            FULL_RECAP[show]["shows"][current_corp]["Music"] = {
                                "Music Brass": {
                                    "Cont": float(mu_b_cont),
                                    "Achv": float(mu_b_achv),
                                    "Total": float(mu_b_total)
                                },
                                "Music Analysis - 1": {
                                    "Cont": float(mu_a_1_cont),
                                    "Achv": float(mu_a_1_achv),
                                    "Total": float(mu_a_1_total)
                                },
                                "Music Analysis - 2": {
                                    "Cont": float(mu_a_2_cont),
                                    "Achv": float(mu_a_2_achv),
                                    "Total": float(mu_a_2_total)
                                },
                                "Music Percussion": {
                                    "Cont": float(mu_p_cont),
                                    "Achv": float(mu_p_achv),
                                    "Total": float(mu_p_total)
                                },
                                "Total": float(mu_total_score),
                            }
                except Exception as e2:
                    print(f"ERROR: {e2}")
        except Exception as exception:
            print(f"Could not grab full recap for {show}!\n -> ERROR: {exception}")
        return FULL_RECAP[show]
