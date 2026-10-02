# Integração direta com Minecraft / Fabric

A Module API fornece infraestrutura do HzkMacros, mas não encapsula toda a API do Minecraft.

Um módulo pode importar `MinecraftClient`, Fabric API ou APIs de outros mods se for compilado com Fabric Loom/mappings adequados para o target.

## Limitação importante

Módulos em:

```text
config/hzkmacros/modules/
```

são descobertos depois da fase inicial de carregamento do Fabric. Por isso, o módulo carregado pela Module API **não é o lugar correto para**:

- registrar Mixins;
- registrar Access Wideners;
- depender de entrypoints Fabric que precisem ser descobertos no bootstrap;
- alterar transformações de classes que já aconteceram.

Quando precisar disso, distribua duas partes:

```text
Seu Mod Fabric
+ Seu módulo HzkMacros
```

O mod Fabric faz integração de baixo nível; o módulo expõe Actions/Variables/Services para o HzkMacros.

## Threading

Minecraft possui operações que precisam ocorrer na client thread. O `ModuleScheduler` é útil para callbacks curtos no client tick. Não bloqueie a thread com rede, disco pesado ou loops longos.
