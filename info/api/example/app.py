"""
Example flask application
"""
from typing import Tuple

from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def hello_world() -> Tuple[str, int]:
    """
    Hello world function on the root path.
    """
    return "Hello World!", 200


@app.route("/int", methods=["GET"])
def int_test() -> Tuple[str, int]:
    """
    Test function for integer type.
    """
    return "42", 200

if __name__ == "__main__":
    app.run()
