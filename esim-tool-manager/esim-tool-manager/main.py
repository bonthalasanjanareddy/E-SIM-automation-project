import argparse
import sys

from tool_manager.checker import check_all
from tool_manager.installer import install_tool
from tool_manager.registry import TOOLS
from tool_manager.verify import run_smoke_test


def print_table(results):
    print(f"{'Software':<12}{'Status':<12}{'Version':<12}Path")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<12}{r['status']:<12}{r['version']:<12}{r['path']}")


def verify_ngspice(results):
    ngspice = next((r for r in results if r["name"] == "Ngspice"), None)
    if not ngspice or ngspice["status"] != "Installed":
        print("\nVerify: ngspice is not installed.")
        return False
    ok, message = run_smoke_test(ngspice["path"])
    print(f"\nVerify: {'OK' if ok else 'FAILED'} - {message}")
    return ok


def main():
    parser = argparse.ArgumentParser(description="Check and install eSim-related tools.")
    parser.add_argument("--check", action="store_true",
                        help="only print the status table (no prompts); exit 1 if anything is missing")
    parser.add_argument("--verify", action="store_true",
                        help="also run a small ngspice simulation to prove it works")
    args = parser.parse_args()

    results = check_all(TOOLS)
    print_table(results)

    missing = [r["name"] for r in results if r["status"] == "Missing"]

    if args.check:
        ok = not missing
        if args.verify:
            ok = verify_ngspice(results) and ok
        sys.exit(0 if ok else 1)

    if missing:
        print(f"\nMissing: {', '.join(missing)}")
        answer = input("Install missing tools now? (y/n): ").strip().lower()
        if answer == "y":
            for tool in TOOLS:
                if tool["name"] in missing:
                    print(f"Installing {tool['name']}...")
                    ok, message = install_tool(tool)
                    print(("  OK: " if ok else "  FAILED: ") + message)
            print("\nRe-checking...\n")
            results = check_all(TOOLS)
            print_table(results)
    else:
        print("\nAll tools are installed.")

    if args.verify:
        verify_ngspice(results)


if __name__ == "__main__":
    main()
