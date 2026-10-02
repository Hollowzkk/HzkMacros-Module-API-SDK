# Checklist de teste e publicação

Antes de publicar um módulo:

1. Compile com Java 21 e a API como `compileOnly`.
2. Abra o JAR e confirme que `hzkmacros.module.json` está na raiz.
3. Confirme que `dev/hzk/hzkmacros/api/module/*` **não** foi empacotado.
4. Rode o verificador offline:

```bash
python tools/verify_module.py path/to/module.jar
```

5. Instale em `config/hzkmacros/modules/`.
6. Reinicie o Minecraft.
7. Confirme o estado em **HzkMacros → Modules**.
8. Teste cada Action/Variable/Iterator/Event exposto.
9. Teste dependências ausentes/incompatíveis quando aplicável.
10. Teste disable/restart e `onUnload()` quando aplicável.
11. Teste com o **JAR final** que será distribuído, não apenas pela IDE.

## Verificador

O verifier detecta problemas estruturais comuns, incluindo manifesto ausente/inválido, entrypoint ausente, docs inválidas, dependências duplicadas e API do HzkMacros empacotada indevidamente.

Ele **não verifica**:

- segurança do código Java;
- compatibilidade real com Fabric/Minecraft;
- lógica de predicados em runtime;
- comportamento da Action;
- remapeamento de classes;
- crashes causados por bibliotecas externas.

## Publicação

O autor decide licença, preço, source aberta/fechada e canal de distribuição do próprio módulo. Evite sugerir que o módulo é oficial/endorsed pelo HzkMacros sem autorização.
