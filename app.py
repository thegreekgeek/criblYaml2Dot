import sys
import os

from flask import Flask, render_template
from dotenv import load_dotenv

from cribl_api import get_cached_api_client
from graph_generator import generate_graph

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """
    Main route that generates the graph and renders it.

    Returns:
        str: Rendered HTML template with the graph SVG.

    Renders:
        index.html: If graph generation is successful.
        error.html: If an exception occurs (e.g., API failure).
    """
    try:
        api_client = get_cached_api_client()
        dot = generate_graph(api_client)
        # Use pipe to get the SVG content as a string
        svg_content = dot.pipe(format="svg").decode("utf-8")
    except Exception as e:
        # If anything goes wrong during graph generation, show an error page.
        # This could happen if the API is not available, for example.
        return render_template("error.html", error_message=str(e))

    return render_template("index.html", svg_content=svg_content)


if __name__ == "__main__":
    # Adding host='0.0.0.0' makes the app accessible from the network
    # Use DEBUG from environment variable, default to False
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0")
