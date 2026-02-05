# Health Tools

## garmin-health.py

Fetch health data from Garmin Connect.

### Setup
```bash
pip install garminconnect
export GARMIN_EMAIL="your@email.com"
export GARMIN_PASSWORD="yourpassword"
```

### Usage
```bash
python garmin-health.py              # Today
python garmin-health.py --date 2026-02-01
python garmin-health.py --range 7    # Last 7 days
python garmin-health.py --weight     # Weight history
python garmin-health.py --json       # JSON output
```
