# Dependências, Services e Message Bus

## Dependência entre módulos

Provider:

```json
{
  "id": "provider_module",
  "version": "1.0.0"
}
```

Consumer:

```json
"dependencies": {
  "modules": [
    { "id": "provider_module", "version": ">=1.0.0" }
  ]
}
```

Dependências obrigatórias são carregadas antes do consumidor. Ciclos obrigatórios são rejeitados. Se uma dependência obrigatória estiver ausente/desabilitada/incompatível/falhar, o consumidor não inicia.

Na API v3+, classes públicas da dependência declarada ficam visíveis ao consumidor. Na API v4, recursos também podem ficar visíveis.

## Como compartilhar uma API Java

O provider declara uma interface própria:

```java
package com.example.provider.api;

public interface GreetingService {
    String greet(String name);
}
```

E registra:

```java
context.services().register("greeting", service);
```

O consumer compila contra o JAR do provider como **`compileOnly`**:

```groovy
dependencies {
    compileOnly files('libs/hzkmacros-module-api-4.0.jar')
    compileOnly files('libs/hello-provider-1.0.0.jar')
}
```

Em runtime:

```java
GreetingService service = context.services().require(
    "hello_provider",
    "greeting",
    GreetingService.class
);
```

Não empacote o provider dentro do consumer.

## Services vs Message Bus

Use **Services** para contratos Java tipados e chamadas ricas.

Use **Message Bus** para eventos/notificações leves:

```java
context.messages().publish(
    "used",
    Map.of("MESSAGE", ModuleValue.string("hello"))
);
```

Consumer:

```java
context.messages().subscribe(
    "hello_provider:used",
    message -> context.logger().info(message.values().toString())
);
```

O listener é síncrono; mantenha-o curto.

Veja `examples/provider-module/` e `examples/consumer-module/`.
