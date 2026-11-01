#!/usr/bin/env python3
"""Check code citations against the repository and turn them into permanent links.

check [CITATION ...] [--file PATH]
    Confirms that each cited file and line exists, then prints the cited line so
    a reader can compare it with the claim. Exits 1 if any citation is broken.
    A citation looks like src/rules.py:42 or src/rules.py:42-58.

permalink PATH [--write]
    Rewrites local code links in a Markdown file as web links pinned to the
    current commit. Prints the result unless --write is given. A link stays
    local, with a warning, when its target would not open on the web.
"""
import argparse
import os
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit

MD_LINK = re.compile(r"(?<!!)\[([^\]\n]*)\]\(<?([^()<>\n]+?)>?\)")
BARE_CITATION = re.compile(r"`([^`\s]+:\d+(?:-\d+)?)`")
LOCATION = re.compile(r"^(?P<path>.+?)(?::(?P<start>\d+)(?:-(?P<end>\d+))?)?$")
WEB_BLOB = re.compile(r"/(?:-/)?(?:blob|src)/(?P<sha>[0-9a-f]{7,40})/(?P<path>[^#?]+)")
FENCE = re.compile(r"^\s*(```|~~~)")
MAX_SHOWN = 110


def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip()


def repo_root():
    code, out = git("rev-parse", "--show-toplevel")
    return out if code == 0 else None


def is_web(target):
    return target.startswith(("http://", "https://"))


def is_external(target):
    return is_web(target) or target.startswith(("#", "mailto:"))


def parse_location(text):
    match = LOCATION.match(unquote(text.strip()))
    start = int(match["start"]) if match["start"] else None
    end = int(match["end"]) if match["end"] else start
    return match["path"], start, end


def resolve(path, root):
    """Find a cited path relative to the working directory, then the repo root."""
    candidates = [path]
    if root and not os.path.isabs(path):
        candidates.append(os.path.join(root, path))
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.realpath(candidate)
    return None


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read().splitlines()


def shown(line_number, text):
    text = text.strip() or "(blank line, so this citation is probably off)"
    if len(text) > MAX_SHOWN:
        text = text[:MAX_SHOWN] + "..."
    return f"    {line_number}: {text}"


def web_lines(sha, path):
    code, out = git("show", f"{sha}:{path}")
    return out.splitlines() if code == 0 else None


def check_local(citation, root):
    path, start, end = parse_location(citation)
    full = resolve(path, root)
    if full is None:
        return False, [f"BROKEN  {citation}  file not found"]
    if start is None:
        return True, [f"OK      {citation}  file exists, no line cited"]
    return check_range(citation, read_lines(full), start, end)


def check_range(citation, lines, start, end):
    if start < 1 or end < start:
        return False, [f"BROKEN  {citation}  invalid line range"]
    if end > len(lines):
        return False, [f"BROKEN  {citation}  file has only {len(lines)} lines"]
    report = [f"OK      {citation}", shown(start, lines[start - 1])]
    if end > start:
        report.append(shown(end, lines[end - 1]))
    return True, report


def check_web(url, root):
    match = WEB_BLOB.search(urlsplit(url).path)
    if not match or not root:
        return None
    if git("cat-file", "-e", f"{match['sha']}^{{commit}}")[0] != 0:
        return None  # Another repository's link, which this one cannot confirm.
    path = unquote(match["path"])
    lines = web_lines(match["sha"], path)
    if lines is None:
        return False, [f"BROKEN  {path}  not in commit {match['sha'][:10]}"]
    numbers = re.findall(r"\d+", urlsplit(url).fragment)
    if not numbers:
        return True, [f"OK      {path} @ {match['sha'][:10]}"]
    start, end = int(numbers[0]), int(numbers[-1])
    span = f"{start}-{end}" if end > start else str(start)
    return check_range(f"{path}:{span} @ {match['sha'][:10]}", lines, start, end)


def citations_in_markdown(text):
    """Yield (label, target) for links and bare citations outside code fences."""
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for label, target in MD_LINK.findall(line):
            yield label, target.strip()
        for bare in BARE_CITATION.findall(MD_LINK.sub("", line)):
            yield None, bare


def label_conflict(label, target):
    """A visible range must start on the line the link opens."""
    label = (label or "").strip("` ")
    if not LOCATION.match(label) or ":" not in label:
        return None
    label_path, label_start, _ = parse_location(label)
    target_path, target_start, _ = parse_location(target)
    if label_start is None or target_start is None:
        return None
    if os.path.basename(label_path) != os.path.basename(target_path):
        return f"label names {label_path} but link opens {target_path}"
    if label_start != target_start:
        return f"label says line {label_start} but link opens line {target_start}"
    return None


