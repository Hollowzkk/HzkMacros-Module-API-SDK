# Compatibilidade da Module API

A versão da Module API é separada da versão do HzkMacros.

## Evolução

- **API v1:** Actions, Invocation, Result.
- **API v2:** Variables, Iterators, Events, typed `ModuleValue`.
- **API v3:** descriptors, logger, storage, services, message bus, dependencies, `onUnload()`.
- **API v4:** version predicates, dependency resource visibility, `findModule()`/`loadedModules()`, scheduler.

A evolução até v4 foi aditiva: métodos novos de `ModuleContext` têm implementações default para preservar binários compilados contra APIs anteriores quando o host suporta aquela versão.

## O que declarar

No manifesto:

```json
"apiVersion": 4,
"hzkmacrosVersion": ">=0.26.0-beta.94"
```

Declare a menor API que seu módulo realmente exige. Se usar scheduler/introspecção v4, declare `4`.

## Minecraft/Fabric

Compatibilidade da Module API não garante automaticamente compatibilidade do seu código com todas as versões de Minecraft.

Se o módulo usa apenas a API pública do HzkMacros, ele tende a depender menos da versão do jogo. Se importa classes do Minecraft/Fabric, o autor precisa compilar/testar para os targets correspondentes.

Quando o HzkMacros ganhar builds multiversão, o autor do módulo deve declarar e testar quais variantes suporta.
