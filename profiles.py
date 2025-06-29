from db import personal_data_collection, notes_collection
import json


def get_values(_id):
    return {
        "_id": _id,
        "general": {
            "name": "",
            "age": 30,
            "weight": 60.0,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male",
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
        },
    }


def create_profile(_id):
    profile_values = get_values(_id)
    # ChromaDB expects ids and documents as lists - using JSON instead of str()
    personal_data_collection.add(ids=[str(_id)], documents=[json.dumps(profile_values)])
    return _id, profile_values


def get_profile(_id):
    # Query by id
    results = personal_data_collection.get(ids=[str(_id)])
    if results and results.get("documents"):
        # Documents are returned as JSON strings - safe to parse
        try:
            return json.loads(results["documents"][0])
        except json.JSONDecodeError:
            # Fallback for old string format
            import ast
            return ast.literal_eval(results["documents"][0])
    return None


def get_notes(_id):
    # Query notes by user_id (stored as metadata)
    results = notes_collection.query(
        query_texts=[""], where={"user_id": str(_id)}, n_results=100
    )
    # Documents are returned as a list of lists
    notes = []
    if results and results.get("documents"):
        for doc_list in results["documents"]:
            for doc in doc_list:
                try:
                    notes.append(json.loads(doc))
                except json.JSONDecodeError:
                    # Fallback for old string format
                    import ast
                    notes.append(ast.literal_eval(doc))
    return notes
