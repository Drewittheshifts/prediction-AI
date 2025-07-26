import random
import json
import datetime
import schedule
import time
from pathlib import Path
import requests

from balldontlie import BalldontlieAPI
api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
{
  "meta": {
    "next_cursor": 90,
    "per_page": 25
  }
}

from balldontlie import BalldontlieAPI
api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
teams = api.nba.teams.list()
{
  "data": [
    {
      "id":1,
      "conference":"East",
      "division":"Southeast",
      "city":"Atlanta",
      "name":"Hawks",
      "full_name":"Atlanta Hawks",
      "abbreviation":"ATL"
    },
    ...
  ]
}

from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
teams = api.nba.teams.get(1)
{
  "data": [
    {
      "id": 1,
      "conference": "East",
      "division": "Southeast",
      "city": "Atlanta",
      "name": "Hawks",
      "full_name": "Atlanta Hawks",
      "abbreviation": "ATL"
    }
  ]
}

from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
players = api.nba.players.list(per_page=25)
{
  "data": [
    {
        "id": 19,
        "first_name": "Stephen",
        "last_name": "Curry",
        "position": "G",
        "height": "6-2",
        "weight": "185",
        "jersey_number": "30",
        "college": "Davidson",
        "country": "USA",
        "draft_year": 2009,
        "draft_round": 1,
        "draft_number": 7,
        "team": {
            "id": 10,
            "conference": "West",
            "division": "Pacific",
            "city": "Golden State",
            "name": "Warriors",
            "full_name": "Golden State Warriors",
            "abbreviation": "GSW"
        }
    },
    ...
  ],
  "meta": {
    "next_cursor": 25,
    "per_page": 25
  }
}

from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
player = api.nba.players.get(19)
{
  "data": {
    "id": 19,
    "first_name": "Stephen",
    "last_name": "Curry",
    "position": "G",
    "height": "6-2",
    "weight": "185",
    "jersey_number": "30",
    "college": "Davidson",
    "country": "USA",
    "draft_year": 2009,
    "draft_round": 1,
    "draft_number": 7,
    "team": {
      "id": 10,
      "conference": "West",
      "division": "Pacific",
      "city": "Golden State",
      "name": "Warriors",
      "full_name": "Golden State Warriors",
      "abbreviation": "GSW"
    }
  }
}

from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
games = api.nba.games.list()
{
  "data": [
    {
      "id": 1,
      "date": "2018-10-16",
      "datetime": "2018-10-17 00:00:00+00",
      "season": 2018,
      "status": "Final",
      "period": 4,
      "time": " ",
      "postseason": False,
      "home_team_score": 105,
      "visitor_team_score": 87,
      "home_team": {
        "id": 2,
        "conference": "East",
        "division": "Atlantic",
        "city": "Boston",
        "name": "Celtics",
        "full_name": "Boston Celtics",
        "abbreviation": "BOS"
      },
      "visitor_team": {
        "id": 23,
        "conference": "East",
        "division": "Atlantic",
        "city": "Philadelphia",
        "name": "76ers",
        "full_name": "Philadelphia 76ers",
        "abbreviation": "PHI"
      }
    },
    ...
  ],
  "meta": {
    "next_cursor": 25,
    "per_page": 25
  }
}

from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key="19e774c4-1fae-4fd3-bd37-abc7bada0a50")
game = api.nba.games.get(1)
{
  "data": [
    {
      "id": 1,
      "date": "2018-10-16",
      "season": 2018,
      "status": "Final",
      "period": 4,
      "time": " ",
      "postseason": False,
      "home_team_score": 105,
      "visitor_team_score": 87,
      "home_team": {
        "id": 2,
        "conference": "East",
        "division": "Atlantic",
        "city": "Boston",
        "name": "Celtics",
        "full_name": "Boston Celtics",
        "abbreviation": "BOS"
      },
      "visitor_team": {
        "id": 23,
        "conference": "East",
        "division": "Atlantic",
        "city": "Philadelphia",
        "name": "76ers",
        "full_name": "Philadelphia 76ers",
        "abbreviation": "PHI"
      }
    }
  ]
}



