from flask import request, jsonify, abort
from datetime import datetime
from config.database import db
from db_models.battle_entry import BattleEntry
from config.status_codes import CREATED, NOT_FOUND, OK, BAD_REQUEST


def get_all_entries():
    entries = BattleEntry.query.all()

    entries_list = []
    for entry in entries:
        entry_dict = entry.to_json()
        entries_list.append(entry_dict)

    return jsonify({'entries': entries_list})


def create_entry():
    req_json = request.get_json()

    has_required_fields = (
        'gameTag' in req_json
        and 'player1Name' in req_json
        and 'player2Name' in req_json
        and 'winnerName' in req_json
    )
    if not has_required_fields or \
            req_json['player1Name'] == req_json['player2Name'] or \
            req_json['winnerName'] not in [req_json['player1Name'], req_json['player2Name']]:
        return abort(BAD_REQUEST, description="Inform different player names and ensure that the winner's name matches one of the player's names")

    battle_entry = BattleEntry.from_json(req_json)

    db.session.add(battle_entry)
    db.session.commit()

    return jsonify({'message': f'Battle entry created with id {battle_entry.id}'}), CREATED


def get_entry(entry_id):
    entry = BattleEntry.query.get(entry_id)
    if entry is None:
        return abort(NOT_FOUND, description='Entry not found')

    entry_dict = entry.to_json()
    return jsonify({'entry': entry_dict})


def partial_update_entry(entry_id):
    req_json = request.get_json()
    entry_to_update = BattleEntry.query.get(entry_id)

    if entry_to_update is None:
        return abort(NOT_FOUND, description='Entry not found')

    if 'gameTag' in req_json:
        return abort(BAD_REQUEST, description='gameTag cannot be updated')

    if 'player1Name' in req_json:
        entry_to_update.player_1_name = req_json['player1Name']
    if 'player2Name' in req_json:
        entry_to_update.player_2_name = req_json['player2Name']
    if 'winnerName' in req_json:
        winner_name = req_json['winnerName']
        if winner_name == entry_to_update.player_1_name or winner_name == entry_to_update.player_2_name:
            entry_to_update.winner_name = winner_name
        else:
            return abort(BAD_REQUEST, description='Winner name must be equal to player 1 or player 2 name')

    if 'finishedDate' in req_json:
        entry_to_update.finished_date = datetime.strptime(
            req_json['finishedDate'], '%Y-%m-%d %H:%M:%S')

    db.session.commit()

    return jsonify({'message': f'Battle entry with id {entry_id} has been updated'}), OK


def delete_entry(entry_id):
    entry_to_delete = BattleEntry.query.get(entry_id)
    if entry_to_delete is None:
        return abort(NOT_FOUND)

    db.session.delete(entry_to_delete)
    db.session.commit()

    return jsonify({'message': f'Battle entry with id {entry_id} has been deleted'}), OK
