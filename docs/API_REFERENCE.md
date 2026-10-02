# Module API v4 — referência pública

Package público:

```text
dev.hzk.hzkmacros.api.module
```

A referência HTML gerada também está em `docs/javadoc/index.html` e `api/hzkmacros-module-api-4.0-javadoc.jar`.

## `HzkModule`

```java
void onLoad(ModuleContext context) throws Exception;
default void onUnload() throws Exception;
```

Entry point principal do módulo.

## `ModuleContext`

```java
String moduleId();
void registerAction(String name, ModuleAction action);
void registerVariable(String name, ModuleVariable provider);
void registerIterator(String name, ModuleIterator provider);
ModuleEvent registerEvent(String name);
ModuleDescriptor descriptor();
ModuleLogger logger();
ModuleServices services();
ModuleMessageBus messages();
Path dataDirectory();
boolean isModuleLoaded(String id);
Optional<ModuleDescriptor> findModule(String id);
List<ModuleDescriptor> loadedModules();
ModuleScheduler scheduler();
```

Registration methods devem ser usados durante `onLoad()`.

## `ModuleAction`

```java
ModuleResult execute(ModuleInvocation invocation) throws Exception;
```

## `ModuleInvocation`

```java
String moduleId();
List<String> arguments();
String argument(int index, String fallback);
void log(String message);
```

Os argumentos já chegam como snapshot expandido da macro.

## `ModuleResult`

```java
static ModuleResult done();
static ModuleResult waitTicks(long ticks);
long waitTicks();
```

`waitTicks` aceita 0..72.000.

## `ModuleValue`

```java
static ModuleValue string(String value);
static ModuleValue integer(int value);
static ModuleValue floatNumber(double value);
static ModuleValue bool(boolean value);
Type type();
Object value();
```

Tipos: `STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`. Floats precisam ser finitos.

## `ModuleVariable`

```java
ModuleValue read();
```

Provider de variável read-only.

## `ModuleIterator`

```java
List<Map<String, ModuleValue>> snapshot();
```

Retorna um snapshot de rows/fields para `FOREACH`.

## `ModuleEvent`

```java
void emit(Map<String, ModuleValue> variables);
default void emit();
```

O handle é obtido por `context.registerEvent(...)`.

## `ModuleScheduler`

```java
ModuleTask schedule(long delayTicks, Runnable task);
ModuleTask repeat(long initialDelayTicks, long intervalTicks, Runnable task);
long currentTick();
default ModuleTask execute(Runnable task);
```

Roda na client tick thread. Não use para I/O bloqueante.

## `ModuleTask`

```java
boolean active();
void cancel();
```

## `ModuleLogger`

```java
void info(String message);
void warn(String message);
void error(String message, Throwable error);
default void error(String message);
```

## `ModuleDescriptor`

```java
String id();
String name();
String version();
String author();
int apiVersion();
List<String> dependencies();
```

Metadados públicos imutáveis.

## `ModuleServices`

```java
void register(String name, Object service);
<T> Optional<T> find(String moduleId, String name, Class<T> type);
<T> T require(String moduleId, String name, Class<T> type);
```

Services não são serializados/proxyficados; são objetos Java compartilhados entre classloaders de módulos com dependência declarada.

## `ModuleMessageBus`

```java
ModuleSubscription subscribe(String qualifiedTopic, ModuleMessageListener listener);
void publish(String topic, Map<String, ModuleValue> values);
default void publish(String topic);
```

Publish usa tópico local; o host transforma em `<module_id>:<topic>`. Subscribe usa tópico totalmente qualificado.

## `ModuleMessage`

```java
String sourceModuleId();
String topic();
Map<String, ModuleValue> values();
```

## `ModuleMessageListener`

```java
void onMessage(ModuleMessage message) throws Exception;
```

Listeners são chamados sincronamente na thread da publicação. Não bloqueie.

## `ModuleSubscription`

```java
boolean active();
void close();
```

Também implementa `AutoCloseable`.
