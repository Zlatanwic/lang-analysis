"""Programming Language Type System Knowledge Graph.

Generates an interactive HTML dashboard for exploring type system features
across programming languages. Run this script to build the dashboard, then
open the generated HTML file in a browser.

Usage:
    python main.py              # Generate dashboard and open in browser
    python main.py --serve      # Generate and start a local HTTP server
    python main.py --output X   # Write dashboard to custom path
"""

import argparse
import http.server
import json
import os
import sys
import threading
import webbrowser
from pathlib import Path

from src.data_processing import load_data, prepare_dashboard_data
from src.dashboard_template import DASHBOARD_HTML

OUTPUT_DIR = Path(__file__).parent / "output"
DEFAULT_OUTPUT = OUTPUT_DIR / "dashboard.html"


def generate_dashboard(output_path: Path | None = None) -> Path:
    """Generate the interactive dashboard HTML file."""
    if output_path is None:
        output_path = DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = load_data()
    dashboard_data = prepare_dashboard_data(data)
    data_json = json.dumps(dashboard_data, ensure_ascii=False)

    html = DASHBOARD_HTML.replace("__DASHBOARD_DATA__", data_json)
    output_path.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {output_path}")
    return output_path


def serve(output_path: Path, port: int = 8080):
    """Start a local HTTP server for the dashboard."""
    os.chdir(output_path.parent)
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(("", port), handler)
    url = f"http://localhost:{port}/{output_path.name}"
    print(f"Serving at {url}")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a type system knowledge graph dashboard"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output path for the HTML file",
    )
    parser.add_argument(
        "--serve", "-s",
        action="store_true",
        help="Start a local HTTP server after generating",
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="Port for the HTTP server (default: 8080)",
    )
    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None
    path = generate_dashboard(output_path)

    if args.serve:
        serve(path, args.port)
    else:
        print(f"Open {path} in your browser to view the dashboard.")
        print("Or run with --serve to start a local server.")


if __name__ == "__main__":
    main()
