from flask import jsonify
from urllib.parse import urlparse

def is_Valid_Url(url: str) -> bool:
    try:
        result = urlparse(url)

        return all([
            result.scheme in ["http", "https"],
            result.netloc
        ])
    except:
        return False
    

def response(success=True, message="", data=None, status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code