from time import sleep

from api.web_scrape.data.covers_baseball_team_data import CoversBaseballTeamData
from api.web_scrape.support import globals


class CoversBaseballMatchData:

    home_team: str
    away_team: str
    home_team_short: str
    away_team_short: str
    match_time: str
    home_team_data: CoversBaseballTeamData
    away_team_data: CoversBaseballTeamData
    analysis = {}
    analyzed = False
    json_dump = {}


    def __init__(self):
        self.home_team_data = CoversBaseballTeamData()
        self.away_team_data = CoversBaseballTeamData()

    def set_analysis (self, analysis : dict):
        self.analysis = analysis
        self.analyzed = True

    def set_hth_data(self, data : dict):
        for item in data:
            match item:
                case globals.HTH_OVER_UNDER:
                    self.home_team_data.hth_over_under = data[item]
                    self.away_team_data.hth_over_under = data[item]
                case globals.HTH_WIN_LOSS:
                    self.home_team_data.hth_win_loss = data[item]
                    self.away_team_data.hth_win_loss = data[item]

    def _set_home_team_lt(self, data : dict):
        for rec in data:
            match rec:
                case globals.TEAM_WIN_LOSS:
                    self.home_team_data.last_ten_win_loss = data[rec]
                case globals.TEAM_OVER_UNDER:
                    self.home_team_data.last_ten_over_under = data[rec]

    def _set_away_team_lt(self, data : dict):
        for rec in data:
            match rec:
                case globals.TEAM_WIN_LOSS:
                    self.away_team_data.last_ten_win_loss = data[rec]
                case globals.TEAM_OVER_UNDER:
                    self.away_team_data.last_ten_over_under = data[rec]


    def set_team_betting_records(self, data : dict):
        for team in data:
            match team:
                case "home":
                    self._set_home_team_lt(data[team])
                case "away":
                    self._set_away_team_lt(data[team])

    def set_hitting_data(self, home_data: dict, away_data:dict):
        for stat in home_data:
            match stat:
                case globals.HITTING_RUNS_AVG :
                    self.home_team_data.runs_avg = home_data[stat]
                case globals.HITTING_HITS_AVG :
                    self.home_team_data.hits_avg = home_data[stat]
                case globals.HITTING_HR_AVG :
                    self.home_team_data.hr_avg = home_data[stat]
                case globals.HITTING_BATTING_AVG :
                    self.home_team_data.batting_avg = home_data[stat]
                case globals.HITTING_BB_AVG :
                    self.home_team_data.walks_avg = home_data[stat]
        for stat in away_data:
            match stat:
                case globals.HITTING_RUNS_AVG :
                    self.away_team_data.runs_avg = away_data[stat]
                case globals.HITTING_HITS_AVG :
                    self.away_team_data.hits_avg = away_data[stat]
                case globals.HITTING_HR_AVG :
                    self.away_team_data.hr_avg = away_data[stat]
                case globals.HITTING_BATTING_AVG :
                    self.away_team_data.batting_avg = away_data[stat]
                case globals.HITTING_BB_AVG :
                    self.away_team_data.walks_avg = away_data[stat]

    def set_home_pitcher_data(self, data : dict):
        for rec in data :
            match rec:
                case globals.PITCHER_WIN_LOSS:
                    self.home_team_data.pitcher_lf_win_loss = data[rec]
                case globals.PITCHER_ERA:
                    self.home_team_data.pitcher_lf_era = data[rec]
                case globals.PITCHER_RUNS:
                    self.home_team_data.pitcher_lf_run = data[rec]
                case globals.PITCHER_IP:
                    self.home_team_data.pitcher_lf_ip = data[rec]
                case globals.PITCHER_HITS:
                    self.home_team_data.pitcher_lf_hits = data[rec]
                case globals.PITCHER_ER:
                    self.home_team_data.pitcher_lf_er = data[rec]
                case globals.PITCHER_SO:
                    self.home_team_data.pitcher_lf_so = data[rec]
                case globals.PITCHER_BB:
                    self.home_team_data.pitcher_lf_bb = data[rec]
                case globals.PITCHER_HR:
                    self.home_team_data.pitcher_lf_hr = data[rec]
                case globals.PITCHER_PIT:
                    self.home_team_data.pitcher_lf_pit = data[rec]
                case globals.PITCHER_PIP:
                    self.home_team_data.pitcher_lf_pip = data[rec]

    def set_away_pitcher_data(self, data : dict):
            for rec in data:
                match rec:
                    case globals.PITCHER_WIN_LOSS:
                        self.away_team_data.pitcher_lf_win_loss = data[rec]
                    case globals.PITCHER_ERA:
                        self.away_team_data.pitcher_lf_era = data[rec]
                    case globals.PITCHER_RUNS:
                        self.away_team_data.pitcher_lf_run = data[rec]
                    case globals.PITCHER_IP:
                        self.away_team_data.pitcher_lf_ip = data[rec]
                    case globals.PITCHER_HITS:
                        self.away_team_data.pitcher_lf_hits = data[rec]
                    case globals.PITCHER_ER:
                        self.away_team_data.pitcher_lf_er = data[rec]
                    case globals.PITCHER_SO:
                        self.away_team_data.pitcher_lf_so = data[rec]
                    case globals.PITCHER_BB:
                        self.away_team_data.pitcher_lf_bb = data[rec]
                    case globals.PITCHER_HR:
                        self.away_team_data.pitcher_lf_hr = data[rec]
                    case globals.PITCHER_PIT:
                        self.away_team_data.pitcher_lf_pit = data[rec]
                    case globals.PITCHER_PIP:
                        self.away_team_data.pitcher_lf_pip = data[rec]

    def set_bullpen_data(self, home_bullpen_data : dict , away_bullpen_data : dict):
        for stat in home_bullpen_data:
            match stat:
                case globals.BULLPEN_ERA:
                    self.home_team_data.available_bullpen_era = home_bullpen_data[stat]
                case globals.BULLPEN_WHIP:
                    self.home_team_data.available_bullpen_whip = home_bullpen_data[stat]
        for stat in away_bullpen_data:
            match stat:
                case globals.BULLPEN_ERA:
                    self.away_team_data.available_bullpen_era = away_bullpen_data[stat]
                case globals.BULLPEN_WHIP:
                    self.away_team_data.available_bullpen_whip = away_bullpen_data[stat]

    def get_json_dump(self):
        json_dump = {
            "Home Team" : self.home_team,
            "Home Team Short" : self.home_team_short,
            "Away Team" : self.away_team,
            "Away Team Short" : self.away_team_short,
            "Match Time" : self.match_time,
            "Home Team Model" : self.analysis["home"],
            "Away Team Model" : self.analysis["away"]
        }
        return json_dump