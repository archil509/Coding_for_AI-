
import os
from typing import Tuple


def process_log_stream(file_path: str, chunk_size: int, /) -> Tuple[int, float]:
    """
    Read a telemetry file in fixed-size byte chunks.

    Returns:
        Tuple containing valid record count and mean sensor value.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Target path '{file_path}' not found."
        )

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    valid_count = 0
    total_value = 0.0
    leftover = b""
    sentinel_found = False

    def process_line(raw_line):
        nonlocal valid_count, total_value, sentinel_found

        line = raw_line.decode("utf-8").strip()

        if line == "END OF LOG":
            sentinel_found = True
            return

        if sentinel_found or not line:
            return

        fields = line.split(",")

        if len(fields) != 3:
            return

        try:
            value = float(fields[2].strip())
        except ValueError:
            return

        valid_count += 1
        total_value += value

    # Read file in binary mode
    with open(file_path, "rb") as file_obj:

        for chunk in iter(
            lambda: file_obj.read(chunk_size),
            b""
        ):

            leftover += chunk

            # Separate complete lines from incomplete data
            *complete_lines, leftover = leftover.split(b"\n")

            for raw_line in complete_lines:
                process_line(raw_line)

    # Process the final leftover after reading ends
    if leftover:
        process_line(leftover)

    # Check required sentinel
    if not sentinel_found:
        print("Warning: END OF LOG not found. File may be truncated.")

    # Calculate mean safely
    mean_value = (
        total_value / valid_count
        if valid_count > 0
        else 0.0
    )

    return valid_count, mean_value


# DRIVER CODE

if __name__ == "__main__":

    sample_file = "telemetry_log.csv"

    # Create sample telemetry log
    with open(sample_file, "w", encoding="utf-8") as file:

        file.write("2026-01-01T00:00:01,SENSOR_A,14.5\n")
        file.write("2026-01-01T00:00:02,SENSOR_B,NaN_READING\n")
        file.write("2026-01-01T00:00:03,SENSOR_C,\n")
        file.write("2026-01-01T00:00:04,SENSOR_A,16.2\n")
        file.write("2026-01-01T00:00:05,MALFORMED_ROW_TOO_FEW_FIELDS\n")
        file.write("2026-01-01T00:00:06,SENSOR_B,15.0\n")
        file.write("END OF LOG\n")

    # Test with different chunk sizes
    chunk_sizes = [1, 3, 7, 16, 32, 64, 128, 1000]

    for size in chunk_sizes:

        result = process_log_stream(sample_file, size)

        print(
            f"Chunk size = {size:<5} -> "
            f"Valid records: {result[0]}, "
            f"Mean: {result[1]:.2f}"
        )

    print("\nAll tests completed successfully.")
