# HzkMacros Module API SDK — Changelog

## SDK v4 / beta.94 host compatibility sync

- keeps the Module API v4 binary/source contract unchanged;
- updates the documented HzkMacros host floor and all official example manifests to `>=0.26.0-beta.94`;
- keeps Minecraft 1.21.1 / Fabric / Java 21 as the current public target;
- public SDK remains MIT; third-party modules remain owned/licensed by their respective authors.

## SDK v4 public kit

- Added self-contained Gradle Wrapper to all examples.
- Added public API sources and generated Javadocs.
- Added full API reference, manifest/dependency/docs guides and compatibility notes.
- Added minimal, advanced, provider and consumer examples.
- Added offline verifier tests and publishing checklist.
- Clarified third-party module ownership and responsibility.

## Module API v4

API evolution summary:

- **v1:** Actions, `ModuleInvocation`, `ModuleResult`.
- **v2:** Variables, Iterators, Events, `ModuleValue`.
- **v3:** module descriptors, logger, storage, services, message bus, module dependencies, `onUnload()`.
- **v4:** version predicates for module dependencies/HzkMacros, dependency resource visibility, module introspection, client-tick scheduler.
