# Domain Search

A Python CLI tool that searches for available domain names across all known TLDs. It supports two modes: **exact search** (e.g., `yourname.computer`, `mysite.dev`) and **domain hack search** (where the TLD forms part of a word, e.g., `creati.ve`, `kosti.ck`). Uses free protocols (DNS lookups and RDAP) requiring no API keys.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
git clone <repo-url>
cd domain-search
uv sync
```

## Usage

### Exact Search

Search for `<word>.{tld}` across all known TLDs:

```bash
uv run python main.py myname
```

### Domain Hack Search

Find creative domain hacks where the TLD forms part of a word:

```bash
uv run python main.py --hack creative
```

This finds domains like `creati.ve` (reads as "creative").

### Combined Search

Run both exact and hack search together:

```bash
uv run python main.py myname --hack creative
```

### Options

| Flag | Description |
|------|-------------|
| `--hack WORD` | Find domain hacks for the given word |
| `--concurrency N` | Max concurrent DNS lookups (default: 50) |
| `--skip-rdap` | Skip RDAP verification (faster but less accurate) |
| `--output FILE` | Export results to `.json`, `.jsonl`, or `.csv` file |
| `--tld TLD [TLD ...]` | Filter to specific TLDs (e.g., `--tld com io`) |

### Export Results

Export to JSON, JSONL, or CSV (format auto-detected from file extension):

```bash
uv run python main.py myname --output results.json
uv run python main.py myname --output results.jsonl
uv run python main.py myname --output results.csv
```

## How It Works

1. **TLD List**: Fetches the complete TLD list from IANA (~1,500 TLDs), cached locally for 24 hours
2. **DNS Check**: Performs async DNS lookups (NS/SOA records) to classify domains as registered, possibly available, or unknown
3. **RDAP Verification**: For "possibly available" domains, queries RDAP servers for confirmation (skippable with `--skip-rdap`)
4. **Results**: Displays a color-coded table with availability status, sorted with available domains first

## Running Tests

```bash
uv run pytest tests/ -v
```
