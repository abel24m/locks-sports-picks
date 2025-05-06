
class BovadaData:
    date: str
    home_team: str
    away_team: str
    home_spread: str
    away_spread: str
    home_ml: str
    away_ml: str
    total: str

    def __init__(self, date: str, home_team: str, away_team: str, home_spread: str, away_spread: str, home_ml: str, away_ml: str, total: str):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_spread = home_spread
        self.away_spread = away_spread
        self.home_ml = home_ml
        self.away_ml = away_ml
        self.total = total

    def write_csv(self):
        csv_result = (self.home_team + ", " +
                      self.home_spread + ", " +
                      self.home_ml + ", " +
                      self.total + "\n" +
                      self.away_team + ", " +
                      self.away_spread + ", " +
                      self.away_ml + ", " +
                      self.total + "\n")
        return csv_result