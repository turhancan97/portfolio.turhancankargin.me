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
  - Requests English place names (Accept-Language: en) and maps country codes to English.
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
FSQ_LOCALE = "en"
FALLBACK_CITY = "Kraków"
FALLBACK_COUNTRY = "Poland"
MAX_AGE_DAYS = 14
LABEL = "Currently in"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "_data" / "current_location.yml"


def api_version() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def fsq_get(path: str, token: str, params: dict | None = None) -> dict:
    query = {"oauth_token": token, "v": api_version(), "locale": FSQ_LOCALE}
    if params:
        query.update(params)
    url = f"{FSQ_API}{path}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Accept-Language": FSQ_LOCALE,
        },
    )
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


# ISO 3166-1 alpha-2 → English short country name (fallback if API locale is ignored).
COUNTRY_EN_BY_CC = {
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua and Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AO": "Angola",
    "AQ": "Antarctica",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AX": "Åland Islands",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BL": "Saint Barthélemy",
    "BM": "Bermuda",
    "BN": "Brunei",
    "BO": "Bolivia",
    "BQ": "Caribbean Netherlands",
    "BR": "Brazil",
    "BS": "Bahamas",
    "BT": "Bhutan",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos Islands",
    "CD": "Democratic Republic of the Congo",
    "CF": "Central African Republic",
    "CG": "Republic of the Congo",
    "CH": "Switzerland",
    "CI": "Côte d'Ivoire",
    "CK": "Cook Islands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CV": "Cape Verde",
    "CW": "Curaçao",
    "CX": "Christmas Island",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands",
    "FM": "Micronesia",
    "FO": "Faroe Islands",
    "FR": "France",
    "GA": "Gabon",
    "GB": "United Kingdom",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GG": "Guernsey",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard Island and McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IM": "Isle of Man",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Iran",
    "IS": "Iceland",
    "IT": "Italy",
    "JE": "Jersey",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "Saint Kitts and Nevis",
    "KP": "North Korea",
    "KR": "South Korea",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Laos",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova",
    "ME": "Montenegro",
    "MF": "Saint Martin",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "MK": "North Macedonia",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "Saint Pierre and Miquelon",
    "PN": "Pitcairn Islands",
    "PR": "Puerto Rico",
    "PS": "Palestine",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russia",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "Saint Helena",
    "SI": "Slovenia",
    "SJ": "Svalbard and Jan Mayen",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "SS": "South Sudan",
    "ST": "São Tomé and Príncipe",
    "SV": "El Salvador",
    "SX": "Sint Maarten",
    "SY": "Syria",
    "SZ": "Eswatini",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TL": "Timor-Leste",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TR": "Turkey",
    "TT": "Trinidad and Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan",
    "TZ": "Tanzania",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UM": "United States Minor Outlying Islands",
    "US": "United States",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Vatican City",
    "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela",
    "VG": "British Virgin Islands",
    "VI": "United States Virgin Islands",
    "VN": "Vietnam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "XK": "Kosovo",
    "YE": "Yemen",
    "YT": "Mayotte",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
}


def merge_location(list_loc: dict, detail_loc: dict) -> dict:
    """Prefer non-empty fields from either list or detail venue.location."""
    merged = dict(list_loc or {})
    for key, value in (detail_loc or {}).items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, list) and not value:
            continue
        existing = merged.get(key)
        if existing is None or existing == "" or existing == []:
            merged[key] = value
    return merged


def merge_venue(list_venue: dict, detail_venue: dict) -> dict:
    """Combine list + detail venue payloads; detail often omits city/country."""
    if not list_venue:
        return dict(detail_venue or {})
    if not detail_venue:
        return dict(list_venue)
    return {
        **list_venue,
        **detail_venue,
        "location": merge_location(
            list_venue.get("location") or {},
            detail_venue.get("location") or {},
        ),
    }


def extract_location(venue: dict, *, near: str = "") -> tuple[str, str]:
    location = venue.get("location") or {}
    city = (
        (location.get("city") or location.get("town") or location.get("state") or near or "")
        .strip()
    )
    cc = (location.get("cc") or "").strip().upper()
    country = COUNTRY_EN_BY_CC.get(cc) or (location.get("country") or "").strip()
    formatted = location.get("formattedAddress")
    if not city and formatted:
        if isinstance(formatted, str):
            parts = [part.strip() for part in formatted.split(",") if part.strip()]
        elif isinstance(formatted, list):
            parts = [str(part).strip() for part in formatted if part and str(part).strip()]
        else:
            parts = []
        if parts:
            city = parts[0]
    if not city and location.get("address"):
        city = str(location["address"]).strip()
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

    venue = merge_venue(latest.get("venue") or {}, checkin.get("venue") or {})
    near = (checkin.get("near") or latest.get("near") or "").strip()
    city, country = extract_location(venue, near=near)
    if not city or not country:
        return fallback_record(
            synced_at,
            f"venue location is incomplete (city={city!r}, country={country!r})",
        )

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
