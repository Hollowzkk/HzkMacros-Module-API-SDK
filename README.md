<p align="center">
  <a href="https://hzkmacros.com">
    <img src="assets/hzkmacros-icon.png" alt="HzkMacros" width="144">
  </a>
</p>

<h1 align="center">HzkMacros Module API & SDK</h1>

<p align="center">
  Build independent Java extensions for <strong>HzkMacros</strong> without access to the proprietary HzkMacros core source.
</p>

<p align="center">
  <a href="https://hzkmacros.com"><strong>hzkmacros.com</strong></a>
  · <a href="README.pt-BR.md">Português (Brasil)</a>
  · <a href="docs/FIRST_MODULE.md">First Module</a>
  · <a href="docs/API_REFERENCE.md">API Reference</a>
  · <a href="docs/TESTING_AND_PUBLISHING.md">Publishing Guide</a>
</p>

---

## What can a module add?

With the public Module API, developers can create their own extensions for HzkMacros, including:

- custom macro **Actions**;
- custom **Variables**;
- custom `FOREACH` **Iterators**;
- custom module **Events**;
- scheduled tasks based on client ticks;
- persistent module storage;
- typed Java **Services** shared between modules;
- cross-module messages through the Message Bus;
- integrations with Minecraft, Fabric, other mods, external tools or services.

> **Your module is yours.** You decide whether it is free or paid, open-source or closed-source, public or private, and which license or business model you use. You are responsible for the module you publish and distribute.

## Current target

| Component | Target |
|---|---|
| HzkMacros | `0.26.0-beta.94+` |
| Module API | **v4** |
| Minecraft | **1.21.1** |
| Loader | **Fabric** |
| Java | **21** |

The Module API is versioned independently from HzkMacros so third-party modules can declare a clear compatibility contract.

> **API v4 is frozen for the beta.94 host target.** Breaking changes require a future major API version.

## Start here

If this is your first HzkMacros module, open [`docs/FIRST_MODULE.md`](docs/FIRST_MODULE.md) or copy [`examples/first-module/`](examples/first-module/).

The First Module is intentionally small. It registers:

```text
HELLO("Steve");
```

and:

```text
&first_module_status
```

### Build

No system-wide Gradle installation is required. Every example includes the Gradle Wrapper.

Windows:

```bat
gradlew.bat clean build
```

Linux/macOS:

```bash
chmod +x gradlew   # only needed once if your checkout lost the executable bit
./gradlew clean build
```

The resulting module JAR will be under `build/libs/`.

Install it in:

```text
.minecraft/config/hzkmacros/modules/
```

Then restart Minecraft and open **HzkMacros → Modules**.

## Which example should I use?

| Example | Purpose |
|---|---|
| [`examples/first-module/`](examples/first-module/) | Minimal Action + Variable; recommended starting point |
| [`examples/advanced-module/`](examples/advanced-module/) | Iterator, Event, Scheduler, storage, logger and lifecycle |
| [`examples/provider-module/`](examples/provider-module/) | Exposes a typed Java service and publishes messages |
| [`examples/consumer-module/`](examples/consumer-module/) | Declares another module as a dependency and consumes its service/messages |

Each example is self-contained and uses the public HzkMacros Module API JAR as `compileOnly`.

## Public SDK contents

```text
HzkMacros-Module-API-SDK/
├── assets/                 HzkMacros public branding used by this repository
├── api/                    Public Module API binary, sources and Javadocs
├── docs/                   Guides and API reference
├── examples/               Buildable example modules
├── schema/                 JSON schemas for manifests and module docs
├── tools/                  Offline module verifier + tests
├── LICENSE                 License for this public SDK/API/example material
├── MODULE_AUTHOR_POLICY.md Third-party module ownership/responsibility policy
└── README.md
```

The SDK includes:

- `api/hzkmacros-module-api-4.0.jar` — compile-only API binary;
- `api/hzkmacros-module-api-4.0-sources.jar` — public API sources for IDE navigation;
- `api/hzkmacros-module-api-4.0-javadoc.jar` and `docs/javadoc/` — public API Javadocs;
- `schema/` — manifest and module documentation JSON schemas;
- `tools/verify_module.py` — offline structural verifier;
- complete First / Advanced / Provider / Consumer examples.

**No HzkMacros proprietary core implementation source is included.**

## Important packaging rule

Use the HzkMacros Module API as **`compileOnly`**.

Do not shade, relocate or bundle:

```text
dev/hzk/hzkmacros/api/module/*
```

inside your final module JAR. HzkMacros provides those classes at runtime.

## Verify before publishing

Python 3 is optional and only required for the standalone verifier:

```bash
python tools/verify_module.py path/to/your-module.jar
```

For modules that depend on one another, pass the related JARs together:

```bash
python tools/verify_module.py provider.jar consumer.jar
```

The verifier checks packaging, manifest metadata, documentation, dependencies and common SDK mistakes. It does **not** replace testing inside Minecraft with the real HzkMacros release.

## Documentation

- [`FIRST_MODULE.md`](docs/FIRST_MODULE.md) — create your first module
- [`MODULE_API_OVERVIEW.md`](docs/MODULE_API_OVERVIEW.md) — capabilities and concepts
- [`API_REFERENCE.md`](docs/API_REFERENCE.md) — public classes and methods
- [`MODULE_MANIFEST.md`](docs/MODULE_MANIFEST.md) — `hzkmacros.module.json`
- [`MODULE_DOCUMENTATION.md`](docs/MODULE_DOCUMENTATION.md) — integrated Help documentation
- [`DEPENDENCIES.md`](docs/DEPENDENCIES.md) — module/Fabric dependencies, services and messages
- [`API_COMPATIBILITY.md`](docs/API_COMPATIBILITY.md) — API versioning and compatibility
- [`FABRIC_INTEGRATION.md`](docs/FABRIC_INTEGRATION.md) — direct Minecraft/Fabric access and limitations
- [`TESTING_AND_PUBLISHING.md`](docs/TESTING_AND_PUBLISHING.md) — testing and release checklist
- [`Javadocs`](docs/javadoc/index.html) — generated public Java API documentation

## Module ownership

Third-party module authors retain ownership of the original modules they create. Authors choose whether their module is free, paid, open-source, closed-source, public or private, subject to licenses of any third-party code they use.

The HzkMacros core remains proprietary. Using this SDK does not grant permission to copy, modify, repackage or redistribute the proprietary core or private implementation classes.

See [`MODULE_AUTHOR_POLICY.md`](MODULE_AUTHOR_POLICY.md) for the public module policy.

## Project

**HzkMacros website:** [https://hzkmacros.com](https://hzkmacros.com)

This repository is the public developer SDK for building third-party HzkMacros modules.
