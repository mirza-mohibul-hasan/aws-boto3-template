import sys
from pathlib import Path

# Add project root to Python path when this compatibility script is run directly.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.cli import app


if __name__ == "__main__":
    app()
