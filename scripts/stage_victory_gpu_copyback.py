"""Stage two public VIctory sparse-copyback fixes in a disposable local Git clone.

Never edits the source working tree or its existing runtime binary. It does not
download or inspect game content and does not claim a Mac GPU performance win.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

UPSTREAM_URL = "https://github.com/Marvisak/VIctory.git"
COMMITS = (
    "cd94d35388765f85d4dd88f24d444e018c468ccd",
    "940d32f69b22265690a0b5a15d6ded572ba33baf",
)


class StageError(RuntimeError):
    pass


def git(*args, cwd=None, check=True):
    command = ["git"]
    if cwd is not None:
        command.extend(["-C", str(cwd), "-c", "core.hooksPath=/dev/null"])
    command.extend(args)
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise StageError(f"Git command failed ({result.returncode}): "
                         f"{' '.join(args)}\n{result.stderr.strip()}")
    return result


def stage(source, output, commits=COMMITS, fetch=False, min_free_mib=1024):
    source = Path(source).expanduser().resolve(strict=True)
    output = Path(output).expanduser().absolute()
    if output.exists() or not output.parent.is_dir():
        raise StageError("output must be a NEW path under an existing directory")
    if output == source or source in output.parents:
        raise StageError("output must be outside the source tree")
    if len(commits) != 2 or any(not re.fullmatch(r"[a-f0-9]{40}", c) for c in commits):
        raise StageError("expected two pinned full Git commit SHAs")
    if min_free_mib < 0:
        raise StageError("invalid minimum free space")
    if shutil.disk_usage(output.parent).free < min_free_mib * 1024 * 1024:
        raise StageError("insufficient free disk space for isolated staging")
    root = Path(git("rev-parse", "--show-toplevel", cwd=source).stdout.strip()).resolve()
    if root != source:
        raise StageError("source must point to the root of a Git working tree")
    head = git("rev-parse", "HEAD", cwd=source).stdout.strip()
    # A self-contained clone, not a shared-object worktree. Source files,
    # existing checkouts, Git refs and the known-good executable stay intact.
    git("clone", "--no-hardlinks", "--no-checkout", "--", str(source), str(output))
    git("checkout", "-b", "3r1/upstream-copyback", head, cwd=output)
    if fetch:
        git("fetch", "--no-tags", UPSTREAM_URL, "main", cwd=output)
    for commit in commits:
        if git("cat-file", "-e", f"{commit}^{{commit}}", cwd=output, check=False).returncode:
            raise StageError("upstream commit missing in isolated clone; rerun with --fetch")
    if git("merge-base", "--is-ancestor", commits[0], commits[1],
           cwd=output, check=False).returncode:
        raise StageError("the selected upstream commits are not in the expected order")
    outcomes = []
    for commit in commits:
        if git("merge-base", "--is-ancestor", commit, "HEAD",
               cwd=output, check=False).returncode == 0:
            outcomes.append({"sha": commit, "status": "already_present"})
            continue
        result = git("-c", "user.name=3r1 Local Staging",
                     "-c", "user.email=staging@local.invalid",
                     "cherry-pick", "-x", commit, cwd=output, check=False)
        if result.returncode:
            # Do not mask conflicts, silently skip safety checks or rewrite
            # the source. Leave the isolated checkout inspectable.
            git("cherry-pick", "--abort", cwd=output, check=False)
            raise StageError(f"upstream {commit} needs a manual rebase in the "
                             f"isolated copy:\n{result.stderr.strip()}")
        outcomes.append({"sha": commit, "status": "cherry_picked"})
    report = {
        "source_head": head,
        "staged_head": git("rev-parse", "HEAD", cwd=output).stdout.strip(),
        "upstream": UPSTREAM_URL,
        "changes": outcomes,
        "real_gpu_test": "NOT_RUN",
        "game_boot": "NOT_TESTED",
        "source_untouched": True,
    }
    (output / "3r1-upstream-staging.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="existing local VIctory Git checkout")
    parser.add_argument("--output", required=True, help="new isolated directory outside source")
    parser.add_argument("--fetch", action="store_true",
                        help="fetch public VIctory main into the COPY, never source")
    parser.add_argument("--min-free-mib", type=int, default=1024)
    args = parser.parse_args()
    try:
        report = stage(args.source, args.output, fetch=args.fetch,
                       min_free_mib=args.min_free_mib)
    except (StageError, OSError) as error:
        parser.exit(1, f"VIctory upstream staging FAIL: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
