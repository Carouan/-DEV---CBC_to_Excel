"""Update utilities for the CBC to Excel CLI and portable executable."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen

DEFAULT_REPO = "Carouan/-DEV---CBC_to_Excel"
DEFAULT_RELEASE_API = (
    f"https://api.github.com/repos/{DEFAULT_REPO}/releases/latest"
)
DEFAULT_EXE_NAME = "cbc-to-excel.exe"


@dataclass(frozen=True)
class ReleaseInfo:
    """Metadata about a GitHub release asset."""

    version: str
    asset_name: str
    download_url: str


@dataclass(frozen=True)
class UpdateCheckResult:
    """Outcome of an update check against GitHub Releases."""

    current_version: str
    latest_version: str | None
    update_available: bool
    message: str
    asset_url: str | None = None


def _parse_version(value: str) -> tuple[int, ...]:
    """Parse a version string into a comparable tuple of integers.

    Args:
        value: Version string such as "v0.1.0" or "0.1.0".

    Returns:
        Tuple of numeric components for comparison.
    """
    numbers = re.findall(r"\d+", value)
    return tuple(int(part) for part in numbers)


def _is_newer_version(current: str, latest: str) -> bool:
    """Compare two versions and return True if latest is newer."""
    return _parse_version(latest) > _parse_version(current)


def _request_json(url: str, timeout: int = 5) -> dict:
    """Fetch JSON data from a URL."""
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "cbc-to-excel",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _find_exe_asset(assets: Iterable[dict]) -> tuple[str, str] | None:
    """Find the Windows executable asset in a list of GitHub assets."""
    for asset in assets:
        name = asset.get("name", "")
        if name.lower() == DEFAULT_EXE_NAME.lower():
            return name, asset.get("browser_download_url", "")
    return None


def get_latest_release(timeout: int = 5) -> ReleaseInfo | None:
    """Retrieve the latest GitHub release and exe asset metadata.

    Args:
        timeout: Timeout in seconds for the HTTP request.

    Returns:
        A ReleaseInfo instance if a suitable asset is found, otherwise None.
    """
    data = _request_json(DEFAULT_RELEASE_API, timeout=timeout)
    tag = data.get("tag_name")
    if not tag:
        return None

    asset_match = _find_exe_asset(data.get("assets", []))
    if not asset_match:
        return None
    asset_name, url = asset_match
    if not url:
        return None
    return ReleaseInfo(version=tag, asset_name=asset_name, download_url=url)


def check_for_updates(current_version: str, timeout: int = 5) -> UpdateCheckResult:
    """Check if a newer release is available on GitHub.

    Args:
        current_version: Currently running application version.
        timeout: Timeout in seconds for the HTTP request.

    Returns:
        UpdateCheckResult describing the outcome.
    """
    try:
        release = get_latest_release(timeout=timeout)
    except (URLError, OSError, json.JSONDecodeError) as exc:
        return UpdateCheckResult(
            current_version=current_version,
            latest_version=None,
            update_available=False,
            message=f"Vérification des mises à jour impossible: {exc}",
        )

    if not release:
        return UpdateCheckResult(
            current_version=current_version,
            latest_version=None,
            update_available=False,
            message="Aucune release trouvée sur GitHub.",
        )

    latest_version = release.version.lstrip("v")
    is_newer = _is_newer_version(current_version, latest_version)

    message = (
        f"Nouvelle version disponible: {latest_version} (actuelle: {current_version})."
        if is_newer
        else f"Version à jour: {current_version}."
    )

    return UpdateCheckResult(
        current_version=current_version,
        latest_version=latest_version,
        update_available=is_newer,
        message=message,
        asset_url=release.download_url if is_newer else None,
    )


def is_frozen_executable() -> bool:
    """Return True if running as a bundled executable."""
    return getattr(sys, "frozen", False)


def _write_update_script(exe_path: Path, new_exe_name: str) -> Path:
    """Create the update.bat script that replaces the executable."""
    script_path = exe_path.with_name("update.bat")
    script = "\n".join(
        [
            "@echo off",
            "setlocal",
            "timeout /t 2 /nobreak >nul",
            f"move /y \"{new_exe_name}\" \"{exe_path.name}\"",
            f"start \"\" \"{exe_path.name}\"",
        ]
    )
    script_path.write_text(script, encoding="utf-8")
    return script_path


def download_latest_exe(asset_url: str, destination: Path, timeout: int = 30) -> None:
    """Download the latest executable to the destination path."""
    request = Request(asset_url, headers={"User-Agent": "cbc-to-excel"})
    with urlopen(request, timeout=timeout) as response:
        destination.write_bytes(response.read())


def perform_portable_update(current_version: str, timeout: int = 30) -> bool:
    """Download and prepare an update for the portable Windows executable.

    Args:
        current_version: Current version string.
        timeout: Timeout in seconds for download.

    Returns:
        True if an update script was prepared, False otherwise.
    """
    if os.name != "nt":
        print("La mise à jour portable est uniquement disponible sous Windows.")
        return False

    if not is_frozen_executable():
        print(
            "La mise à jour portable est disponible uniquement pour l'exécutable."
        )
        return False

    result = check_for_updates(current_version, timeout=timeout)
    print(result.message)
    if not result.update_available or not result.asset_url:
        return False

    exe_path = Path(sys.executable)
    new_exe_name = "cbc-to-excel.new.exe"
    new_exe_path = exe_path.with_name(new_exe_name)

    download_latest_exe(result.asset_url, new_exe_path, timeout=timeout)
    script_path = _write_update_script(exe_path, new_exe_name)

    print(
        "Mise à jour téléchargée. Exécutez update.bat pour finaliser "
        "la mise à jour."
    )
    print(f"Script de mise à jour: {script_path}")
    return True


def maybe_notify_update(current_version: str) -> None:
    """Check for updates and notify if a newer version exists."""
    result = check_for_updates(current_version)
    if result.update_available:
        print(result.message)


def throttled_update_check(current_version: str, min_interval: int = 0) -> None:
    """Check for updates with an optional delay for startup ergonomics."""
    if min_interval > 0:
        time.sleep(min_interval)
    maybe_notify_update(current_version)
