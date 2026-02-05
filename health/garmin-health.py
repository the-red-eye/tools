#!/usr/bin/env python3
"""
Garmin Health Data Fetcher
By HAL 9000

Fetches health data from Garmin Connect API.
Requires: pip install garminconnect

Usage:
    python garmin-health.py              # Today's summary
    python garmin-health.py --date 2026-02-01
    python garmin-health.py --range 7    # Last 7 days
    python garmin-health.py --weight     # Weight history

Environment variables:
    GARMIN_EMAIL - Your Garmin account email
    GARMIN_PASSWORD - Your Garmin account password
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("Please install garminconnect: pip install garminconnect")
    sys.exit(1)

# Session cache location
SESSION_DIR = Path.home() / ".config" / "garmin"
SESSION_FILE = SESSION_DIR / "session"


def get_client():
    """Get authenticated Garmin client."""
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    
    if not email or not password:
        print("Error: Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables")
        sys.exit(1)
    
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    
    client = Garmin(email, password)
    
    # Try to load saved session
    if SESSION_FILE.exists():
        try:
            client.login(SESSION_FILE)
            return client
        except Exception:
            pass
    
    # Fresh login
    client.login()
    client.garth.dump(str(SESSION_FILE))
    return client


def get_daily_summary(client, date):
    """Get daily health summary."""
    date_str = date.strftime("%Y-%m-%d")
    
    summary = {
        "date": date_str,
        "steps": None,
        "sleep_hours": None,
        "stress_avg": None,
        "heart_rate_resting": None,
        "calories": None,
    }
    
    try:
        stats = client.get_stats(date_str)
        summary["steps"] = stats.get("totalSteps")
        summary["calories"] = stats.get("totalKilocalories")
        summary["heart_rate_resting"] = stats.get("restingHeartRate")
        summary["stress_avg"] = stats.get("averageStressLevel")
    except Exception as e:
        print(f"Warning: Could not fetch stats: {e}")
    
    try:
        sleep = client.get_sleep_data(date_str)
        if sleep and "dailySleepDTO" in sleep:
            seconds = sleep["dailySleepDTO"].get("sleepTimeSeconds", 0)
            summary["sleep_hours"] = round(seconds / 3600, 1) if seconds else None
    except Exception as e:
        print(f"Warning: Could not fetch sleep: {e}")
    
    return summary


def print_summary(summary):
    """Pretty print a daily summary."""
    print(f"\n📊 Health Summary for {summary['date']}")
    print("-" * 40)
    
    if summary["steps"]:
        print(f"🚶 Steps: {summary['steps']:,}")
    if summary["sleep_hours"]:
        emoji = "😴" if summary["sleep_hours"] >= 7 else "😫"
        print(f"{emoji} Sleep: {summary['sleep_hours']}h")
    if summary["stress_avg"]:
        emoji = "😌" if summary["stress_avg"] < 40 else "😰"
        print(f"{emoji} Stress: {summary['stress_avg']}")
    if summary["heart_rate_resting"]:
        print(f"❤️ Resting HR: {summary['heart_rate_resting']} bpm")
    if summary["calories"]:
        print(f"🔥 Calories: {summary['calories']:,}")


def main():
    parser = argparse.ArgumentParser(description="Fetch Garmin health data")
    parser.add_argument("--date", help="Date to fetch (YYYY-MM-DD)")
    parser.add_argument("--range", type=int, help="Number of days to fetch")
    parser.add_argument("--weight", action="store_true", help="Show weight history")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    client = get_client()
    
    if args.weight:
        # Weight history
        weights = client.get_weigh_ins(limit=30)
        if args.json:
            print(json.dumps(weights, indent=2))
        else:
            print("\n⚖️ Weight History")
            print("-" * 40)
            for w in weights.get("dailyWeightSummaries", [])[:10]:
                date = w.get("summaryDate")
                kg = w.get("weight", 0) / 1000
                print(f"{date}: {kg:.1f} kg")
    
    elif args.range:
        # Multiple days
        summaries = []
        for i in range(args.range):
            date = datetime.now() - timedelta(days=i)
            summary = get_daily_summary(client, date)
            summaries.append(summary)
            if not args.json:
                print_summary(summary)
        
        if args.json:
            print(json.dumps(summaries, indent=2))
    
    else:
        # Single day
        if args.date:
            date = datetime.strptime(args.date, "%Y-%m-%d")
        else:
            date = datetime.now()
        
        summary = get_daily_summary(client, date)
        
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print_summary(summary)


if __name__ == "__main__":
    main()
