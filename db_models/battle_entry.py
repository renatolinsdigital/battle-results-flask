from config.database import db
from datetime import datetime, timezone


class BattleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_tag = db.Column(db.String(100), nullable=False)
    player_1_name = db.Column(db.String(100), nullable=False)
    player_2_name = db.Column(db.String(100), nullable=False)
    winner_name = db.Column(db.String(100), nullable=False)
    finished_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    @classmethod
    def from_json(cls, json_dict: dict):
        return cls(
            game_tag=json_dict['gameTag'],
            player_1_name=json_dict['player1Name'],
            player_2_name=json_dict['player2Name'],
            winner_name=json_dict['winnerName'],
            finished_date=datetime.strptime(
                json_dict['finishedDate'], '%Y-%m-%d %H:%M:%S')
        )

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'gameTag': self.game_tag,
            'player1Name': self.player_1_name,
            'player2Name': self.player_2_name,
            'winnerName': self.winner_name,
            'finishedDate': self.finished_date.strftime('%Y-%m-%d %H:%M:%S')
        }
