from flask import Blueprint, render_template
from db_models.battle_entry import BattleEntry

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    # Query the database for all entries in descending order by ID
    entries = BattleEntry.query.order_by(BattleEntry.id.desc()).all()

    # Render the index.html template with the entries data
    return render_template('index.html', entries=entries)
