# First Module — passo a passo

Este guia cria o módulo mais simples possível para **HzkMacros Module API v4**.

## 1. Copie o exemplo

Use `examples/first-module/` como template. Ele já contém:

```text
first-module/
├── gradlew
├── gradlew.bat
├── gradle/wrapper/
├── build.gradle
├── settings.gradle
├── libs/
│   └── hzkmacros-module-api-4.0.jar
└── src/main/
    ├── java/com/example/firstmodule/FirstModule.java
    └── resources/
        ├── hzkmacros.module.json
        └── docs/
            ├── en_us.json
            └── pt_br.json
```

Você só precisa de **Java 21**. O Gradle Wrapper baixa a versão correta do Gradle na primeira execução.

## 2. A dependência pública é `compileOnly`

```groovy
dependencies {
    compileOnly files('libs/hzkmacros-module-api-4.0.jar')
}
```

Nunca use `implementation` para a API se isso fizer as classes `dev.hzk.hzkmacros.api.module.*` entrarem no JAR final.

## 3. Entry point

```java
package com.example.firstmodule;

import dev.hzk.hzkmacros.api.module.HzkModule;
import dev.hzk.hzkmacros.api.module.ModuleContext;
import dev.hzk.hzkmacros.api.module.ModuleResult;
import dev.hzk.hzkmacros.api.module.ModuleValue;

public final class FirstModule implements HzkModule {
    @Override
    public void onLoad(ModuleContext context) {
        context.logger().info("First Module loaded!");

        context.registerVariable(
            "&first_module_status",
            () -> ModuleValue.string("ready")
        );

        context.registerAction("HELLO", invocation -> {
            String name = invocation.argument(0, "player");
            invocation.log("Hello, " + name + "!");
            return ModuleResult.done();
        });
    }
}
```

Isso registra:

```text
HELLO("Steve");
```

E a variável:

```text
&first_module_status
```

## 4. Manifesto

Todo módulo precisa de `src/main/resources/hzkmacros.module.json`:

```json
{
  "schemaVersion": 1,
  "id": "first_module",
  "name": "First Module",
  "version": "1.0.0",
  "author": "YourName",
  "apiVersion": 4,
  "hzkmacrosVersion": ">=0.26.0-beta.94",
  "entrypoint": "com.example.firstmodule.FirstModule",
  "documentation": {
    "en_us": "docs/en_us.json",
    "pt_br": "docs/pt_br.json"
  },
  "dependencies": {
    "fabricMods": [],
    "optionalFabricMods": [],
    "modules": [],
    "optionalModules": []
  }
}
```

Mantenha o `id` estável depois de publicar o módulo.

## 5. Compile

Windows:

```bat
gradlew.bat clean build
```

Linux/macOS:

```bash
chmod +x gradlew   # only needed once if your checkout lost the executable bit
./gradlew clean build
```

Resultado:

```text
build/libs/first-module-1.0.0.jar
```

## 6. Verifique

A partir da raiz deste SDK:

```bash
python tools/verify_module.py examples/first-module/build/libs/first-module-1.0.0.jar
```

Python 3 é opcional; o verificador só checa estrutura e metadados.

## 7. Instale e teste

Copie o JAR para:

```text
.minecraft/config/hzkmacros/modules/
```

Reinicie o Minecraft. Abra **HzkMacros → Modules** e confirme que `First Module` está carregado.

Macro de teste:

```text
$${
    HELLO("Steve");
    LOG(%&first_module_status%);
}$$
```

## 8. Personalize

Antes de publicar, altere:

- `group` e nome do projeto;
- package Java;
- classe de entrypoint;
- `id`, `name`, `version`, `author`;
- Actions/Variables do exemplo;
- documentação integrada.

Depois avance para `examples/advanced-module/`.
