import sys

from flask import Flask, render_template

import yaml2dot

app = Flask(__name__)

# Check for Flask dependency, and provide a helpful error message if it's missing.
try:
    from flask import Flask
except ImportError:
    print(
        "Flask is not installed. Please install it by running 'pip install Flask'",
        file=sys.stderr,
    )
    sys.exit(1)


@app.route("/")
def index():
    """
    Generates the graph and renders it in an HTML template.
    """
    try:
        dot = yaml2dot.get_graph_object()
        # Use pipe to get the SVG content as a string
        svg_content = dot.pipe(format="svg").decode("utf-8")
    except Exception as e:
        # If anything goes wrong during graph generation, show an error page.
        # This could happen if the yaml files are not found, for example.
        return render_template("error.html", error_message=str(e))

    return render_template("index.html", svg_content=svg_content)


if __name__ == "__main__":
    # Adding host='0.0.0.0' makes the app accessible from the network
    app.run(debug=True, host="0.0.0.0")
