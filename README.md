# repo-release-notes

Generate a Markdown release-note draft from local Git commit subjects, grouped by conventional commit type.

## Status

Initial prototype, created in October 2026. This is a small,
independent starter project, without claims of production deployment or adoption.

## Installation

Python 3.10+ is required. No third-party Python packages are needed.
Copy this directory, then run commands from inside it.

## Usage

```sh
python3 cli.py --repo /path/to/a/git/repository --since v0.1.0 --until HEAD
```

Run `python3 cli.py --help` for options. Reports go to standard output unless an
output file is specified. Input errors return status 2.

## Limitations

Requires Git. Reads local commit subjects only; no GitHub API, pull request retrieval, automatic tagging or publishing. An omitted --since includes all reachable history.

## Development and contributing

Keep changes narrowly scoped. Include a reproducible example for a bug report.
Use synthetic fixtures rather than personal, proprietary or research data.
Run the project checks from this directory:

```sh
python3 -m unittest discover -s tests -v
```

## License

MIT; see [LICENSE](LICENSE).
