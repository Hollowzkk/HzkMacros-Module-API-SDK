# Module API v4 — visão geral

A Module API é uma superfície pública Java para extensões independentes do HzkMacros.

## Lifecycle

```java
public final class MyModule implements HzkModule {
    @Override
    public void onLoad(ModuleContext context) throws Exception {
        // registrar capacidades e inicializar
    }

    @Override
    public void onUnload() throws Exception {
        // cleanup best-effort
    }
}
```

`onLoad()` ocorre durante a inicialização client-side. `MinecraftClient.player` e `world` podem ainda não existir. Não assuma que o jogador já entrou em um mundo.

## Actions

```java
context.registerAction("MYACTION", invocation -> {
    invocation.log(invocation.argument(0, "default"));
    return ModuleResult.done();
});
```

A macro usa:

```text
MYACTION("hello");
```

Para esperar de forma cooperativa:

```java
return ModuleResult.waitTicks(20);
```

O wait continua na **próxima statement**. O limite público é 72.000 ticks.

## Variables

```java
context.registerVariable(
    "&my_module_status",
    () -> ModuleValue.string("ready")
);
```

Tipos suportados:

```java
ModuleValue.string("text");
ModuleValue.integer(10);
ModuleValue.floatNumber(1.5);
ModuleValue.bool(true);
```

## Iterators

```java
context.registerIterator("my_module_rows", () -> List.of(
    Map.of("NAME", ModuleValue.string("A")),
    Map.of("NAME", ModuleValue.string("B"))
));
```

Uso:

```text
FOREACH(my_module_rows);
    LOG(%NAME%);
NEXT;
```

## Module Events

```java
ModuleEvent changed = context.registerEvent("my_module_changed");
```

Depois do `onLoad()`:

```java
changed.emit(Map.of(
    "MESSAGE", ModuleValue.string("changed")
));
```

Macro:

```text
WAITEVENT(my_module_changed,100);
```

## Scheduler

```java
ModuleTask once = context.scheduler().schedule(20, () ->
    context.logger().info("one second later")
);

ModuleTask repeating = context.scheduler().repeat(20, 100, () ->
    context.logger().info("periodic")
);
```

Callbacks rodam na client tick thread e **não devem bloquear**. `delayTicks=0` executa no próximo tick. Intervalos repetidos precisam ser >= 1 tick. O host limita tarefas agendadas por módulo e cancela tarefas automaticamente quando o módulo é encerrado.

## Logger e storage

```java
context.logger().info("loaded");
Path data = context.dataDirectory();
```

O diretório é persistente e exclusivo do ID do módulo, normalmente:

```text
config/hzkmacros/module-data/<module_id>/
```

## Services

Para integração Java tipada entre módulos:

```java
context.services().register("greeting", serviceObject);
```

Consumidor:

```java
GreetingService service = context.services().require(
    "provider_module",
    "greeting",
    GreetingService.class
);
```

O consumidor deve declarar o provedor em `dependencies.modules` e compilar contra o JAR do provedor como `compileOnly`.

## Message Bus

Publicação:

```java
context.messages().publish(
    "status.changed",
    Map.of("STATUS", ModuleValue.string("ready"))
);
```

O tópico vira `module_id:status.changed`.

Assinatura:

```java
ModuleSubscription sub = context.messages().subscribe(
    "provider_module:status.changed",
    message -> context.logger().info(message.values().toString())
);
```

Use Services para integrações ricas; Message Bus para notificações leves.

## Introspecção

```java
context.findModule("shared_tools").ifPresent(module ->
    context.logger().info(module.name() + " " + module.version())
);

List<ModuleDescriptor> snapshot = context.loadedModules();
```

## Minecraft/Fabric

A Module API não tenta encapsular toda a API do Minecraft. Um módulo pode acessar Minecraft/Fabric diretamente quando compilado/remapeado corretamente. Porém, JARs carregados pela pasta `modules/` são descobertos tarde demais para registrar Mixins/access wideners. Para isso, use um mod Fabric normal + um módulo HzkMacros como integração.

## Segurança

Módulos são código JVM confiável no mesmo processo do Minecraft. **Não existe sandbox de segurança.**
