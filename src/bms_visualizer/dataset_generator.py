import csv
import random


def generate_battery_timeseries(duration_seconds=600, interval_seconds=1, filename="battery_data.csv"):
    soc = 85.0           # Initial SoC %
    pack_capacity_ah = 50.0  # Total capacity
    r_int = 0.09         # Internal resistance in Ohms
    nominal_ocv_base = 45.0  # Base OCV offset
    mode = 'cruise'

    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "elapsed_s", "soc_pct", "pack_current_a", "pack_voltage_v"])

        current = 0.0
        for t in range(0, duration_seconds + 1, interval_seconds):
            mins, secs = divmod(t, 60)
            timestamp = f"{mins:02d}:{secs:02d}"

            # Simple simulated driving cycle: random profile transitions
            if t % 60 == 0:
                mode = random.choices(["cruise", "accel", "regen", "idle"], weights=[0.4, 0.3, 0.15, 0.15])[0]

            if mode == "accel":
                current = max(0.0, current + random.uniform(1.0, 3.0))
                current = min(current, 35.0)
            elif mode == "cruise":
                current = 12.0 + random.uniform(-2.0, 2.0)
            elif mode == "regen":
                current = -random.uniform(5.0, 15.0)
            else:
                current = 0.0

            # Coulomb counting for SoC
            # delta_ah = current * (hours)
            delta_ah = (current * interval_seconds) / 3600.0
            soc -= (delta_ah / pack_capacity_ah) * 100.0

            # Linear approximation of OCV with SoC + IR drop + sensor noise
            ocv = nominal_ocv_base + (soc / 100.0) * 8.5
            voltage = ocv - (current * r_int) + random.gauss(0, 0.02)

            writer.writerow([timestamp, t, round(soc, 3), round(current, 2), round(voltage, 2)])

    print(f"Generated data written to {filename}")

if __name__ == "__main__":
    generate_battery_timeseries(duration_seconds=1000, interval_seconds=1)
