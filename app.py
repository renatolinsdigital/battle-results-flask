from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort
from flask_cors import cross_origin
from config.flask import FLASK_RUN_PORT, FLASK_RUN_HOST, FLASK_DEBUG, FLASK_SECRET_KEY
from config.status_code_consts import CREATED, NOT_FOUND, OK, BAD_REQUEST
from config.assets_registering import register_assets_for
from db_models.battle_entry import BattleEntry
from config.database import db, configure_local_database


# Create a Flask application instance with a secret
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Configure the database
configure_local_database(app)

# Attach assets and static files
register_assets_for(app)

# Initialize the Flask application with the database
db.init_app(app)


@app.route('/')
def index():
    # Query the database for all entries in descending order by ID
    entries = BattleEntry.query.order_by(BattleEntry.id.desc()).all()

    # Render the index.html template with the entries data
    return render_template('index.html', entries=entries)


@app.route('/entries', methods=['GET', 'POST', 'PUT'])
@cross_origin()
def entries():
    if request.method == 'GET':
        # Query the database for all entries
        entries = BattleEntry.query.all()

        # Convert the entries to a list of dictionaries
        entries_list = []
        for entry in entries:
            entry_dict = entry.to_json()
            entries_list.append(entry_dict)

        # Return the entries as JSON
        return jsonify({'entries': entries_list})

    elif request.method == 'POST':
        req_json = request.get_json()

        has_required_fields = (
            'gameTag' in req_json
            and 'player1Name' in req_json
            and 'player2Name' in req_json
            and 'winnerName' in req_json
            and 'finishedDate' in req_json
        )
        if not has_required_fields:
            return abort(BAD_REQUEST)

        # Create a new BattleEntry object from the JSON data
        battle_entry = BattleEntry.from_json(req_json)

        # Save the new BattleEntry object to the database
        db.session.add(battle_entry)
        db.session.commit()

        # Return a success response
        return jsonify({'message': f'Battle entry created with id {battle_entry.id}'}), CREATED

    elif request.method == 'PUT':
        req_json = request.get_json()

        # Check if 'id' field is present in the JSON data
        if 'id' not in req_json:
            return abort(BAD_REQUEST)

        # Get the ID of the entry to update
        entry_id = req_json['id']

        # Query the database for the entry with the given ID
        entry_to_update = BattleEntry.query.get(entry_id)

        # If the entry does not exist, return 404 Not Found
        if entry_to_update is None:
            return abort(NOT_FOUND)

        # Update the entry with the new data (current value is kept by default if requisition is not informing a new one)
        entry_to_update.game_tag = req_json.get(
            'gameTag', entry_to_update.game_tag)
        entry_to_update.player_1_name = req_json.get(
            'player1Name', entry_to_update.player_1_name)
        entry_to_update.player_2_name = req_json.get(
            'player2Name', entry_to_update.player_2_name)
        entry_to_update.winner_name = req_json.get(
            'winnerName', entry_to_update.winner_name)
        entry_to_update.finished_date = datetime.strptime(
            req_json.get('finishedDate'), '%Y-%m-%d %H:%M:%S')

        # Commit the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': f'Battle entry with id {entry_id} updated'}), OK

    else:
        return abort(BAD_REQUEST)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
