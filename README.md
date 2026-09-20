# pyscn-pre-commit

A [pre-commit](https://pre-commit.com) hook for [pyscn](https://github.com/ludo-technologies/pyscn),
an intelligent Python code quality analyzer.

This is a mirror repository. It holds no source of its own: it installs `pyscn`
from PyPI so that `pre-commit` does not have to clone the main repository, which
carries the Go implementation. The mirror follows PyPI automatically, so every
`pyscn` release gets a matching tag here within a few hours.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/ludo-technologies/pyscn-pre-commit
    rev: v1.32.1
    hooks:
      - id: pyscn
```

Then:

```console
$ pre-commit install
$ pre-commit run pyscn --all-files
```

The hook runs `pyscn check`, which analyses the whole project and fails the
commit on complexity, dead code, circular dependency, and parse issues. Configure
thresholds through `.pyscn.toml` or `[tool.pyscn]` in `pyproject.toml` as usual;
see the [pyscn documentation](https://pyscn.ludo-tech.org).

To pass extra flags, use `args`:

```yaml
      - id: pyscn
        args: [--select, complexity, --max-complexity, "15"]
```

The hook also works with [prek](https://github.com/j178/prek).

## Platform support

`pyscn` ships prebuilt wheels for Linux x86_64 and arm64, macOS arm64, and
Windows x86_64. There is no source distribution, so the hook cannot be installed
on platforms without a wheel. Use `brew install pyscn` or `go install` on those.

## License

MIT, matching pyscn.