def cmd_check(args):
    root = repo_root()
    items = [(None, citation) for citation in args.citations]
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            items += list(citations_in_markdown(handle.read()))
    if not items:
        print("No citations found.")
        return 1
    broken = checked = 0
    for label, target in items:
        if is_web(target):
            outcome = check_web(target, root)
            if outcome is None:
                continue
        elif is_external(target):
            continue
        else:
            conflict = label_conflict(label, target)
            if conflict:
                outcome = (False, [f"BROKEN  {target}  {conflict}"])
            else:
                location = target
                if label:
                    # Keep the range from the label, because the target holds only the start.
                    label_path, label_start, label_end = parse_location(label.strip("` "))
                    target_path, target_start, _ = parse_location(target)
                    if label_start == target_start and label_end and label_end != label_start:
                        location = f"{target_path}:{label_start}-{label_end}"
                outcome = check_local(location, root)
        passed, report = outcome
        checked += 1
        broken += 0 if passed else 1
        print("\n".join(report))
    print(f"\n{checked} citations checked, {broken} broken.")
    return 1 if broken else 0


def web_base(remote):
    """Return (host, https base URL) from a remote, dropping any embedded credentials."""
    scp = re.match(r"^[^/@]+@([^:/]+):(.+)$", remote)
    if scp:
        host, repo = scp.groups()
    else:
        parts = urlsplit(remote)
        host, repo = parts.hostname, parts.path.lstrip("/")
    if not host or not repo:
        return None, None
    return host.lower(), f"https://{host}/{re.sub(r'[.]git/?$', '', repo)}"


def web_url(host, base, sha, path, start, end):
    encoded = quote(path)
    if "gitlab" in host:
        url = f"{base}/-/blob/{sha}/{encoded}"
        return url + (f"#L{start}-{end}" if start and end != start else f"#L{start}" if start else "")
    if "bitbucket" in host:
        url = f"{base}/src/{sha}/{encoded}"
        return url + (f"#lines-{start}:{end}" if start and end != start else f"#lines-{start}" if start else "")
    if "github" in host:
        url = f"{base}/blob/{sha}/{encoded}"
        return url + (f"#L{start}-L{end}" if start and end != start else f"#L{start}" if start else "")
    return None


def cmd_permalink(args):
    root = repo_root()
    if not root:
        print("Not inside a git repository.", file=sys.stderr)
        return 1
    code, remote = git("remote", "get-url", "origin")
    host, base = web_base(remote) if code == 0 else (None, None)
    if not base or not any(name in host for name in ("github", "gitlab", "bitbucket")):
        print("Links left local: the origin remote is missing or its host is not "
              "GitHub, GitLab or Bitbucket.", file=sys.stderr)
        host = None
    _, sha = git("rev-parse", "HEAD")
    if host and not git("branch", "-r", "--contains", sha)[1]:
        print(f"Links left local: commit {sha[:10]} has not been pushed, so web "
              "links to it would not open. Push it, then run this again.", file=sys.stderr)
        host = None

    warned = set()

    def rewrite(match):
        label, target = match.group(1), match.group(2).strip()
        if is_external(target) or host is None:
            return match.group(0)
        label_path, label_start, label_end = parse_location(label.strip("` "))
        path, start, end = parse_location(target)
        if label_start == start and label_end:
            end = label_end
        full = resolve(path, root)
        if full is None:
            return match.group(0)
        relative = os.path.relpath(full, os.path.realpath(root))
        tracked = git("ls-files", "--error-unmatch", "--", full)[0] == 0
        if not tracked or git("diff", "--quiet", "HEAD", "--", full)[0] != 0:
            if relative not in warned:
                print(f"Left local: {relative} has uncommitted changes or is untracked.",
                      file=sys.stderr)
                warned.add(relative)
            return match.group(0)
        return f"[{label}]({web_url(host, base, sha, relative, start, end)})"

    with open(args.path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            lines[index] = MD_LINK.sub(rewrite, line)
    result = "\n".join(lines)
    if args.write:
        with open(args.path, "w", encoding="utf-8") as handle:
            handle.write(result)
        print(f"Updated {args.path} at commit {sha[:10]}.")
    else:
        print(result)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("citations", nargs="*")
    check.add_argument("--file")
    check.set_defaults(run=cmd_check)
    permalink = commands.add_parser("permalink")
    permalink.add_argument("path")
    permalink.add_argument("--write", action="store_true")
    permalink.set_defaults(run=cmd_permalink)
    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
