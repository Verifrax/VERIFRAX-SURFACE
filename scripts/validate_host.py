#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_CLASSES = {"root", "tool", "reference"}
REQUIRED_KEYS = {
    "host", "repo", "hostClass", "role", "title", "description", "deployMode", "adjacentHosts"
}
FORBIDDEN = {
    "www": ["execution surface", "authority issuance", "proof publication", "verification runtime"],
    "api": ["github pages", "static github pages host"],
    "verify": ["proof publication surface", "authority issuance surface"],
    "proof": ["verification ui", "governed execution"],
    "authority": ["proof publication", "public verifier"],
    "runtime": ["public authority issuance", "intake surface"],
    "enforcement": ["docs root", "public verifier"],
    "archive": ["execution runtime", "authority issuance"],
    "apply": ["proof publication", "execution runtime"],
    "docs": ["authority issuance", "governed execution"],
    "status": ["proof publication", "authority issuance"],
}

def main():
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    cfg_path = repo_root / "surface.host.json"
    if not cfg_path.exists():
        raise SystemExit(f"missing config: {cfg_path}")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS - set(cfg)
    if missing:
        raise SystemExit(f"missing keys: {sorted(missing)}")
    if cfg["hostClass"] not in ALLOWED_CLASSES:
        raise SystemExit(f"invalid hostClass: {cfg['hostClass']}")
    role = cfg["role"]
    bad_terms = FORBIDDEN.get(role, [])
    blob = "\n".join(str(v) for v in cfg.values()).lower()
    hits = [term for term in bad_terms if term in blob]
    if hits:
        raise SystemExit(f"forbidden terms for role {role}: {hits}")
    print(f"[ok] {cfg['repo']} -> {cfg['host']} ({cfg['hostClass']}/{role})")

if __name__ == "__main__":
    main()
