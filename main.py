"""Programming Language Type System Knowledge Graph.

Generates structured dashboard data for the Vue frontend.

Usage:
    python main.py
    python main.py --json-output custom/path/dashboard-data.json
"""

import argparse
import json
from pathlib import Path

from src.data_processing import load_data, prepare_dashboard_data

FRONTEND_DIR = Path(__file__).parent / "frontend"
DEFAULT_JSON_OUTPUT = FRONTEND_DIR / "public" / "dashboard-data.json"


def generate_dashboard_json(output_path: Path | None = None) -> Path:
    """Generate frontend-consumable dashboard data JSON."""
    if output_path is None:
        output_path = DEFAULT_JSON_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = load_data()
    dashboard_data = prepare_dashboard_data(data)
    output_path.write_text(
        json.dumps(dashboard_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Dashboard JSON generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate Vue frontend dashboard data"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path for the generated dashboard JSON file",
    )
    parser.add_argument(
        "--json-output",
        type=str,
        default=None,
        help="Optional JSON output path for the Vue frontend data bundle",
    )
    args = parser.parse_args()

    if args.output and not args.json_output:
        json_output_path = Path(args.output)
    else:
        json_output_path = Path(args.json_output) if args.json_output else None

    generated_json_path = generate_dashboard_json(json_output_path)
    print(f"Vue frontend data ready at {generated_json_path}.")
    print("Run `cd frontend && pnpm dev` for local development.")
    print("Run `cd frontend && pnpm build` for a production bundle.")


if __name__ == "__main__":
    main()
