

import csv
import random
import uuid
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Reproducibility
random.seed(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "gps_mobility_pings.csv"

# Bengaluru study area mobility hotspots
CITY_HOTSPOTS = [
    (12.9716, 77.5946),  # City Center
    (12.9352, 77.6245),  # Koramangala
    (12.9784, 77.6408),  # Indiranagar
    (12.9698, 77.7500),  # Whitefield
    (12.9250, 77.5838),  # Jayanagar
    (12.9116, 77.6389),  # HSR Layout
    (12.9569, 77.7011),  # Marathahalli
    (13.0035, 77.5700),  # Malleshwaram
    (12.8399, 77.6770),  # Electronic City
    (13.0358, 77.5970),  # Hebbal
    (13.1007, 77.5963),  # Yelahanka
    (12.9100, 77.6830),  # Sarjapur Road
]

START_TIME = datetime(2026, 11, 1, 0, 0, 0)

DAYS_OF_ACTIVITY = 30


def generate_gps_ping(device_ids):
    """Generate one anonymized synthetic GPS ping."""

    hotspot = random.choice(CITY_HOTSPOTS)

    latitude = hotspot[0] + random.uniform(-0.008, 0.008)
    longitude = hotspot[1] + random.uniform(-0.008, 0.008)

    device_id = random.choice(device_ids)

    random_seconds = random.randint(
        0,
        DAYS_OF_ACTIVITY * 24 * 60 * 60 - 1
    )

    timestamp = START_TIME + timedelta(
        seconds=random_seconds
    )

    return [
        device_id,
        round(latitude, 6),
        round(longitude, 6),
        timestamp.strftime("%Y-%m-%d %H:%M:%S")
    ]


def generate_dataset(total_records, batch_size):
    """Generate GPS records in batches to control memory usage."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0

    # Create reusable anonymized device IDs
    device_count = min(total_records, 100_000)

    device_ids = [
        f"DEV_{i:07d}"
        for i in range(1, device_count + 1)
    ]

    print("Starting GPS mobility data generation...")
    print(f"Target records: {total_records:,}")
    print(f"Unique device pool: {device_count:,}")
    print(f"City hotspots: {len(CITY_HOTSPOTS)}")

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "DeviceID",
            "Latitude",
            "Longitude",
            "Timestamp"
        ])

        while generated < total_records:

            current_batch = min(
                batch_size,
                total_records - generated
            )

            rows = [
                generate_gps_ping(device_ids)
                for _ in range(current_batch)
            ]

            writer.writerows(rows)

            generated += current_batch

            print(
                f"Generated {generated:,} / "
                f"{total_records:,} GPS pings"
            )

    print("\nGPS dataset generation completed!")
    print(f"Total records: {generated:,}")
    print(f"Device pool: {device_count:,}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate synthetic Bengaluru GPS mobility data"
    )

    parser.add_argument(
        "--records",
        type=int,
        default=1_000_000
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=100_000
    )

    args = parser.parse_args()

    if args.records <= 0 or args.batch_size <= 0:
        parser.error(
            "Records and batch size must be positive."
        )

    generate_dataset(
        args.records,
        args.batch_size
    )
