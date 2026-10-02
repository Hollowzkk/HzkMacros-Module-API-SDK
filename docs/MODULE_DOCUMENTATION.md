# Documentação integrada do módulo

Docs são opcionais, mas recomendadas. Quando declaradas no manifesto, aparecem em **Help → Module Docs**.

Exemplo `docs/pt_br.json`:

```json
{
  "schemaVersion": 1,
  "moduleId": "inventory_tools",
  "language": "pt_br",
  "entries": [
    {
      "kind": "action",
      "name": "INVCOUNT",
      "syntax": "INVCOUNT(<item>,#count);",
      "category": "Inventory Tools",
      "description": "Conta o item e grava o total.",
      "details": "Descrição longa opcional.",
      "example": "INVCOUNT(\"minecraft:diamond\",#total);"
    }
  ]
}
```

Kinds suportados:

```text
action
variable
event
iterator
service
feature
guide
```

Campos por entry:

- `kind` — obrigatório;
- `name` — obrigatório;
- `syntax` — recomendado quando aplicável;
- `category` — opcional;
- `description` — obrigatório;
- `details` — opcional;
- `example` — opcional.

Use `schema/hzkmacros-docs.schema.json` para validação.

Para Actions, mostre a sintaxe completa incluindo `;`, por exemplo:

```text
HELLO("Steve");
```
