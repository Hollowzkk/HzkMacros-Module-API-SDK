# Manifesto `hzkmacros.module.json`

Todo módulo precisa de um manifesto na raiz do JAR.

```json
{
  "schemaVersion": 1,
  "id": "inventory_tools",
  "name": "Inventory Tools",
  "version": "1.4.0",
  "author": "ExampleDeveloper",
  "apiVersion": 4,
  "hzkmacrosVersion": ">=0.26.0-beta.60",
  "entrypoint": "com.example.inventory.InventoryToolsModule",
  "documentation": {
    "en_us": "docs/en_us.json",
    "pt_br": "docs/pt_br.json"
  },
  "dependencies": {
    "fabricMods": [
      { "id": "fabric-api", "version": ">=0.116.0" }
    ],
    "optionalFabricMods": [],
    "modules": [
      { "id": "shared_tools", "version": ">=2.0.0" }
    ],
    "optionalModules": ["map_bridge"]
  }
}
```

## Campos

- `schemaVersion`: quando presente, deve ser `1`.
- `id`: obrigatório; regex `^[a-z][a-z0-9_]{2,63}$`. Não altere depois de publicar.
- `name`: obrigatório; nome exibido ao usuário.
- `version`: obrigatório; versão do módulo.
- `author`: recomendado.
- `apiVersion`: obrigatório; APIs 1..4 são reconhecidas pelo host atual.
- `hzkmacrosVersion`: opcional; predicado de versão no formato aceito pelo Fabric Loader.
- `entrypoint`: obrigatório; classe que implementa `HzkModule`.
- `documentation`: opcional; docs integradas `en_us`/`pt_br`.
- `dependencies`: opcional; dependências Fabric e de módulos.

## Dependências

Aceitam formato simples:

```json
"modules": ["shared_tools"]
```

ou com predicado:

```json
"modules": [
  { "id": "shared_tools", "version": ">=2.0.0" }
]
```

Listas:

- `fabricMods`: obrigatórias;
- `optionalFabricMods`: opcionais;
- `modules`: módulos HzkMacros obrigatórios;
- `optionalModules`: módulos HzkMacros opcionais.

Use `schema/hzkmacros-module.schema.json` na IDE para validação.
