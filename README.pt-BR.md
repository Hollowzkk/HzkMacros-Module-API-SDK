<p align="center">
  <a href="https://hzkmacros.com">
    <img src="assets/hzkmacros-icon.png" alt="HzkMacros" width="144">
  </a>
</p>

<h1 align="center">HzkMacros Module API & SDK</h1>

<p align="center">
  Crie extensões Java independentes para o <strong>HzkMacros</strong> sem acesso à source proprietária do core.
</p>

<p align="center">
  <a href="https://hzkmacros.com"><strong>hzkmacros.com</strong></a>
  · <a href="README.md">English</a>
  · <a href="docs/FIRST_MODULE.md">Primeiro módulo</a>
  · <a href="docs/API_REFERENCE.md">Referência da API</a>
  · <a href="docs/TESTING_AND_PUBLISHING.md">Publicação</a>
</p>

---

## O que um módulo pode adicionar?

Com a Module API pública, desenvolvedores podem criar extensões próprias para o HzkMacros, incluindo:

- **Actions** personalizadas para macros;
- **Variables** personalizadas;
- **Iterators** para `FOREACH`;
- **Events** próprios do módulo;
- tarefas agendadas por client ticks;
- armazenamento persistente do módulo;
- **Services** Java tipados compartilhados entre módulos;
- comunicação entre módulos através do Message Bus;
- integrações com Minecraft, Fabric, outros mods, ferramentas ou serviços externos.

> **O módulo é do autor.** O desenvolvedor decide se ele será gratuito ou pago, open-source ou closed-source, público ou privado, além da licença ou modelo de distribuição utilizado. O autor/distribuidor é responsável pelo módulo que publica.

## Alvo atual

| Componente | Alvo |
|---|---|
| HzkMacros | `0.26.0-beta.60+` |
| Module API | **v4** |
| Minecraft | **1.21.1** |
| Loader | **Fabric** |
| Java | **21** |

A Module API possui versionamento próprio para permitir que módulos de terceiros declarem compatibilidade de forma clara.

## Comece aqui

Se este é seu primeiro módulo para HzkMacros, abra [`docs/FIRST_MODULE.md`](docs/FIRST_MODULE.md) ou copie [`examples/first-module/`](examples/first-module/).

O First Module é intencionalmente pequeno e registra:

```text
HELLO("Steve");
```

e:

```text
&first_module_status
```

### Compilação

Não é necessário instalar Gradle globalmente. Todos os exemplos já incluem o Gradle Wrapper.

Windows:

```bat
gradlew.bat clean build
```

Linux/macOS:

```bash
chmod +x gradlew   # only needed once if your checkout lost the executable bit
./gradlew clean build
```

O JAR será gerado em `build/libs/`.

Instale em:

```text
.minecraft/config/hzkmacros/modules/
```

Depois reinicie o Minecraft e abra **HzkMacros → Modules**.

## Qual exemplo usar?

| Exemplo | Objetivo |
|---|---|
| [`examples/first-module/`](examples/first-module/) | Action + Variable mínimas; melhor ponto de partida |
| [`examples/advanced-module/`](examples/advanced-module/) | Iterator, Event, Scheduler, storage, logger e lifecycle |
| [`examples/provider-module/`](examples/provider-module/) | Expõe um Service Java tipado e publica mensagens |
| [`examples/consumer-module/`](examples/consumer-module/) | Declara outro módulo como dependência e consome service/messages |

Cada exemplo é autocontido e utiliza o JAR público da Module API como `compileOnly`.

## Conteúdo público do SDK

```text
HzkMacros-Module-API-SDK/
├── assets/                 Identidade visual pública usada no repositório
├── api/                    Binário público da API, sources e Javadocs
├── docs/                   Guias e referência da API
├── examples/               Exemplos compiláveis
├── schema/                 Schemas JSON de manifesto e documentação
├── tools/                  Verificador offline + testes
├── LICENSE                 Licença do SDK/API/exemplos públicos
├── MODULE_AUTHOR_POLICY.md Política de autoria/responsabilidade dos módulos
└── README.md
```

O SDK inclui:

- `api/hzkmacros-module-api-4.0.jar` — binário `compileOnly`;
- `api/hzkmacros-module-api-4.0-sources.jar` — source somente da API pública para navegação na IDE;
- `api/hzkmacros-module-api-4.0-javadoc.jar` e `docs/javadoc/` — Javadocs da API pública;
- `schema/` — schemas JSON;
- `tools/verify_module.py` — verificador estrutural offline;
- exemplos completos First / Advanced / Provider / Consumer.

**Nenhuma implementação/source proprietária do core do HzkMacros é incluída.**

## Regra importante de empacotamento

Use a Module API como **`compileOnly`**.

Não inclua, faça shade ou relocação de:

```text
dev/hzk/hzkmacros/api/module/*
```

no JAR final do seu módulo. O HzkMacros fornece essas classes em runtime.

## Verifique antes de publicar

Python 3 é opcional e necessário apenas para o verificador standalone:

```bash
python tools/verify_module.py caminho/para/seu-modulo.jar
```

Para módulos relacionados:

```bash
python tools/verify_module.py provider.jar consumer.jar
```

O verificador checa empacotamento, manifesto, documentação, dependências e erros comuns do SDK. Ele **não substitui** testes dentro do Minecraft usando a versão real do HzkMacros.

## Documentação

- [`FIRST_MODULE.md`](docs/FIRST_MODULE.md) — crie seu primeiro módulo
- [`MODULE_API_OVERVIEW.md`](docs/MODULE_API_OVERVIEW.md) — conceitos e recursos
- [`API_REFERENCE.md`](docs/API_REFERENCE.md) — classes e métodos públicos
- [`MODULE_MANIFEST.md`](docs/MODULE_MANIFEST.md) — `hzkmacros.module.json`
- [`MODULE_DOCUMENTATION.md`](docs/MODULE_DOCUMENTATION.md) — documentação integrada ao Help
- [`DEPENDENCIES.md`](docs/DEPENDENCIES.md) — dependências, Services e mensagens
- [`API_COMPATIBILITY.md`](docs/API_COMPATIBILITY.md) — versionamento e compatibilidade
- [`FABRIC_INTEGRATION.md`](docs/FABRIC_INTEGRATION.md) — acesso direto a Minecraft/Fabric e limitações
- [`TESTING_AND_PUBLISHING.md`](docs/TESTING_AND_PUBLISHING.md) — checklist de testes/publicação
- [`Javadocs`](docs/javadoc/index.html) — documentação Java pública gerada

## Autoria dos módulos

Autores de módulos de terceiros mantêm a propriedade do código e conteúdo original que criarem. O autor decide se o módulo será gratuito, pago, open-source, closed-source, público ou privado, respeitando as licenças de eventuais dependências de terceiros.

O core do HzkMacros continua proprietário. O uso deste SDK não concede permissão para copiar, modificar, reempacotar ou redistribuir o core proprietário ou classes privadas de implementação.

Consulte [`MODULE_AUTHOR_POLICY.md`](MODULE_AUTHOR_POLICY.md).

## Projeto

**Site do HzkMacros:** [https://hzkmacros.com](https://hzkmacros.com)

Este repositório é o SDK público oficial para desenvolvimento de módulos de terceiros para o HzkMacros.
