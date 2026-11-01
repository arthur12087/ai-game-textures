# Fluxo completo com GPT Images

## Estados de conclusão

- `source`: geração selecionada, ainda sem garantia de tiling ou mapas corretos;
- `prepared`: imagem equalizada, seamless verificado e mapas derivados/revisados;
- `game-ready`: material importado no engine, canais e escala configurados, testado no mesh real e medido no hardware-alvo.

Não chame um asset de `game-ready` só porque o prompt contém “seamless” ou “PBR”.

## 1. Especificação do material

Antes de gerar, registre:

- material e variação: tijolo antigo, reboco úmido, telha esmaltada etc.;
- uso: parede, piso, teto, trim, decal ou interior falso;
- escala física: tamanho real do tile e dimensão média dos elementos;
- estilo: realista, estilizado, época, região e estado de conservação;
- estrutura: grade rígida, fileiras deslocadas, padrão orgânico ou ruído;
- mapas esperados: base color, height, normal, roughness e, se necessário, AO/metallic;
- engine e convenção de normal: Godot geralmente OpenGL; Unreal normalmente DirectX;
- resolução-alvo e orçamento de memória.

## 2. Geração da pintura-base

Use o gerador integrado de imagens por padrão. Para materiais diferentes, faça uma geração por asset; um painel com muitos materiais serve como concept sheet, mas não substitui arquivos individuais de produção.

O prompt deve pedir uma amostra ortográfica/frontal, uniforme e sem iluminação de cena. “Seamless” ajuda a intenção, mas não elimina o pós-processamento.

Estrutura recomendada:

```text
Use case: stylized-concept
Asset type: tileable game texture source
Primary request: <material, região/época, estado e variação>
Subject: a single continuous material surface filling the entire square frame
Style/medium: <realistic or stylized> PBR material reference, front-facing orthographic capture
Composition/framing: square crop, edge-to-edge, consistent physical scale, no perspective, no horizon
Lighting/mood: neutral diffuse illumination, even exposure across the frame, no directional shadow, no baked highlights
Materials/textures: <cor, tamanho, juntas, desgaste, microdetalhe>
Constraints: tile-friendly structure; no obvious focal feature; no objects; no borders; no labels; no logos; no watermark
Avoid: perspective convergence, vignette, cast shadows, strong ambient occlusion, specular glare, duplicated hero marks
```

### Padrões estruturados

Para tijolos, telhas e pedras assentadas, detalhe orientação das fileiras, amarração, tamanho aproximado dos módulos, largura/profundidade aparente das juntas e tolerância a irregularidade. Peça fileiras retas e escala consistente. Variação cromática deve ocorrer por elemento sem criar manchas únicas que denunciem o tile.

### Materiais orgânicos

Para reboco, terra, concreto, musgo e asfalto, peça distribuição isotrópica, sem fluxo dominante e sem um centro visual. Evite rachadura única, mancha circular grande ou gradiente de iluminação.

## 3. Seleção e iteração

Avalie leitura material, escala, ausência de perspectiva, iluminação neutra, estrutura emendável e diversidade sem um “ponto-herói”. Itere com uma alteração por vez:

- “Keep the material and scale unchanged; reduce the left-to-right lighting gradient only.”
- “Keep color and wear unchanged; make the mortar grid straighter and more consistent.”
- “Keep the surface unchanged; remove the single large stain and distribute small wear uniformly.”

## 4. Equalização da imagem

Antes de emendar:

1. corrija perspectiva e rotação;
2. remova gradientes de iluminação de baixa frequência;
3. preserve variação de albedo que pertence ao material;
4. normalize contraste sem esmagar juntas;
5. defina a escala física e recorte para uma unidade repetível.

Não confunda “luz desigual” com “variação material”. Use blur de grande escala, regressão de iluminação ou decomposição de frequência para estimar o campo de luz; subtraia/divida esse campo suavemente e revise visualmente.

## 5. Construção seamless

### Com juntas

Método do vídeo:

1. detecte linhas de argamassa/juntas;
2. alinhe-as a uma grade ou curva regular;
3. trate cada fileira separadamente;
4. escolha o corte dentro de uma junta, nunca através do centro de um elemento;
5. desloque/estique levemente a fileira para que a peça final de uma borda complete a inicial da outra;
6. repita no eixo vertical respeitando a amarração;
7. revise a largura da junta após a deformação.

Use deformações pequenas. Se o ajuste necessário for grande, volte à geração ou selecione outro período do padrão.

### Sem juntas claras

Método do vídeo:

1. desloque a imagem para trazer bordas ao centro;
2. sobreponha regiões de ambos os lados;
3. procure uma faixa em que cor, frequência e direção do detalhe sejam semelhantes;
4. misture com máscara irregular e de baixa evidência;
5. preserve detalhes de alta frequência e evite blur visível.

Faça os dois eixos e teste em mosaico. Uma emenda invisível no tile isolado pode formar uma cruz em repetição 8×8.

## 6. Geração dos mapas

### Base color

Deve conter cor intrínseca, sem sombras, highlights ou vinheta. Trabalhe em sRGB no arquivo/importação apropriada.

### Height

Represente altura relativa em escala de cinza linear. Em tijolos, a face fica acima da argamassa; lascas e rachaduras modulam esse relevo. Não copie a luminância da foto sem separar iluminação. Height só move geometria quando um shader/tessellation/displacement realmente o consome; sozinho é apenas dado.

### Normal

Derive do height e ajuste intensidade à escala real. Verifique o eixo Y: OpenGL e DirectX usam sinais opostos para o canal verde. Teste com luz girando; sulcos devem afundar, não estufar.

### Roughness

Modele o comportamento físico, não apenas a cor. Argamassa, pó e reboco tendem a ser mais ásperos; superfícies molhadas, metal polido e esmalte tendem a ser menos ásperos. Evite contraste extremo e ruído de alta frequência que cintile.

### AO, metallic e empacotamento

AO é opcional e deve ser sutil; não asse sombras largas no base color. Metallic deve ser semanticamente justificado. Se o engine empacota canais, documente a ordem, por exemplo ORM/RMA, e não compare memória por número de arquivos sem considerar formato e compressão.

## 7. Validação

Execute uma pré-validação local:

```powershell
python scripts/validate_texture.py caminho\material_basecolor.png --output caminho\validacao
```

O relatório mede descontinuidade nos pixels de borda e desequilíbrio de luminância, além de gerar mosaicos 3×3 e 8×8. As notas são heurísticas: textura procedural ou muito ruidosa pode pontuar mal e ainda parecer aceitável; uma textura pode pontuar bem e repetir uma mancha no centro.

Depois valide luz neutra e rasante, plano e mesh curvo, câmera próxima/média/distante, cada mapa em debug, custo GPU e memória após importação. Corrija a causa certa: iluminação, estrutura, emenda, mapa, escala, compressão ou shader. Não esconda todos os problemas com mais ruído.

## 8. Entrega por material

Use nomes consistentes:

```text
old_red_brick_basecolor.png
old_red_brick_normal_opengl.png
old_red_brick_height.png
old_red_brick_roughness.png
old_red_brick_orm.png
```

Inclua um manifesto com prompt, variação aprovada, escala em metros, resolução, convenção do normal, empacotamento, compressão e técnica anti-tiling.
