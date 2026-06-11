#!/usr/bin/env python3
"""
Grihine Soap — one-command Hostinger deploy.

Mirrors the site files (repo root) to the Hostinger FTP account
(public_html). Uses FTPS (explicit TLS) when the server supports it and
falls back to plain FTP otherwise.

NOTE: the primary host is GitHub Pages (just `git push`). This script is the
fallback for deploying the same site to Hostinger instead.

Credentials come from environment variables (see ../.deploy.env.example):
  HOSTINGER_FTP_HOST   e.g. 145.79.x.x  or  ftp.yourdomain.com
  HOSTINGER_FTP_USER   e.g. u123456789.yourdomain.com
  HOSTINGER_FTP_PASS   the FTP password from hPanel
  HOSTINGER_REMOTE_DIR optional, default: public_html
"""

import ftplib
import os
import posixpath
import ssl
import sys

LOCAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKIP_NAMES = {".DS_Store", "README-HOSTINGER.md", "README.md", "deploy.sh", "CNAME"}
SKIP_DIRS = {".git", "deploy", ".claude"}


def connect(host: str, user: str, password: str) -> ftplib.FTP:
    try:
        ftps = ftplib.FTP_TLS(host, timeout=30, context=ssl.create_default_context())
        ftps.login(user, password)
        ftps.prot_p()  # encrypt the data channel too
        print(f"✓ Connected with FTPS (TLS) to {host}")
        return ftps
    except Exception as exc:
        print(f"  FTPS failed ({exc}); retrying with plain FTP…")
        ftp = ftplib.FTP(host, timeout=30)
        ftp.login(user, password)
        print(f"✓ Connected with plain FTP to {host}")
        return ftp


def ensure_remote_dir(ftp: ftplib.FTP, path: str) -> None:
    parts = [p for p in path.split("/") if p]
    current = ""
    for part in parts:
        current = posixpath.join(current, part) if current else part
        try:
            ftp.mkd(current)
        except ftplib.error_perm:
            pass  # already exists


def upload_tree(ftp: ftplib.FTP, local_root: str, remote_root: str) -> int:
    count = 0
    for dirpath, dirnames, filenames in os.walk(local_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and (not d.startswith(".") or d == ".well-known")]
        rel = os.path.relpath(dirpath, local_root)
        remote_dir = remote_root if rel == "." else posixpath.join(remote_root, rel.replace(os.sep, "/"))
        ensure_remote_dir(ftp, remote_dir)
        for name in sorted(filenames):
            if name in SKIP_NAMES or name.startswith("."):
                continue
            local_path = os.path.join(dirpath, name)
            remote_path = posixpath.join(remote_dir, name)
            with open(local_path, "rb") as fh:
                ftp.storbinary(f"STOR {remote_path}", fh)
            size = os.path.getsize(local_path)
            print(f"  ↑ {remote_path}  ({size:,} bytes)")
            count += 1
    return count


def main() -> int:
    host = os.environ.get("HOSTINGER_FTP_HOST", "")
    user = os.environ.get("HOSTINGER_FTP_USER", "")
    password = os.environ.get("HOSTINGER_FTP_PASS", "")
    remote_dir = os.environ.get("HOSTINGER_REMOTE_DIR", "public_html")

    missing = [n for n, v in [("HOSTINGER_FTP_HOST", host), ("HOSTINGER_FTP_USER", user), ("HOSTINGER_FTP_PASS", password)] if not v]
    if missing:
        print("✗ Missing credentials: " + ", ".join(missing))
        print("  Copy .deploy.env.example to .deploy.env, fill it in, then run ./deploy.sh")
        return 1

    if not os.path.isdir(LOCAL_DIR):
        print(f"✗ Local folder not found: {LOCAL_DIR}")
        return 1

    print(f"Deploying {os.path.abspath(LOCAL_DIR)} → {host}:/{remote_dir}")
    ftp = connect(host, user, password)
    try:
        uploaded = upload_tree(ftp, LOCAL_DIR, remote_dir)
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()

    print(f"✓ Done — {uploaded} files uploaded. Site is live (hard-refresh with Ctrl+Shift+R).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
