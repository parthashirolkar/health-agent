from db import personal_data_collection, notes_collection
from datetime import datetime
import json


def update_personal_info(existing, update_type, **kwargs):
    # Update the in-memory object
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}
    # Update in ChromaDB (replace document) - using JSON instead of str()
    personal_data_collection.update(
        ids=[str(existing["_id"])], documents=[json.dumps(existing)]
    )
    return existing


def add_note(note, profile_id):
    # ChromaDB expects ids and documents as lists
    note_id = f"{profile_id}_{int(datetime.now().timestamp())}"
    new_note = {
        "user_id": profile_id,
        "text": note,
        "metadata": {"injested": datetime.now().isoformat()},
        "_id": note_id
    }
    # Store the complete note object as JSON instead of just the text
    notes_collection.add(
        ids=[note_id], documents=[json.dumps(new_note)], metadatas=[new_note["metadata"]]
    )
    return new_note


def delete_note(_id):
    # Remove by id in ChromaDB
    notes_collection.delete(ids=[str(_id)])
