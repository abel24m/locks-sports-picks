from selenium.webdriver.common.print_page_options import PrintOptions

from api.web_scrape.data.covers_baseball_match_data import CoversBaseballMatchData
from api.web_scrape.data.covers_baseball_team_data import CoversBaseballTeamData


class Analyst:

    def __init__(self):
        pass

    def analyze_mlb(self, mlb_matches : [CoversBaseballMatchData]):
        match : CoversBaseballMatchData
        for match in mlb_matches:
            # analyze the starting pitchers
            home_pitcher_model = self._analyze_pitcher(match.home_team_data)
            away_pitcher_model = self._analyze_pitcher(match.away_team_data)

            # analyze the hitting
            home_hitting_model = self._analyze_hitting(match.home_team_data)
            away_hitting_model = self._analyze_hitting(match.away_team_data)

            # analyze bullpen
            home_bullpen_model = self._analyze_bullpen(match.home_team_data)
            away_bullpen_model = self._analyze_bullpen(match.away_team_data)

            # hth and overall team record
            home_hth_model = self._analyze_hth_model(match.home_team_data)
            away_hth_model = self._analyze_hth_model(match.away_team_data)

            home_analysis = {**home_pitcher_model, **home_hitting_model,
                             **home_bullpen_model, **home_hth_model}
            away_analysis = {**away_pitcher_model, **away_hitting_model,
                             **away_bullpen_model, **away_hth_model}
            results = {
                "home" : home_analysis,
                "away" : away_analysis
            }
            match.set_analysis(results)


    @staticmethod
    def _analyze_hth_model (team_data: CoversBaseballTeamData):
        results = {
            "hth_win_loss" : team_data.hth_win_loss,
            "hth_over_under" : team_data.hth_over_under
        }
        return results

    @staticmethod
    def _analyze_bullpen(team_data : CoversBaseballTeamData):
        results = {
            "bullpen_era" : float(team_data.available_bullpen_era),
            "bullpen_whip" : float(team_data.available_bullpen_whip)
        }
        return results

    @staticmethod
    def _analyze_hitting(team_data : CoversBaseballTeamData):
        hitting_code = 0

        try:
            hitting_code += float(team_data.runs_avg) * 1.75
            hitting_batting_average = float(team_data.batting_avg) * 2
            hitting_code += float(team_data.hits_avg) * 1.25
            hitting_code += float(team_data.hr_avg) * 1.75
            hitting_code += float(team_data.walks_avg) * 1.80
            hitting_results = {
                "Hitting Batting Avg" : hitting_batting_average,
                "Hitting Performance" : hitting_code
            }
            return hitting_results
        except ValueError as err:
            print("Value error for hitting")
            results = {}
            return results

    @staticmethod
    def _analyze_pitcher(team_data : CoversBaseballTeamData):
        pitcher_code_one = 0
        pitcher_code_one += float(team_data.pitcher_lf_era) * 2
        pitcher_code_one += float(team_data.pitcher_lf_run) * 1.5
        pitcher_code_one += float(team_data.pitcher_lf_hits) * 1.5
        pitcher_code_one += float(team_data.pitcher_lf_hr) * 2
        pitcher_code_one += float(team_data.pitcher_lf_bb) * 1.25

        pitcher_code_two = float(team_data.pitcher_lf_so) * 2

        pitcher_code_three = float(team_data.pitcher_lf_pit)
        pitcher_code_four = float(team_data.pitcher_lf_pip)
        pitcher_results = {
            "Starting Pitcher Rating (low)" : pitcher_code_one,
            "Starting Pitcher Strikeouts" : pitcher_code_two,
            "Starting Pitcher Total Pitches" : pitcher_code_three,
            "Starting Pitcher Pitches and Inning" : pitcher_code_four
        }

        return pitcher_results
