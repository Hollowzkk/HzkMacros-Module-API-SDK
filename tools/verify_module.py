#!/usr/bin/env python3
"""HzkMacros Module SDK v4 offline JAR structural verifier (Python 3 standard library).

Checks packaging and metadata, not Java bytecode verification, Fabric remapping,
third-party security, or runtime registration. Test against the final game JAR too.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import zipfile

ID = re.compile(r"[a-z][a-z0-9_]{2,63}\Z")
FABRIC_ID = re.compile(r"[a-z0-9][a-z0-9_.-]{0,127}\Z")
ENTRYPOINT = re.compile(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+\Z", re.ASCII)
DOC_PATH = re.compile(r"docs/[A-Za-z0-9_/-]{1,128}\.json\Z")
KINDS = {"action", "variable", "event", "iterator", "service", "feature", "guide"}
MAX_JAR = 32 * 1024 * 1024
MAX_JSON = 256 * 1024
MAX_TOTAL = 64 * 1024 * 1024


class ModuleError(ValueError):
    pass


def reject(message: str) -> None:
    raise ModuleError(message)


def text_field(obj: dict, key: str, max_chars: int, required: bool = False) -> str:
    value = obj.get(key)
    if value is None and not required:
        return ""
    if not isinstance(value, str) or (required and not value.strip()) or len(value.strip()) > max_chars:
        reject(f"Invalid field {key}: expected {'nonempty ' if required else ''}string <= {max_chars} chars")
    return value.strip()


def json_entry(archive: zipfile.ZipFile, name: str) -> dict:
    info = archive.getinfo(name)
    if info.is_dir() or info.file_size > MAX_JSON:
        reject(f"Invalid JSON entry size: {name}")
    raw = archive.read(info)
    if len(raw) > MAX_JSON:
        reject(f"JSON exceeds {MAX_JSON} bytes: {name}")
    try:
        result = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError) as error:
        reject(f"Malformed UTF-8 JSON {name}: {error}")
    if not isinstance(result, dict):
        reject(f"Expected JSON object: {name}")
    return result


def dependencies(manifest: dict, owner: str) -> dict:
    root = manifest.get("dependencies", {})
    if not isinstance(root, dict):
        reject("dependencies must be a JSON object")
    result: dict[str, list[str]] = {}
    for key, max_items, pattern in (
        ("modules", 32, ID), ("optionalModules", 32, ID),
        ("fabricMods", 64, FABRIC_ID), ("optionalFabricMods", 64, FABRIC_ID),
    ):
        items = root.get(key, [])
        if not isinstance(items, list) or len(items) > max_items:
            reject(f"dependencies.{key} must be an array of at most {max_items} items")
        names = []
        for entry in items:
            if isinstance(entry, str):
                ident = entry.strip()
            elif isinstance(entry, dict):
                ident = text_field(entry, "id", 64 if pattern is ID else 128, True)
                if "version" in entry:
                    text_field(entry, "version", 128, True)
            else:
                reject(f"Invalid dependencies.{key} entry")
            if not pattern.fullmatch(ident) or ident in names:
                reject(f"Invalid or duplicated dependencies.{key} id: {ident}")
            names.append(ident)
        result[key] = names
    if owner in result["modules"] + result["optionalModules"]:
        reject("Module cannot depend on itself")
    for a, b in (("modules", "optionalModules"), ("fabricMods", "optionalFabricMods")):
        overlap = set(result[a]) & set(result[b])
        if overlap:
            reject(f"Required/optional dependency overlap: {sorted(overlap)}")
    return result


def verify(path: Path) -> dict:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_JAR:
        reject("Not a regular JAR, symbolic link, or exceeds 32 MiB")
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if len(infos) > 4096 or sum(info.file_size for info in infos) > MAX_TOTAL:
                reject("JAR contains too many entries or too much uncompressed data")
            names = [info.filename for info in infos]
            if len(set(names)) != len(names):
                reject("Duplicate JAR entry names")
            if any(name.startswith("/") or "\\" in name or ".." in name.split("/") for name in names):
                reject("Unsafe JAR entry path")
            if "hzkmacros.module.json" not in names:
                reject("Missing hzkmacros.module.json")
            if any(name.startswith("dev/hzk/hzkmacros/api/module/") and name.endswith(".class") for name in names):
                reject("Do not bundle HzkMacros public API classes; declare compileOnly")
            manifest = json_entry(archive, "hzkmacros.module.json")
            if manifest.get("schemaVersion", 1) != 1:
                reject("Unsupported manifest schemaVersion")
            ident = text_field(manifest, "id", 64, True)
            if not ID.fullmatch(ident):
                reject("Invalid module id")
            name = text_field(manifest, "name", 100, True)
            version = text_field(manifest, "version", 64, True)
            entrypoint = text_field(manifest, "entrypoint", 200, True)
            if not ENTRYPOINT.fullmatch(entrypoint) or entrypoint.replace(".", "/") + ".class" not in names:
                reject("Missing or invalid compiled entrypoint class")
            api = manifest.get("apiVersion")
            if type(api) is not int or not 1 <= api <= 4:
                reject("apiVersion must be an integer from 1 through 4")
            if "hzkmacrosVersion" in manifest:
                text_field(manifest, "hzkmacrosVersion", 128, True)
            deps = dependencies(manifest, ident)
            paths = manifest.get("documentation", {})
            if not isinstance(paths, dict):
                reject("documentation must be a JSON object")
            total_docs = 0
            for lang, location in paths.items():
                if lang not in ("en_us", "pt_br") or not isinstance(location, str) or not DOC_PATH.fullmatch(location) or ".." in location:
                    reject(f"Invalid documentation path/language: {lang}")
                if location not in names:
                    reject(f"Declared docs entry missing: {location}")
                docs = json_entry(archive, location)
                if docs.get("schemaVersion") != 1 or docs.get("moduleId") != ident:
                    reject(f"Docs schema/owner mismatch: {location}")
                entries = docs.get("entries")
                if not isinstance(entries, list) or len(entries) > 256:
                    reject(f"Docs entries invalid: {location}")
                for idx, item in enumerate(entries):
                    if not isinstance(item, dict):
                        reject(f"Docs entry {idx} is not an object")
                    kind = text_field(item, "kind", 24, True).lower()
                    if kind not in KINDS:
                        reject(f"Unsupported docs kind: {kind}")
                    text_field(item, "name", 100, True)
                    text_field(item, "syntax", 250)
                    text_field(item, "category", 80)
                    text_field(item, "description", 2048, True)
                    text_field(item, "details", 8192)
                    text_field(item, "example", 8192)
                total_docs += len(entries)
            corrupt = archive.testzip()
            if corrupt:
                reject(f"Corrupt ZIP/JAR entry: {corrupt}")
    except (OSError, zipfile.BadZipFile, KeyError) as error:
        reject(f"Cannot read JAR: {error}")
    return {"id": ident, "name": name, "version": version, "apiVersion": api,
            "docs": total_docs, "required_modules": deps["modules"], "optional_modules": deps["optionalModules"]}


def verify_set(paths: list[Path]) -> None:
    seen = {}
    for path in paths:
        data = verify(path)
        if data["id"] in seen:
            reject(f"Duplicate module id {data['id']} in {path} and {seen[data['id']]}")
        seen[data["id"]] = path
        print(f"PASS {path.name}: {data['id']} v{data['version']} API v{data['apiVersion']}; {data['docs']} docs")
    if len(paths) > 1:
        print("Note: checking JAR presence only; version predicates and Fabric dependencies require the running Fabric Loader.")
        for path in paths:
            data = verify(path)
            for dependency in data["required_modules"]:
                if dependency not in seen:
                    reject(f"{data['id']} requires missing module {dependency}")
    print(f"PASS: {len(paths)} module JAR(s) structurally valid. Runtime compatibility NOT verified.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jars", nargs="+", type=Path, help="module JARs, not the HzkMacros mod or API JAR")
    args = parser.parse_args(argv)
    try:
        verify_set(args.jars)
    except ModuleError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
