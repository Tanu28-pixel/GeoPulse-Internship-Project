
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

# Simulated city movement hotspots (latitude, longitude)
CITY_HOTSPOTS = [
    (12.9716, 77.5946),  # City center
    (12.9352, 77.6245),  # Commercial area
    (12.9784, 77.6408),  # Residential area
    (12.9591, 77.6974),  # Business district
    (12.9141, 77.6411)   # Retail area
]

START_TIME = datetime(2026, 11, 1, 0, 0, 0)


def generate_gps_ping(device_ids):
    """Generate one anonymized synthetic GPS ping."""

    hotspot = random.choice(CITY_HOTSPOTS)

    latitude = hotspot[0] + random.uniform(-0.008, 0.008)
    longitude = hotspot[1] + random.uniform(-0.008, 0.008)

    # Reuse device IDs to simulate repeated mobile activity
    device_id = random.choice(device_ids)

    random_seconds = random.randint(0, 30 * 24 * 60 * 60)
    timestamp = START_TIME + timedelta(seconds=random_seconds)

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

    device_count = min(total_records, 100_000)

    device_ids = [
        f"DEV_{i:07d}"
        for i in range(1, device_count + 1)
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "DeviceID",
            "Latitude",
            "Longitude",
            "Timestamp"
        ])

        while generated < total_records:
            current_batch = min(batch_size, total_records - generated)

            rows = [
                generate_gps_ping(device_ids)
                for _ in range(current_batch)
            ]

            writer.writerows(rows)
            generated += current_batch

            print(
                f"Generated {generated:,} / {total_records:,} GPS pings"
            )

    print("\nGPS dataset generation completed!")
    print(f"Total records: {generated:,}")
    print(f"Output file: {OUTPUT_FILE}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic GPS mobility data"
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
        parser.error("Records and batch size must be positive.")

    generate_dataset(args.records, args.batch_size)
