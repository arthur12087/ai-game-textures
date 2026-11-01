# PBR, anti-tiling e integração no engine

## UV e escala

Para arquitetura, use uma densidade física estável: por exemplo, um tile representa 1 m × 1 m. Se o material atravessa vários meshes, mantenha a mesma escala aparente. Faça unwrap para assets únicos; use world-aligned/triplanar em rochas e formas com UV ruim, aceitando o custo de múltiplas amostras e possíveis problemas de normal blending.

## Importação de mapas

`Base color` é o termo mais seguro no pipeline metálico/roughness. “Albedo” é usado informalmente como sinônimo, mas em alguns contextos técnicos significa refletância difusa e não inclui a cor especular de metais. Siga a nomenclatura do engine e documente o canal.

- base color: sRGB ligado;
- normal: tipo normal map, sem sRGB; confirme OpenGL vs DirectX;
- height, roughness, AO, metallic e máscaras: dados lineares, sRGB desligado;
- desative compressão destrutiva para height quando banding for visível;
- preserve padding e mip-safe borders em atlas/trim sheets.

No Godot, confirme a convenção normal do projeto/material. No Unreal, confira a opção Flip Green Channel quando a origem do normal estiver na convenção oposta.

## Macrovariação

Multiplique ou misture um ruído suave em world space com amplitude baixa. A frequência deve ser muito maior que o tile base: a variação atravessa vários metros e não deve parecer sujeira pintada em cada repetição.

Para tijolo e cobble, prefira macrovariação que preserve todas as juntas. Aplique-a sobretudo a cor/roughness; evite deslocar UVs de forma que quebre a argamassa.

## Segunda escala

Uma segunda amostra em escala diferente pode esconder periodicidade, mas aumenta custo e pode criar batimento visual. Use em materiais orgânicos e misture por máscara de baixa frequência. Não use em padrões arquitetônicos se as juntas divergirem.

## Hex tiling

Hex tiling ou stochastic tiling amostra células em offsets/rotações diferentes e mistura as bordas. Funciona bem em terra, reboco, concreto, musgo e ruído. Em tijolos, telhas, tábuas e paralelepípedos, rompe linhas estruturais; nesses casos, limite-se a macrovariação ou use um algoritmo consciente de fileiras/juntas.

Meça custo com o profiler do engine no hardware-alvo. Os números do vídeo são apenas uma referência do projeto mostrado.

## Mipmaps e cintilação

Ative mipmaps e filtragem anisotrópica onde necessário. Roughness/normal com detalhe fino demais podem cintilar mesmo com mipmaps; reduza contraste de microdetalhe ou use técnicas de normal/roughness filtering. Avalie em movimento, não só em captura estática.

## Máscara contextual de dano

Para reboco quebrado:

1. gere ou bake uma máscara de concavidade/arestas no DCC;
2. dê mais peso a cantos e bordas de janelas;
3. combine com ruído controlado;
4. revele o material de tijolo abaixo;
5. mantenha uma faixa de transição com argamassa/poeira, não um corte digital perfeito.

Para sujeira, use regras físicas: água desce; ferrugem nasce em metal; umidade acumula na base; pingos começam sob saliências; musgo prefere regiões persistentemente úmidas.

## Trim sheets

- alinhe cada peça longa a uma faixa horizontal;
- faça a faixa repetir no eixo longitudinal;
- mantenha padding suficiente entre faixas para os mipmaps;
- evite detalhes únicos próximos às bordas;
- documente a escala e a posição UV de cada faixa.

Um trim sheet reduz materiais e draw calls, mas só funciona se a modelagem e o UV layout forem planejados para ele.

## Decals

Use decals para variação localizada que não deve se repetir: chuva, ferrugem, umidade e rachaduras. Prefira atlas de decals com bordas transparentes e padding. Limite overdraw, especialmente em superfícies grandes e sobrepostas.

## Interior mapping

Uma textura em perspectiva pode simular um cômodo em uma caixa virtual atrás da janela. A geometria continua plana; o shader calcula uma interseção de raio analítica com planos da caixa e amostra a imagem. Isso é interior mapping/parallax, não ray tracing físico da cena. Produza várias variantes para evitar que todas as janelas revelem o mesmo cômodo.

## Parallax occlusion mapping

POM usa o height para procurar a interseção aparente ao longo da direção de visão. Oferece profundidade e auto-oclusão sem geometria real, mas custa múltiplas amostras, piora em ângulos rasantes, pode criar instabilidade e não altera a silhueta por padrão.

A variação de recorte de borda mostrada no vídeo descarta pixels quando o relevo virtual ultrapassaria a superfície, simulando silhueta irregular. Isso requer geometria/material apropriado, controle de sombras e cuidado com transparência/early-z. Compare com displacement ou geometria real no engine-alvo.

## Matriz mínima de testes

| Teste | Detecta |
|---|---|
| 3×3 sob luz neutra | emendas e diferenças de exposição |
| 8×8 à distância | grade, manchas repetidas e macrovariação insuficiente |
| luz rasante móvel | normal invertido, height exagerado, emendas de relevo |
| plano + esfera + rocha | dependência de UV e falha de projeção |
| câmera em movimento | shimmer, mipmaps e instabilidade de POM |
| profiler GPU | custo real de amostras, hex tiling e parallax |
| captura de memória | impacto de resolução, formato, canais e compressão |

## Critério de aprovação

Aprove somente quando:

- não há emenda perceptível em 3×3;
- não há grade evidente em 8×8 na distância de jogo;
- juntas permanecem contínuas;
- relevo responde corretamente à luz;
- escala do material é plausível;
- mapas usam os espaços de cor e canais corretos;
- custo e memória estão dentro do orçamento do projeto.
