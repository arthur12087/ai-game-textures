---
name: ai-game-textures
description: Criar, processar e validar texturas de jogos com foco em GPT Images, materiais PBR, seamless tiling, trim sheets, decals e integração em Godot ou Unreal. Use quando o pedido envolver gerar texturas com IA, comparar métodos de texturização ou transformar uma imagem de material em um asset pronto para jogo; não use para concept art comum sem intenção de material 3D.
---

# Texturas de jogo com IA

Produza materiais que sobrevivam à repetição, à iluminação do engine e à inspeção de perto e de longe. O fluxo principal desta skill segue o método do vídeo “This Is How to Make Game Textures With AI”: GPT Images pinta a base visual; um estágio de processamento transforma essa pintura em textura repetível e mapas PBR.

## Limite crucial

A ferramenta de preparação mostrada no vídeo é uma ferramenta própria do autor e não acompanha esta skill. Não diga que GPT Images entrega automaticamente um material PBR pronto. Se não houver uma ferramenta de processamento disponível, entregue a pintura-base e o plano de pós-processamento, ou implemente o estágio pedido; rotule o resultado como `source`, `prepared` ou `game-ready` conforme o que foi realmente concluído.

## Escolha o método

Use GPT Images como padrão quando o usuário quer um visual específico, muitas variações ou materiais únicos. Considere as outras rotas quando elas forem mais adequadas:

- shader procedural: quando o padrão não pode repetir ou a memória de textura é o gargalo;
- Blender procedural + bake: quando o material é geométrico, limpo e fácil de descrever por nós;
- biblioteca PBR: quando velocidade e previsibilidade importam mais que exclusividade;
- GPT Images + processamento: quando direção artística, variedade e iteração rápida são prioritárias.

Leia [references/video-methods.md](references/video-methods.md) para a comparação completa e para não transformar medições específicas do vídeo em regras universais.

## Fluxo principal

1. Defina o material, a escala física, o estilo, o engine, o tipo de UV e os mapas necessários.
2. Gere a imagem-base com GPT Images. Use o gerador integrado por padrão; não mude para CLI/API sem pedido explícito. Para materiais distintos, faça uma chamada por asset. Para editar uma imagem local, inspecione-a antes.
3. Trate a imagem gerada como pintura de origem, não como textura final. Remova iluminação direcional, corrija perspectiva e normalize a escala.
4. Torne o material seamless com a técnica adequada à sua estrutura:
   - padrões com juntas: alinhe a grade e ajuste cada fileira nos intervalos entre elementos;
   - padrões sem juntas claras: sobreponha bordas e faça a transição onde as duas regiões são visualmente compatíveis.
5. Derive e revise base color, height, normal e roughness. Gere AO apenas se o pipeline realmente o usar.
6. Teste em grade 3×3 e 8×8, em uma esfera/rocha e no mesh real, sob luz rasante e neutra.
7. Corrija repetição distante com macrovariação. Use hex tiling somente em materiais que tolerem a quebra da continuidade; tijolos, telhas e paralelepípedos normalmente não toleram.
8. Configure mipmaps, filtragem, escala física e convenção do normal map no engine antes de avaliar o resultado.

Use `scripts/validate_texture.py` para gerar mosaicos 3×3/8×8, diferenças de borda e um relatório heurístico. O script ajuda a encontrar problemas; ele não substitui inspeção no engine.

Leia [references/gpt-images-workflow.md](references/gpt-images-workflow.md) para executar o fluxo em detalhe. Leia [references/prompt-recipes.md](references/prompt-recipes.md) quando precisar gerar materiais, variações, trim sheets, decals ou interiores falsos. Leia [references/pbr-integration.md](references/pbr-integration.md) para mapas, anti-tiling, triplanar, parallax e validação no engine.

## Regras de qualidade

- Não prometa que “seamless” no prompt garante bordas perfeitas; valide e processe.
- Não confunda base color com uma foto iluminada. O mapa de cor deve carregar material, não sombras de uma cena.
- Não derive roughness por simples dessaturação sem revisar a resposta física do material.
- Não trate height e normal como equivalentes: height representa relevo; normal representa a orientação local usada pela luz.
- Preserve a continuidade das juntas em materiais estruturados.
- Mantenha a escala física consistente entre materiais e informe a densidade pretendida, por exemplo 1 m por repetição.
- Registre prompt, seed/variante quando disponível, resolução, escala, pós-processamento e convenção normal OpenGL/DirectX.
- Apresente números de desempenho e memória como medições do projeto testado, não como garantia para outro hardware ou engine.

## Entrega

Use estes níveis sem inflar o estado do trabalho:

- `source`: imagem-base gerada e selecionada;
- `prepared`: iluminação/perspectiva corrigidas, bordas tratadas e mapas produzidos;
- `game-ready`: importado no engine, escala e canais configurados, repetição validada no mesh e custo medido.

Para cada material, entregue ou documente:

- imagem-base aprovada e prompt final;
- mapas finais com nomes e espaços de cor corretos;
- escala física e estratégia de UV/projeção;
- captura do teste de repetição e do mesh real;
- técnica anti-tiling usada e seu custo medido;
- limitações restantes, especialmente em bordas, juntas e visão rasante.
