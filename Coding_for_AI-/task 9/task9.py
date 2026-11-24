def parse_payload(raw_packet: list, delimiter: str, /, *,
                  correction_offset: int = 0) -> tuple:

   
   status_tokens = raw_packet[2].split(delimiter)

   
    corrected_sensors = [
        value if "ERROR" in status_tokens
        else value + correction_offset
        for value in raw_packet[1][:]
    ]

   
    return raw_packet[0], corrected_sensors

print("TEST 1")

raw_packet1 = [
    501,
    [12.5, 13.0, 11.8],
    "NOMINAL|CALIBRATED"
]

original1 = raw_packet1[1][:]

result1 = parse_payload(
    raw_packet1, "|", correction_offset=2
)

print("Test 1 ->", result1[0], result1[1])

assert raw_packet1[1] == original1
assert id(result1[1]) != id(raw_packet1[1])

print("Test 1 side-effect assertions passed.")

print("\nTEST 2")

raw_packet2 = [
    502,
    [9.0, 8.5],
    "ERROR|SENSOR FAULT"
]

original2 = raw_packet2[1][:]

result2 = parse_payload(
    raw_packet2, "|", correction_offset=5
)

print("Test 2 ->", result2[0], result2[1])

assert raw_packet2[1] == original2
assert id(result2[1]) != id(raw_packet2[1])

print("Test 2 side-effect assertions passed.")




print("\nTEST 3")

raw_packet3 = [
    503,
    [1.0, 2.0],
    "NOMINAL"
]

result3 = parse_payload(raw_packet3, "|")

print("Test 3 (default offset) ->",
      result3[0], result3[1])

print("\nTEST 4")

try:
    parse_payload(
        raw_packet=raw_packet1,
        delimiter="|"
    )
except TypeError as e:
    print("Test 4 passed. TypeError raised as expected:", e)




print("\nTEST 5")

try:
    parse_payload(raw_packet1, "|", 2)
except TypeError as e:
    print("Test 5 passed. TypeError raised as expected:", e)



print("\nTEST 6")

raw_packet4 = [
    504,
    [10.0, 20.0, 30.0],
    "NOMINAL|CALIBRATED|LOW POWER"
]

result4 = parse_payload(
    raw_packet4, "|", correction_offset=3
)

print("Multiple status codes ->", result4)

print("\nTEST 7")

raw_packet5 = [
    505,
    [],
    "NOMINAL"
]

result5 = parse_payload(
    raw_packet5, "|", correction_offset=5
)

print("Empty sensor list ->", result5)

print("\nTEST 8")

raw_packet6 = [
    506,
    [5.0, 10.0],
    "NOMINAL"
]

default_result = parse_payload(raw_packet6, "|")

zero_result = parse_payload(
    raw_packet6, "|", correction_offset=0
)

print("Default offset:", default_result)
print("Explicit zero:", zero_result)

assert default_result == zero_result

print("\nALL TESTS COMPLETED SUCCESSFULLY!")
