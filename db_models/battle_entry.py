from datetime import datetime
from config.database import db


class BattleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_tag = db.Column(db.String(100), nullable=False)
    player_1_name = db.Column(db.String(100), nullable=False)
    player_2_name = db.Column(db.String(100), nullable=False)
    winner_name = db.Column(db.String(100), nullable=False)
    finished_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, game_tag, player_1_name, player_2_name, winner_name):
        self.game_tag = game_tag
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        self.winner_name = winner_name

    @classmethod
    def from_json(cls, json_dict):
        return cls(
            game_tag=json_dict['gameTag'],
            player_1_name=json_dict['player1Name'],
            player_2_name=json_dict['player2Name'],
            winner_name=json_dict['winnerName']
        )

    def to_json(self):
        return {
            'id': self.id,
            'gameTag': self.game_tag,
            'player1Name': self.player_1_name,
            'player2Name': self.player_2_name,
            'winnerName': self.winner_name,
            'finishedDate': self.finished_date.strftime('%Y-%m-%d %H:%M:%S')
        }
