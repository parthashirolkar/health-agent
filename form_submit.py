from db import personal_data_collection, notes_collection
from datetime import datetime


def update_personal_info(existing, update_type, **kwargs):
    # Update the in-memory object
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}
    # Update in ChromaDB (replace document)
    personal_data_collection.update(
        ids=[str(existing["_id"])], documents=[str(existing)]
    )
    return existing


def add_note(note, profile_id):
    # ChromaDB expects ids and documents as lists
    note_id = f"{profile_id}_{int(datetime.now().timestamp())}"
    new_note = {
        "user_id": profile_id,
        "text": note,
        "metadata": {"injested": datetime.now().isoformat()},
    }
    notes_collection.add(
        ids=[note_id], documents=[note], metadatas=[new_note["metadata"]]
    )
    new_note["_id"] = note_id
    return new_note


def delete_note(_id):
    # Remove by id in ChromaDB
    notes_collection.delete(ids=[str(_id)])
