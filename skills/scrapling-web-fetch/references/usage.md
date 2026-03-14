# Usage

## Basic
```bash
uv run scripts/scrapling_fetch.py <url> 10000
```

## JSON output
```bash
uv run scripts/scrapling_fetch.py <url> 10000 --json
```

## Wrapper
```bash
uv run scripts/fetch-web-content <url> 10000
```

## Batch mode
```bash
uv run scripts/scrapling_fetch.py --batch urls.txt 20000 --json
```

## Site selector overrides
```bash
uv run scripts/scrapling_fetch.py <url> 10000 --selectors /path/to/site-overrides.json
```
