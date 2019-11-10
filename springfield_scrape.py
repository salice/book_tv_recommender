import json, requests, time
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

base_url = "https://www.springfieldspringfield.co.uk"
res = requests.get(base_url)

if res.status_code == 200:
    start = time.time()
    #there are 281 pages total
    base = "https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php"
    for i in range(21,282):
        page_show_list = []
        url = base + "?page=" +str(i)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        episode_page = soup.html
        episodes = episode_page.find_all("a",  {"class":"script-list-item"}) 
        time.sleep(5)
        #print(episodes)
        for episode in episodes:
            episode_url = base_url +str(episode.attrs["href"])
            #print(episode_url)
            res_episode = requests.get(episode_url)
            soup_episode = BeautifulSoup(res_episode.content, "lxml")
            show_page = soup_episode.html
            shows = show_page.find_all("a", {"class": "season-episode-title"})
            time.sleep(5)

            for show in shows:
                scripts = {}
                script_url = base_url+"/" + str(show.attrs["href"])
                #print(script_url)
                res_show = requests.get(script_url)
                soup_show = BeautifulSoup(res_show.content, "lxml")
                script_page = soup_show.html

                scripts["text"] = script_page.find("div", {"class": "scrolling-script-container"}).text.strip()
                scripts["episode_name"] = script_page.find("h3").text.strip()
                scripts["show_name"] = script_page.find("h1").text.strip()
                #print(scripts)
                page_show_list.append(scripts)
                time.sleep(5)

        script_df = pd.DataFrame(page_show_list)
        script_df.to_csv("./data/springfield/springfield-scrape-page-" + str(i) + ".csv", index=False)
        elapsed = round((time.time() - start) / 60, 2)
        print(f"Page {i} is done and it took {elapsed} minutes")
