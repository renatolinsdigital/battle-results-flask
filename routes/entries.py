from flask import Blueprint, request
from controllers.entries import get_all_entries, create_entry, get_entry, partial_update_entry, delete_entry


entries_bp = Blueprint('entries', __name__)


@entries_bp.route('/entries', methods=['GET', 'POST'])
def entries():
    if request.method == 'GET':
        return get_all_entries()

    elif request.method == 'POST':
        return create_entry()


@entries_bp.route('/entry/<int:entry_id>', methods=['GET', 'PATCH', 'DELETE'])
def entry(entry_id):
    if request.method == 'GET':
        return get_entry(entry_id)

    elif request.method == 'PATCH':
        return partial_update_entry(entry_id)

    elif request.method == 'DELETE':
        return delete_entry(entry_id)
