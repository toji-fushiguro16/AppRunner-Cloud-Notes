import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 128 * 1024
table = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION")).Table(os.environ["TABLE_NAME"])


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/notes")
def list_notes():
    result = table.scan(Limit=50)
    notes = result.get("Items", [])
    notes.sort(key=lambda note: note.get("created_at", ""), reverse=True)
    return jsonify(notes=notes)


@app.post("/notes")
def create_note():
    payload = request.get_json(silent=True)
    text = payload.get("text") if isinstance(payload, dict) else None
    if not isinstance(text, str) or not text.strip() or len(text) > 2000:
        return jsonify(error="Provide note text between 1 and 2000 characters."), 400
    note = {"note_id": str(uuid4()), "text": text.strip(), "created_at": datetime.now(timezone.utc).isoformat()}
    table.put_item(Item=note)
    return jsonify(note=note), 201


@app.delete("/notes/<note_id>")
def delete_note(note_id):
    result = table.delete_item(Key={"note_id": note_id}, ReturnValues="ALL_OLD")
    if "Attributes" not in result:
        return jsonify(error="Note not found."), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
