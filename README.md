# polyscan-pre-commit

[pre-commit](https://pre-commit.com) hooks for the polyscan code quality analyzers:

| Hook id | Analyzer | Languages |
|---|---|---|
| `pyscn` | [pyscn](https://github.com/ludo-technologies/pyscn) | Python |
| `polyscan` | [polyscan](https://github.com/ludo-technologies/polyscan) | JavaScript, TypeScript, Go, Rust, C++ |

This is a mirror repository. It holds no source of its own: the hooks install
`pyscn` from PyPI and `polyscan` from npm, so `pre-commit` does not have to clone
the main repositories. The mirror follows both registries automatically, and
every new release of either analyzer gets a date tag (`vYYYY.MM.DD`) here within
a few hours. The commit message of each tag names the versions it pins.

## Usage

Add the hooks for the languages in your project to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/ludo-technologies/polyscan-pre-commit
    rev: v1.31.1
    hooks:
      - id: pyscn
      - id: polyscan
```

Then:

```console
$ pre-commit install
$ pre-commit run --all-files
```

Each hook runs the analyzer's `check` command, which analyses the whole project
and fails the commit on complexity, dead code, circular dependency, and parse
issues. Clone detection is not run. A hook is skipped when the commit touches
no file in its languages.

Configure thresholds as usual, through `.pyscn.toml` or `[tool.pyscn]` in
`pyproject.toml` for pyscn and `.polyscan.toml` for polyscan; see the
[documentation](https://docs.codescan.dev).

To pass extra flags, use `args`:

```yaml
      - id: pyscn
        args: [--select, complexity, --max-complexity, "15"]
```

The hooks also work with [prek](https://github.com/j178/prek).

## Platform support

Both analyzers ship prebuilt binaries for Linux x86_64 and arm64, macOS arm64,
and Windows x86_64 only. Intel Macs are not supported.

## License

MIT, matching pyscn and polyscan.
