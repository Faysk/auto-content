import re
import uuid

def slugify(text, max_length=40):
    return re.sub(r"\W+", "_", text.lower())[:max_length].strip("_")

def client_id():
    return str(uuid.uuid4())
