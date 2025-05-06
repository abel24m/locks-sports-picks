
class CoversBaseballTeamData:

    pitcher_lf_win_loss: str # last 5 games win/loss ratio
    pitcher_lf_era: str # last 5 games pitcher ERA
    pitcher_lf_run: str # last 5 games avg runs allowed
    pitcher_lf_ip: str # last 5 games avg innings pitched
    pitcher_lf_hits: str # last 5 games avg hits given
    pitcher_lf_er: str # last 5 games avg earned runs allowed
    pitcher_lf_so: str # last 5 games avg strikeouts
    pitcher_lf_bb: str # last 5 games avg walks
    pitcher_lf_hr: str # last 5 games avg HR
    pitcher_lf_pit: str # last 5 games pitches thrown
    pitcher_lf_pip: str # last 5 games pitches per inning
    hth_win_loss: str # head-to-head win loss record
    hth_over_under: str # head-to-head over under record
    last_ten_win_loss: str # last 10 games win loss record
    last_ten_over_under: str # last 10 games over under record
    available_bullpen_era: str # available bullpen era.
    available_bullpen_whip: str # available bullpen whip
    runs_avg: str # average runs total per game
    batting_avg: str # batting average
    hits_avg: str # hits average per game
    hr_avg: str # home runs average per game
    walks_avg: str # average walks per game

    def __init__(self):
        self.pitcher_lf_win_loss = "0"  # last 5 games win/loss ratio
        self.pitcher_lf_era = "0"  # last 5 games pitcher ERA
        self.pitcher_lf_run = "0"  # last 5 games avg runs allowed
        self.pitcher_lf_ip = "0"  # last 5 games avg innings pitched
        self.pitcher_lf_hits = "0"  # last 5 games avg hits given
        self.pitcher_lf_er = "0"  # last 5 games avg earned runs allowed
        self.pitcher_lf_so = "0"  # last 5 games avg strikeouts
        self.pitcher_lf_bb = "0"  # last 5 games avg walks
        self.pitcher_lf_hr = "0"  # last 5 games avg HR
        self.pitcher_lf_pit = "0"  # last 5 games pitches thrown
        self.pitcher_lf_pip = "0"  # last 5 games pitches per inning
        self.hth_win_loss = "0"  # head-to-head win loss record
        self.hth_over_under = "0"  # head-to-head over under record
        self.last_ten_win_loss = "0"  # last 10 games win loss record
        self.last_ten_over_under = "0"  # last 10 games over under record
        self.available_bullpen_era = "0"  # available bullpen era.
        self.available_bullpen_whip = "0"  # available bullpen whip
        self.runs_avg = "0"  # average runs total per game
        self.batting_avg = "0"  # batting average
        self.hits_avg = "0"  # hits average per game
        self.hr_avg = "0"  # home runs average per game
        self.walks_avg = "0"  # average walks per game
        pass

class CoversHeadToHeadData:
    win_loss: str #win loss ratio
    over_under: str # over under record

