# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "packaging==24.2",
#   "urllib3==2.3.0",
# ]
# ///
"""Update polyscan-pre-commit to the latest versions of pyscn and polyscan."""

import datetime
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import urllib3
from packaging.version import Version

ROOT = Path(__file__).parent


@dataclass(frozen=True)
class Mirror:
    package: str
    index_url: str
    # Key of the registry document that maps every published version.
    versions_key: str
    # File that pins the version, and how the pin is written there.
    path: str
    pin: str

    @property
    def pin_pattern(self) -> str:
        return re.escape(self.pin).replace(r"\{\}", r"([^\s\"']+)")

    def current_version(self) -> Version:
        content = (ROOT / self.path).read_text()
        matches = re.findall(self.pin_pattern, content)
        assert len(matches) == 1, f"{self.path} should pin {self.package} exactly once"
        return Version(matches[0])

    def latest_version(self) -> Version:
        response = urllib3.request("GET", self.index_url)
        if response.status != 200:
            raise RuntimeError(f"Failed to fetch {self.package} versions from {self.index_url}")
        # Betas are not mirrored: a pre-commit `rev` is meant to be something a
        # project can sit on.
        versions = (Version(v) for v in response.json()[self.versions_key])
        return max(v for v in versions if not v.is_prerelease)

    def pin_to(self, version: Version) -> None:
        path = ROOT / self.path
        path.write_text(re.sub(self.pin_pattern, self.pin.format(version), path.read_text()))


MIRRORS = (
    Mirror(
        package="pyscn",
        index_url="https://pypi.org/pypi/pyscn/json",
        versions_key="releases",
        path="pyproject.toml",
        pin='"pyscn=={}"',
    ),
    Mirror(
        package="polyscan",
        index_url="https://registry.npmjs.org/polyscan",
        versions_key="versions",
        path=".pre-commit-hooks.yaml",
        pin="polyscan@{}",
    ),
)


def main() -> None:
    updated = False
    for mirror in MIRRORS:
        current, latest = mirror.current_version(), mirror.latest_version()
        if latest > current:
            mirror.pin_to(latest)
            updated = True

    if not updated:
        print("Already up to date with pyscn and polyscan.")
        return

    tag = next_tag()
    readme = ROOT / "README.md"
    readme.write_text(re.sub(r"rev: v[\d.]+", f"rev: {tag}", readme.read_text()))

    versions = ", ".join(f"{m.package} {m.current_version()}" for m in MIRRORS)
    paths = ["README.md", *(m.path for m in MIRRORS)]
    subprocess.run(["git", "add", *paths], check=True)
    subprocess.run(["git", "commit", "-m", f"Mirror: {versions}"], check=True)
    subprocess.run(["git", "tag", tag], check=True)


def next_tag() -> str:
    """Date the release, numbering any further releases on the same day."""
    base = datetime.datetime.now(datetime.UTC).strftime("v%Y.%m.%d")
    existing = set(subprocess.check_output(["git", "tag", "--list", f"{base}*"], text=True).split())
    tag, n = base, 1
    while tag in existing:
        n += 1
        tag = f"{base}.{n}"
    return tag


if __name__ == "__main__":
    main()
