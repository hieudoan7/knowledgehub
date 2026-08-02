from pathlib import Path


TEST_DATA_DIR = Path(__file__).parent.parent / "data"


def get_test_file(name: str) -> Path:
    return TEST_DATA_DIR / name
