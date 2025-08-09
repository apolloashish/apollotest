from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

from dotenv import load_dotenv

from moodle_client import MoodleClient, MoodleError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Moodle API quickstart: fetch site info")
    parser.add_argument("--base-url", dest="base_url", help="Moodle base URL, e.g. https://moodle.example.com")
    parser.add_argument("--token", dest="token", help="Moodle web service token")
    parser.add_argument("--timeout", dest="timeout", type=float, default=15.0, help="HTTP timeout in seconds (default: 15)")
    return parser.parse_args()


def main() -> int:
    load_dotenv()  # Load variables from a local .env if present

    args = parse_args()

    base_url: Optional[str] = args.base_url or os.getenv("MOODLE_BASE_URL")
    token: Optional[str] = args.token or os.getenv("MOODLE_TOKEN")

    if not base_url or not token:
        print(
            "Missing configuration. Provide --base-url and --token, or set MOODLE_BASE_URL and MOODLE_TOKEN in the environment.",
            file=sys.stderr,
        )
        return 2

    client = MoodleClient(base_url=base_url, token=token, timeout_seconds=args.timeout)

    try:
        site_info = client.get_site_info()
    except MoodleError as err:
        print(f"Moodle error: {err}", file=sys.stderr)
        return 1
    except Exception as err:  # noqa: BLE001 keep broad to show unexpected failures for a demo
        print(f"Unexpected error: {err}", file=sys.stderr)
        return 1

    print(json.dumps(site_info, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())