# HzkMacros — Third-Party Module Author Policy

This policy explains the intended relationship between HzkMacros and independently developed third-party modules. It does not open-source or license the proprietary HzkMacros core.

## Your module is yours

A third-party developer keeps ownership of the code and original content they create for their module, subject to any third-party licenses they use.

The author decides whether the module is:

- free or paid;
- open-source or closed-source;
- public or private;
- distributed under any license/business model chosen by the author.

HzkMacros does not claim ownership of an independently developed module merely because it uses the public Module API.

## Your responsibility

The module author/distributor is responsible for the module's behavior, security, dependencies, licensing, support, data handling, purchases, compatibility and compliance with applicable rules/laws.

Third-party modules are Java code executed in the Minecraft client process. They are **not sandboxed** by HzkMacros. Users should install modules only from sources they trust.

## HzkMacros core remains proprietary

Using the public Module API does not grant permission to copy, modify, repackage or redistribute proprietary HzkMacros core code except where separately permitted by the HzkMacros license or applicable law.

A module must not bundle the HzkMacros core or private/internal implementation classes.

## Public Module API / SDK

The public API binary, public API source/Javadocs, schemas, documentation, verifier and official examples exist to let developers create independent software interoperable with HzkMacros.

The API JAR must be used as `compileOnly` and must not be bundled into the final module JAR.

## Name and affiliation

Authors may use compatibility wording such as:

```text
MyModule for HzkMacros
Compatible with HzkMacros
HzkMacros Module
```

A third-party module must not claim to be official, endorsed or maintained by HzkMacros unless that authorization was actually given.

## Compatibility

Module API versions are versioned contracts. Authors are responsible for declaring and testing the HzkMacros, Minecraft, Fabric and dependency versions they support.

HzkMacros is not responsible for third-party module availability, support, purchases or damage caused by third-party code.
