# HzkMacros — Offline Module JAR verifier

Requires Python 3, standard library only. It is **optional**; the HzkMacros build and the Java SDK do not require Python.

```sh
python3 verify_module.py path/to/my-module.jar
python3 verify_module.py path/to/provider.jar path/to/consumer.jar
python3 -m unittest discover -s . -p 'test_*.py'
```

The verifier checks manifest/API version/id, compiled entrypoint presence, declared JSON docs, ZIP integrity/limits, duplicated SDK classes, dependencies declared in a coherent format and (when several JARs are passed) duplicate module IDs and missing required module JARs. It cannot validate Fabric version predicate semantics, Minecraft intermediary remapping, runtime registration, safe Java behavior or Mixins. The final compiled JAR must still be tested in Minecraft 1.21.1 with the HzkMacros release JAR.
