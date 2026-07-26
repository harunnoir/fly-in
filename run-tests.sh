from pathlib import Path
import traceback

from src.parser.map_parser import parse_map   # change if needed


VALID = Path("tests/valid")
INVALID = Path("tests/invalid")


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def test_valid():
    passed = 0
    total = 0

    for file in sorted(VALID.glob("*.map")):
        total += 1
        try:
            parse_map(file)

            print(f"{GREEN}PASS{RESET} {file.name}")
            passed += 1

        except Exception:
            print(f"{RED}FAIL{RESET} {file.name}")
            traceback.print_exc()

    return passed, total


def test_invalid():
    passed = 0
    total = 0

    for file in sorted(INVALID.glob("*.map")):
        total += 1

        try:
            parse_map(file)

            print(f"{RED}FAIL{RESET} {file.name} (accepted invalid map)")

        except Exception:
            print(f"{GREEN}PASS{RESET} {file.name}")
            passed += 1

    return passed, total


def main():
    print("========== VALID MAPS ==========")
    v_pass, v_total = test_valid()

    print()

    print("========= INVALID MAPS =========")
    i_pass, i_total = test_invalid()

    print()

    print("========== SUMMARY ==========")
    print(f"Valid:   {v_pass}/{v_total}")
    print(f"Invalid: {i_pass}/{i_total}")

    if v_pass == v_total and i_pass == i_total:
        print(f"{GREEN}ALL TESTS PASSED{RESET}")
    else:
        print(f"{RED}SOME TESTS FAILED{RESET}")


if __name__ == "__main__":
    main()
