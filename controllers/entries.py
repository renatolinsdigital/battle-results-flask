import logging
from flask import request, jsonify
from datetime import datetime, timezone
from config.database import db
from db_models.battle_entry import BattleEntry
from config.status_codes import CREATED, NOT_FOUND, OK, BAD_REQUEST, INTERNAL_SERVER_ERROR

logger = logging.getLogger(__name__)

_MAX_FIELD_LENGTH = 100
_REQUIRED_CREATE_FIELDS = ('gameTag', 'player1Name',
                           'player2Name', 'winnerName')


def _validate_string_field(value: str, field_name: str):
    """Return an error message if the field value is invalid, else None."""
    if not isinstance(value, str) or not value.strip():
        return f"'{field_name}' must be a non-empty string."
    if len(value) > _MAX_FIELD_LENGTH:
        return f"'{field_name}' must not exceed {_MAX_FIELD_LENGTH} characters."
    return None


def get_all_entries():
    try:
        entries = BattleEntry.query.order_by(BattleEntry.id.desc()).all()
        return jsonify({'entries': [e.to_json() for e in entries]})
    except Exception:
        logger.exception("Failed to retrieve entries")
        return jsonify({'error': 'An unexpected error occurred.'}), INTERNAL_SERVER_ERROR


def create_entry():
    try:
        req_json = request.get_json(silent=True)
        if req_json is None:
            return jsonify({'error': 'Request body must be valid JSON.'}), BAD_REQUEST

        missing = [f for f in _REQUIRED_CREATE_FIELDS if f not in req_json]
        if missing:
            return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), BAD_REQUEST

        for field in _REQUIRED_CREATE_FIELDS:
            err = _validate_string_field(req_json[field], field)
            if err:
                return jsonify({'error': err}), BAD_REQUEST

        if req_json['player1Name'] == req_json['player2Name']:
            return jsonify({'error': "Player names must be different."}), BAD_REQUEST

        if req_json['winnerName'] not in (req_json['player1Name'], req_json['player2Name']):
            return jsonify({'error': "Winner name must match one of the player names."}), BAD_REQUEST

        battle_entry = BattleEntry.from_json(req_json)
        db.session.add(battle_entry)
        db.session.commit()

        return jsonify({'message': f'Battle entry created with id {battle_entry.id}'}), CREATED
    except Exception:
        logger.exception("Failed to create entry")
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred.'}), INTERNAL_SERVER_ERROR


def get_entry(entry_id):
    try:
        entry = db.session.get(BattleEntry, entry_id)
        if entry is None:
            return jsonify({'message': f'Entry with id {entry_id} was not found'}), NOT_FOUND

        return jsonify({'entry': entry.to_json()})
    except Exception:
        logger.exception("Failed to retrieve entry %s", entry_id)
        return jsonify({'error': 'An unexpected error occurred.'}), INTERNAL_SERVER_ERROR


def partial_update_entry(entry_id):
    try:
        req_json = request.get_json(silent=True)
        if req_json is None:
            return jsonify({'error': 'Request body must be valid JSON.'}), BAD_REQUEST

        entry_to_update = db.session.get(BattleEntry, entry_id)
        if entry_to_update is None:
            return jsonify({'message': f'Entry with id {entry_id} was not found'}), NOT_FOUND

        if 'gameTag' in req_json:
            return jsonify({'message': 'gameTag cannot be updated.'}), BAD_REQUEST

        if 'player1Name' in req_json:
            err = _validate_string_field(
                req_json['player1Name'], 'player1Name')
            if err:
                return jsonify({'error': err}), BAD_REQUEST
            entry_to_update.player_1_name = req_json['player1Name']

        if 'player2Name' in req_json:
            err = _validate_string_field(
                req_json['player2Name'], 'player2Name')
            if err:
                return jsonify({'error': err}), BAD_REQUEST
            entry_to_update.player_2_name = req_json['player2Name']

        if 'winnerName' in req_json:
            winner_name = req_json['winnerName']
            if winner_name not in (entry_to_update.player_1_name, entry_to_update.player_2_name):
                return jsonify({'message': 'Winner name must match player 1 or player 2 name.'}), BAD_REQUEST
            entry_to_update.winner_name = winner_name

        if 'finishedDate' in req_json:
            try:
                entry_to_update.finished_date = datetime.strptime(
                    req_json['finishedDate'], '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                return jsonify({'error': "Invalid 'finishedDate' format. Use 'YYYY-MM-DD HH:MM:SS'."}), BAD_REQUEST

        db.session.commit()
        return jsonify({'message': f'Battle entry with id {entry_id} has been updated'}), OK
    except Exception:
        logger.exception("Failed to update entry %s", entry_id)
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred.'}), INTERNAL_SERVER_ERROR


def delete_entry(entry_id):
    try:
        entry_to_delete = db.session.get(BattleEntry, entry_id)
        if entry_to_delete is None:
            return jsonify({'message': f'Entry with id {entry_id} was not found'}), NOT_FOUND

        db.session.delete(entry_to_delete)
        db.session.commit()
        return jsonify({'message': f'Battle entry with id {entry_id} has been deleted'}), OK
    except Exception:
        logger.exception("Failed to delete entry %s", entry_id)
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred.'}), INTERNAL_SERVER_ERROR
