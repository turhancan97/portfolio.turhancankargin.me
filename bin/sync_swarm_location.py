#!/usr/bin/env python3
"""Sync Swarm (Foursquare) check-ins into _data/current_location.yml.

Setup (one-time):
  1. Create a Foursquare developer app: https://foursquare.com/developers/home
  2. Set a redirect URI (e.g. https://localhost/callback).
  3. Open in a browser (replace CLIENT_ID and REDIRECT_URI):
       https://foursquare.com/oauth2/authenticate?client_id=CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI
  4. After approving, exchange the code for an access token:
       curl "https://foursquare.com/oauth2/access_token?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&grant_type=authorization_code&redirect_uri=REDIRECT_URI&code=CODE"
  5. Add the oauth_token value as GitHub repo secret FOURSQUARE_ACCESS_TOKEN.

Behavior:
  - Uses the latest check-in (public or private) from GET /v2/users/self/checkins.
  - If the check-in is older than 14 days, falls back to Kraków, Poland.
  - Scheduled via .github/workflows/sync-swarm-location.yml (every 2 days).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

FSQ_API = "https://api.foursquare.com/v2"
FALLBACK_CITY = "Kraków"
FALLBACK_COUNTRY = "Poland"
MAX_AGE_DAYS = 14
LABEL = "Currently in"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "_data" / "current_location.yml"


def api_version() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def fsq_get(path: str, token: str, params: dict | None = None) -> dict:
    query = {"oauth_token": token, "v": api_version()}
    if params:
        query.update(params)
    url = f"{FSQ_API}{path}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    meta = payload.get("meta", {})
    if meta.get("code") != 200:
        raise RuntimeError(f"Foursquare API error {meta.get('code')}: {meta.get('errorDetail')}")
    return payload["response"]


def parse_checkin_time(raw: str | int | float) -> datetime:
    if isinstance(raw, (int, float)):
        return datetime.fromtimestamp(raw, tz=timezone.utc)
    text = str(raw).strip()
    if text.isdigit():
        return datetime.fromtimestamp(int(text), tz=timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text).astimezone(timezone.utc)


def extract_location(venue: dict) -> tuple[str, str]:
    location = venue.get("location") or {}
    city = (location.get("city") or "").strip()
    country = (location.get("country") or "").strip()
    if not city and location.get("formattedAddress"):
        parts = [part.strip() for part in location["formattedAddress"] if part and part.strip()]
        if parts:
            city = parts[0]
    return city, country


def build_record(
    *,
    city: str,
    country: str,
    source: str,
    checkin_at: datetime | None,
    synced_at: datetime,
) -> dict:
    return {
        "city": city,
        "country": country,
        "label": LABEL,
        "source": source,
        "checkin_at": checkin_at.isoformat().replace("+00:00", "Z") if checkin_at else None,
        "synced_at": synced_at.isoformat().replace("+00:00", "Z"),
    }


def fallback_record(synced_at: datetime, reason: str) -> dict:
    print(f"Using fallback ({reason}).", file=sys.stderr)
    return build_record(
        city=FALLBACK_CITY,
        country=FALLBACK_COUNTRY,
        source="fallback",
        checkin_at=None,
        synced_at=synced_at,
    )


def sync_location(token: str) -> dict:
    synced_at = datetime.now(timezone.utc)
    cutoff = synced_at - timedelta(days=MAX_AGE_DAYS)

    try:
        listing = fsq_get("/users/self/checkins", token, {"limit": 1})
    except (urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Failed to list check-ins: {exc}") from exc

    checkins = listing.get("checkins", {}).get("items", [])
    if not checkins:
        return fallback_record(synced_at, "no check-ins found")

    latest = checkins[0]
    checkin_id = latest.get("id")
    if not checkin_id:
        return fallback_record(synced_at, "latest check-in has no id")

    try:
        details = fsq_get(f"/checkins/{checkin_id}", token)
    except (urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Failed to fetch check-in {checkin_id}: {exc}") from exc

    checkin = details.get("checkin") or latest
    created_raw = checkin.get("createdAt") or latest.get("createdAt")
    if not created_raw:
        return fallback_record(synced_at, "check-in has no createdAt")

    checkin_at = parse_checkin_time(created_raw)
    if checkin_at < cutoff:
        return fallback_record(
            synced_at,
            f"latest check-in is older than {MAX_AGE_DAYS} days ({checkin_at.date().isoformat()})",
        )

    venue = checkin.get("venue") or {}
    city, country = extract_location(venue)
    if not city or not country:
        return fallback_record(synced_at, "venue location is incomplete")

    print(f"Using Swarm check-in from {checkin_at.date().isoformat()}: {city}, {country}")
    return build_record(
        city=city,
        country=country,
        source="swarm",
        checkin_at=checkin_at,
        synced_at=synced_at,
    )


def yaml_scalar(value: str | None) -> str:
    if value is None:
        return "null"
    text = str(value)
    if not text:
        return '""'
    if any(ch in text for ch in ":#[]{}'\",&*?|>!%@`\n") or text.startswith(" ") or text.endswith(" "):
        return json.dumps(text, ensure_ascii=False)
    return text


def write_yaml(record: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Synced from Swarm via .github/workflows/sync-swarm-location.yml "
        "(bin/sync_swarm_location.py).\n"
    )
    body = "\n".join(
        [
            f"city: {yaml_scalar(record['city'])}",
            f"country: {yaml_scalar(record['country'])}",
            f"label: {yaml_scalar(record['label'])}",
            f"source: {yaml_scalar(record['source'])}",
            f"checkin_at: {yaml_scalar(record['checkin_at'])}",
            f"synced_at: {yaml_scalar(record['synced_at'])}",
            "",
        ]
    )
    OUTPUT_PATH.write_text(header + body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fallback-only",
        action="store_true",
        help="Write Kraków fallback without calling the Foursquare API.",
    )
    args = parser.parse_args()

    if args.fallback_only:
        write_yaml(fallback_record(datetime.now(timezone.utc), "manual fallback-only run"))
        print(f"Wrote fallback to {OUTPUT_PATH}")
        return 0

    token = os.environ.get("FOURSQUARE_ACCESS_TOKEN", "").strip()
    if not token:
        print("FOURSQUARE_ACCESS_TOKEN is not set.", file=sys.stderr)
        return 1

    try:
        record = sync_location(token)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    write_yaml(record)
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
