# Métodos apresentados no vídeo

Fonte: [This Is How to Make Game Textures With AI](https://www.youtube.com/watch?v=_rMMP7GPgt4), duração aproximada de 10:08. Estas notas são uma síntese operacional; não são uma transcrição literal.

## Matriz de decisão

| Rota | Força principal | Custo/risco real | Melhor encaixe |
|---|---|---|---|
| Shader procedural | variação infinita e nenhuma imagem do material | mais ALU/amostras por frame; direção artística mais técnica | padrões matemáticos e superfícies que não podem repetir |
| Blender procedural + bake | resultado determinístico e mapas reproduzíveis | regularidade visual; tempo de autoria e bake | materiais limpos, geométricos e controláveis |
| Biblioteca PBR | rapidez e qualidade conhecida | pouca exclusividade; licença e escala precisam ser verificadas | protótipo e materiais secundários |
| GPT Images + preparação | direção artística e muitas variações | saída crua não é game-ready; exige tiling, mapas e validação | materiais autorais e iteração visual rápida |

## Fundamentos — 00:56–02:26

O autor separa o mesh do material e explica o conjunto de mapas: cor, normal, roughness e height. UV é a correspondência entre a superfície 3D e a imagem 2D. Em paredes, ele trabalha com escala métrica; UV ruim estica a textura. Para superfícies em que o unwrap não é confiável, apresenta projeção triplanar: três projeções ortogonais são combinadas conforme a orientação da superfície.

## Método 1: shader procedural — 02:31–03:11

Um shader constrói tijolos por código: fileiras, variação aleatória de cor, tijolos queimados, ruído, bordas lascadas e argamassa recuada cerca de 9 mm. Vantagens: não repete e não consome memória de imagens do material. Isso não significa “0 MB de VRAM” para a renderização inteira: shader, buffers e render targets continuam usando memória. Desvantagens: aparência inicialmente limpa/artificial e cálculo contínuo na GPU.

Use quando a ausência de repetição for essencial, a estrutura puder ser descrita matematicamente e o custo de shader for aceitável.

## Método 2: Blender procedural + bake — 03:11–03:24

O material é criado por nós, por exemplo com Brick Texture, e depois assado para imagens. É gratuito e controlável, mas no exemplo parece excessivamente regular e “feito por computador”. Use quando o material for limpo, geométrico ou precisar de mapas determinísticos.

## Método 3: biblioteca PBR — 03:24–03:39

O exemplo usa um material popular do Poly Haven. A qualidade é alta e o custo de aquisição é baixo, mas o asset é reconhecível e compartilhado por muitos projetos. Use para protótipos, preenchimento secundário ou quando prazo e previsibilidade forem mais importantes que exclusividade. Verifique sempre licença e atribuição na fonte atual.

## Método 4: GPT Images + preparação — 03:39–06:34

É o método preferido do autor. Ele mostra 12 materiais produzidos em conjunto: tijolo, reboco cinza, reboco ocre, paralelepípedo, placas, granito, asfalto, madeira, ferro, estanho, telhas e concreto com musgo. Depois mostra oito variações adicionais de tijolo.

A geração é somente o início. A ferramenta própria do autor — mostrada, mas não distribuída no vídeo — faz o seguinte:

1. uniformiza a iluminação para evitar faixas na repetição;
2. detecta juntas e as coloca em uma grade exata;
3. em tijolos, telhas e paralelepípedos, corta fileiras nos vãos e as estica levemente para casar as bordas;
4. em reboco e materiais sem juntas, sobrepõe as extremidades e corta onde ambas parecem semelhantes;
5. usa as juntas para construir height, normal e roughness;
6. gera texturas tileable para cada variação.

O vídeo não mostra um prompt literal para os 12 materiais ou para as oito variações. Também não demonstra que uma única resposta do GPT produziu arquivos finais separados; mostra o conjunto de resultados. Qualquer prompt nesta skill é uma reconstrução prática baseada no resultado e no processo, não uma citação do autor.

## Anti-repetição — 04:37–05:19

Três soluções são apresentadas:

1. ruído suave de grande escala para variar luminosidade/cor;
2. segunda cópia da textura em outra escala;
3. hex tiling, dividindo a superfície em células que amostram regiões aleatórias e se misturam.

Hex tiling remove bem a grade em materiais orgânicos, mas quebra juntas contínuas de tijolos e paralelepípedos. Para esses, o autor recomenda apenas a macrovariação suave.

## Mipmaps — 05:20–05:41

Sem versões reduzidas e filtradas, um pixel distante pode amostrar detalhes inconsistentes e causar cintilação. Godot e Unreal geram/usam mipmaps automaticamente, mas importação, compressão e filtragem ainda devem ser verificadas.

## Comparação e números — 05:41–06:34

No teste mostrado, os quatro métodos têm custo de frame parecido. O shader procedural não usa imagens; os demais usam mapas de textura. O vídeo cita aproximadamente 11 MB por parede e 165 MB para 14 materiais, mas também descreve quatro tipos de mapa e depois fala em três imagens por parede. Trate esse número como específico do empacotamento, formato e resolução usados pelo autor; não o reutilize sem medir o projeto real.

## Variação contextual do edifício — 06:34–08:07

Uma única textura limpa não basta. O autor adiciona:

- reboco quebrado em cantos e perto de janelas, guiado por uma máscara de arestas gerada no Blender;
- escurecimento na base, marcas de chuva e musgo em regiões molhadas;
- trim sheet criado com GPT para cornijas, blocos, faixas, peitoris, molduras, zinco, tijolo e granito;
- decals de chuva, ferrugem, umidade e rachaduras, colocados em locais plausíveis como sob peitoris, sob canos e junto ao chão.

## Truques de profundidade — 08:07–09:41

- interior mapping: uma imagem em perspectiva criada com GPT simula um cômodo atrás de vidro plano por interseção/projeção em uma caixa virtual; não é ray tracing físico da cena;
- parallax occlusion mapping: usa height para deslocar a amostragem e criar oclusão aparente;
- recorte de silhueta: a variação mostrada como “Crimson” descarta pixels onde o relevo virtual ultrapassaria a borda, deixando a silhueta irregular;
- geometria real: referência visual para comparação, mas com custo de triângulos muito maior no exemplo.

O vídeo cita cerca de 3,5 ms para hex tiling em Godot e quase zero no teste Unreal; para parallax, cerca de 0,5 ms em Godot e quase zero no teste Unreal com Nanite. São resultados locais, não benchmarks universais.

## Conclusão do autor — 09:41–10:08

Procedural é forte quando não pode haver repetição; Blender atende materiais simples e limpos; bibliotecas são rápidas, mas pouco exclusivas; GPT vence para o autor porque entrega exatamente a direção desejada e muitas variações rapidamente.
