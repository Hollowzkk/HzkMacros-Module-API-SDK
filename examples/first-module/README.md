# First Module

Minimal HzkMacros Module API v4 template.

Project website: https://hzkmacros.com

## Build

Windows:

```bat
gradlew.bat clean build
```

Linux/macOS:

```bash
chmod +x gradlew   # only needed once if your checkout lost the executable bit
./gradlew clean build
```

Install `build/libs/first-module-1.0.0.jar` into:

```text
.minecraft/config/hzkmacros/modules/
```

Restart Minecraft and try:

```text
HELLO("Steve");
```

The example also exposes:

```text
&first_module_status
```

Read `../../docs/FIRST_MODULE.md` for the step-by-step guide.