class ParlayBot:
    def __init__(self, player_data_path='player_data.json', history_path='history.json'):
        self.player_data_path = Path(player_data_path)
        self.history_path = Path(history_path)
        if not self.player_data_path.exists():
            print("Player data not found. Fetching player data from API...")
            self.fetch_and_generate_player_data()
        self.players = self.load_player_data()
        self.history = self.load_history()

    def fetch_and_generate_player_data(self):
        print("Fetching all NBA players from Balldontlie API...")
        players = []
        page = 1
        while True:
            response = requests.get(f'https://www.balldontlie.io/api/v1/players?page={page}&per_page=100')
            data = response.json()
            players.extend(data['data'])
            if data['meta']['next_page'] is None:
                break
            page += 1
            time.sleep(0.5)  # avoid rate limits

        print(f"Fetched {len(players)} players.")

        player_props = []
        for p in players:
            player_props.append({
                "name": f"{p['first_name']} {p['last_name']}",
                "team": p['team']['abbreviation'],
                "prop": "PTS",
                "line": 20 + (p['id'] % 10),  # dummy line
                "avg": 20 + (p['id'] % 12),   # dummy avg
                "trend": [
                    {"game": "2025-07-20", "value": 20 + (p['id'] % 15)},
                    {"game": "2025-07-18", "value": 18 + (p['id'] % 15)}
                ]
            })

        with self.player_data_path.open('w', encoding='utf-8') as f:
            json.dump(player_props, f, indent=2)
        print(f"Saved player data with props to '{self.player_data_path}'.")

    def load_player_data(self):
        if not self.player_data_path.exists():
            return []
        try:
            with self.player_data_path.open(encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def load_history(self):
        if not self.history_path.exists():
            return []
        try:
            with self.history_path.open(encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def save_history(self):
        try:
            with self.history_path.open('w', encoding='utf-8') as f:
                json.dump(self.history[:10], f, indent=2)
        except Exception:
            pass

    def evaluate(self, player):
        try:
            diff = float(player.get('avg', 0)) - float(player.get('line', 0))
            if diff > 1.0:
                return "MORE"
            elif diff < -1.0:
                return "LESS"
            return "MORE (lean)" if diff > 0 else "LESS (lean)"
        except Exception:
            return "N/A"

    def filter_players(self, search_term='', prop_filter=''):
        return [p for p in self.players if 'name' in p and search_term.lower() in p['name'].lower() and (not prop_filter or p.get('prop') == prop_filter)]

    def generate_parlay(self, search_term='', prop_filter='', legs=3):
        filtered = self.filter_players(search_term, prop_filter)
        if len(filtered) < legs:
            return []
        picks = random.sample(filtered, legs)
        now = datetime.datetime.now().isoformat()
        for pick in picks:
            pick['suggestion'] = self.evaluate(pick)
            pick['timestamp'] = now
        self.history.insert(0, picks)
        self.save_history()
        return picks

    def display_parlay(self, picks):
        print("\nGenerated Parlay:")
        for p in picks:
            print(f"• {p.get('name', 'Unknown')} - {p.get('prop', '?')} - {p.get('suggestion', '?')} (Line: {p.get('line', '?')}, Avg: {p.get('avg', '?')})")

    def display_history(self, limit=3):
        print("\nRecent Parlay History:")
        for i, entry in enumerate(self.history[:limit]):
            timestamp = entry[0].get('timestamp') if entry and isinstance(entry, list) else 'N/A'
            print(f"\nParlay #{i+1} - {timestamp}")
            for p in entry:
                print(f"  • {p.get('name', 'Unknown')} - {p.get('prop', '?')} - {p.get('suggestion', '?')} (Line: {p.get('line', '?')}, Avg: {p.get('avg', '?')})")

    def daily_auto_pick(self):
        self.players = self.load_player_data()
        picks = self.generate_parlay(legs=3)
        if picks:
            print("\n[Auto-Pick] Daily Parlay:")
            self.display_parlay(picks)

if __name__ == '__main__':
    bot = ParlayBot()

    schedule.every().day.at("08:00").do(bot.daily_auto_pick)

    try:
        search = input("Search player (or press enter): ").strip()
        prop = input("Filter by prop (or press enter): ").strip()
        legs_input = input("Number of picks (2–6): ").strip()
        legs = int(legs_input) if legs_input.isdigit() and 2 <= int(legs_input) <= 6 else 3
    except Exception:
        search, prop, legs = '', '', 3

    picks = bot.generate_parlay(search, prop, legs)
    if picks:
        bot.display_parlay(picks)
    bot.display_history()

    print("\n[Scheduler Running] Daily picks will be generated at 08:00 AM")
    while True:
        schedule.run_pending()
        time.sleep(60)
