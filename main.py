"""Domain Search CLI - backwards compatibility wrapper.

This file is kept for backwards compatibility with the old `uv run python main.py` usage.
The actual CLI implementation has been moved to domain_search.cli module.
"""

from domain_search.cli import main

if __name__ == "__main__":
    main()
