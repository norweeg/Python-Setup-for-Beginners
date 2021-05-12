from itertools import chain
import logging
import sys
from json import loads
from os import cpu_count, environ
from pathlib import Path
from subprocess import CalledProcessError, run

stdout = logging.StreamHandler(sys.stdout)
stdout.addFilter(lambda r: r.levelno < logging.WARNING)
stderr = logging.StreamHandler(sys.stderr)
stderr.setLevel(logging.WARNING)

logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    handlers=[stdout, stderr],
)

# Get location of conda
conda_exe = Path(environ["CONDA_EXE"])

# Add default anaconda channel as lower priority channel to conda-forge in base
run(f"{conda_exe} config --env --append channels defaults".split(" "))

# apply system conda config
configuration = {
    "channel_priority": "strict",
    "pip_interop_enabled": "true",
    "report_errors": "true",
    "default_threads": max(1, cpu_count() // 2),
}

for key, value in configuration.items():
    run(f"{conda_exe} config --system --set {key} {value}".split(" "))

try:
    # Update everything installed in base environment
    run(
        f"{conda_exe} update --yes --name base --all".split(" "),
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )
except CalledProcessError:
    logging.exception("Unable to update packages installed in base conda environment")

try:
    # Install Anaconda Navigator in base environment
    run(
        f"{conda_exe} install --yes --name base anaconda-navigator menuinst".split(" "),
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )
except CalledProcessError:
    logging.exception("Failed to install Anaconda Navigator")
    sys.exit(1)


try:
    # Search for anaconda metapackage in default repository, get info on it
    search_results = loads(
        run(
            f"{conda_exe} search --info --override-channels -c defaults anaconda --json".split(
                " "
            ),
            capture_output=True,
        ).stdout
    ).get("anaconda")

    # find the latest non-custom version number
    latest_version = (
        [
            result
            for result in search_results
            if int(result["timestamp"])
            == max(
                {
                    int(result["timestamp"])
                    for result in search_results
                    if result.get("version") != "custom"
                }
            )
        ]
        .pop()
        .get("version")
    )

    # find all builds that match the lastest non-custom version number
    choices = {
        result.get("build"): result.get("depends")
        for result in search_results
        if result.get("version") == latest_version
    }

    # find the python versions that the matching builds depend on
    python_versions = (
        d.split(" ")[1]
        for d in chain.from_iterable(choices.values())
        if d.split(" ")[0].lower() == "python"
    )

    # pick the latest python version
    python_version = max(python_versions)

    # pick the build that depends on the latest python version
    build = [
        b
        for b, d in choices.items()
        if f"python {python_version}" in (_[: _.rfind(" ")] for _ in d)
    ].pop()

    # Get only dependencies of most recent build
    depends = {d.split(" ")[0] for d in choices[build]}

except (CalledProcessError, KeyError):
    logging.exception("Failed to get dependencies for Anaconda")
    sys.exit(2)

# Add in some other packages
with open(
    list(Path(__file__).resolve().parents)[1] / "requirements/anaconda.txt", "r"
) as requires:
    depends |= {line.strip() for line in requires.readlines()}

try:
    # Find packages that aren't able to be found in conda-forge
    try:
        not_found = set(
            loads(
                run(
                    f"{conda_exe} create --yes --name anaconda --dry-run --json".split(
                        " "
                    )
                    + list(depends),
                    capture_output=True,
                ).stdout
            ).get("packages")
        )
    except (KeyError, TypeError):
        not_found = set()

    # Install "anaconda" environment from conda-forge channel
    run(
        f"{conda_exe} create --yes --name anaconda".split(" ")
        + sorted(list(depends - not_found)),
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )
except (CalledProcessError, KeyError):
    logging.exception("Failed to get dependencies for Anaconda")
    sys.exit(3)
