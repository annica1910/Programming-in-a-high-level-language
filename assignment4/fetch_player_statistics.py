import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str):
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams("https://en.wikipedia.org/wiki/2022_NBA_playoffs")
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {}
    for team in teams:
        all_players[team['name']] = get_players(team['url'])

    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        players_new = []
        for player in players:
            stats = get_player_stats(player['url'], team)
            if stats:
                res = player | stats        #merge 2 dicts
            players_new.append(res)
        all_players[team] = players_new
    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    # Select top 3 for each team by points:
    best = {}
    top_stat = ...
    for team, players in all_players.items():
        # Sort and extract top 3 based onpoints
        top_3 = sorted(players, key=lambda d: d['points'], reverse=True)[0:3]
        best[team] = top_3      

    print(len(best))      

    stats_to_plot = ["points", "assists", "rebounds"]
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points"):
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics"
    """Plot NBA player statistics"""
    count_so_far = 0
    all_names = []

    # iterate through each team and the
    for team, players in best.items():
        # collect the points and name of each player on the team
        # you'll want to repeat with other stats as well
        stat_bar = []
        names = []
        for player in players:
            names.append(player["name"])
            stat_bar.append(player[stat])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = range(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players points,
        # with the team name as the label
        bars = plt.bar(x, stat_bar, label=team)
        # add the value as text on the bars
        plt.bar_label(bars)

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(range(len(all_names)), all_names, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=0)
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title(stat + " per game")
    # save the figure to a file
    nba_stats_dir = "NBA_player_statistics"
    if not os.path.exists(nba_stats_dir):
        os.makedirs(nba_stats_dir)
    filename = stat + ".png"
    print(f"Creating {filename}")
    plt.savefig(os.path.join(nba_stats_dir, filename))


def get_teams(url: str):
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str):
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    roster = soup.find(id="Roster")
    table = roster.find_next("table", {"class": "sortable"})

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    rows = rows[1:]
    for row in rows:

        # Get the columns
        cols = row.find_all("td")[2]    #3rd col is names
        # find name links (a tags)
        # and add to players a dict with
        # {'name':, 'url':}
        a_tag = cols.find("a")
        name = a_tag.get_text().strip()
        link = a_tag["href"]
        TW = cols.find("b")
        if TW:
            name += TW.get_text()
        player = {
            'name': name,
            'url' : base_url + link 
        }
        players.append(player)

    # return list of players
    return players



def get_player_stats(player_url: str, team: str):
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")
    year = "2021–22 NBA season"

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")

    career_stats = soup.find(id="Career_statistics")
    if not career_stats:
        career_stats = soup.find(id="NBA_career_statistics")
        reg_seas = career_stats.find_next(id="Regular_season")
        table = reg_seas.find_next("table", {"class": "wikitable sortable"})
    else:
        nba = career_stats.find_next(id="NBA")
        if nba:
            reg_seas = nba.find_next(id="Regular_season")
        else:
            reg_seas = career_stats.find_next(id="Regular_season")
        if reg_seas:
            table = reg_seas.find_next("table", {"class": "wikitable sortable"})
        else:
            table = nba.find_next("table", {"class": "wikitable sortable"})


    wanted = {'PPG' : 'points', 'RPG': 'rebounds', 'APG' : 'assists', 'SPG' : 'steals', 'BPG' : 'blocks'}
    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]

    stats = {}

    rows = table.find_all("tr", attrs={"class":None})
    rows = rows[1:]
    # Loop over rows and extract the stats

    for row in rows:
        cols = row.find_all("td")

        # Check correct team and year (some players change team within season)
        row_yr = cols[0].find("a")
        if row_yr: 
            row_yr = row_yr['title'] 
        if row_yr == year:                             
            if cols[1].get_text().strip() == team:  
                # Iterate cells in row
                for i in range(len(cols)):
                    label = labels[i]
                    if label in wanted:
                        key = wanted[label]
                        text = cols[i].text.strip()
                        text = text.replace('*','')
                        stats[wanted[label]] = float(text)
    
        # load stats from columns
        # keys should be 'points', 'assists', etc.

    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)

    # team_url = "https://en.wikipedia.org/wiki/2021%E2%80%9322_Philadelphia_76ers_season"
    # teamplayers = get_players(team_url)
    # print(teamplayers)
    
    player_url = "https://en.wikipedia.org/wiki/D%C4%81vis_Bert%C4%81ns"
    #player_stats = get_player_stats(player_url, )
    #print(player_stats)
    