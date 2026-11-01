# Prompts para GPT Images

Os prompts abaixo são reconstruções originais baseadas no processo mostrado no vídeo. Não são prompts literais do autor.

## Tijolo antigo — base para material tileable

```text
Use case: stylized-concept
Asset type: tileable game texture source
Primary request: weathered late-19th-century Central European red brick wall, lived-in rather than ruined
Subject: one continuous brick surface filling the entire image; running-bond rows; handmade brick variation; narrow aged lime mortar
Style/medium: realistic PBR material reference, front-facing orthographic capture
Composition/framing: square, edge-to-edge, no perspective, consistent scale; bricks approximately 24 cm by 7 cm
Lighting/mood: perfectly even neutral diffuse light; no directional shadows; no baked highlights
Materials/textures: muted red and brown bricks, occasional dark fired bricks, restrained chips, subtle mineral deposits, mortar slightly recessed
Constraints: tile-friendly row structure; straight horizontal courses; no isolated focal damage; no objects; no borders; no text; no logos; no watermark
Avoid: vignette, corner darkness, graffiti, large unique cracks, wet specular glare, perspective convergence, dramatic lighting
```

## Reboco gasto

```text
Use case: stylized-concept
Asset type: tileable game texture source
Primary request: old gray mineral plaster from a damp European backstreet, worn but maintained
Subject: continuous plaster surface filling the frame
Style/medium: realistic PBR material reference, front-facing orthographic capture
Composition/framing: square, edge-to-edge, isotropic detail, no center of interest, no perspective
Lighting/mood: even neutral diffuse illumination, flat exposure, no cast shadows
Materials/textures: fine sand grain, subtle trowel variation, small dispersed hairline cracks, faint moisture discoloration distributed uniformly
Constraints: tile-friendly; balanced detail at macro and micro scales; no exposed brick; no isolated large stain; no text; no watermark
Avoid: directional streaks, vignette, dramatic contrast, large recognizable crack, strong ambient occlusion
```

## Paralelepípedo molhado sem iluminação assada

```text
Use case: stylized-concept
Asset type: tileable game texture source
Primary request: historic dark granite cobblestones for a recently rained-on street
Subject: continuous top-down cobblestone paving with plausible irregular stones and narrow joints
Style/medium: realistic PBR material reference
Composition/framing: square top-down orthographic view, edge-to-edge, consistent stone scale, no perspective
Lighting/mood: neutral diffuse capture; no sky reflection or directional highlight baked into the color
Materials/textures: charcoal and cool-gray granite, restrained color variation, worn rounded edges, joints lower than stones
Constraints: tile-friendly joint network; no puddles in the base color; no leaves, litter, text, borders, logos or watermark
Avoid: single hero stone, strong wet glare, long shadow, perspective, radial pattern
```

Adicione o aspecto molhado no shader por roughness, reflection e puddle masks; não asse reflexos no base color.

## Lote de variações de tijolo

Planeje as variações primeiro e gere cada asset separadamente:

1. pale limewashed;
2. dark soot-stained;
3. yellow clinker;
4. mossy damp;
5. patchy red limewash;
6. glazed dark red;
7. modern precise red;
8. narrow Gothic brick.

Use o prompt-base de tijolo, alterando apenas material, cor, época, desgaste e dimensões. Repita todas as restrições de câmera, iluminação e escala em cada chamada. Não peça oito materiais distintos dentro de uma única imagem de produção.

## Concept sheet de 12 materiais

Use somente para direção artística e comparação, não como fonte final de mapas:

```text
Use case: stylized-concept
Asset type: game-material concept sheet
Primary request: a coherent set of 12 material swatches for one damp Central European backstreet: red brick, gray plaster, ochre plaster, cobblestone, concrete slabs, granite, asphalt, painted wood, aged iron, weathered zinc, roof tiles, mossy concrete
Composition/framing: clean 4-by-3 grid of equal square swatches; each swatch front-facing and edge-to-edge inside its cell
Lighting/mood: identical neutral diffuse illumination for every swatch
Style/medium: realistic PBR material reference, consistent age and art direction
Constraints: no perspective; no scene objects; no decorative frame; no logos; no watermark; no text except short material names if explicitly needed
```

Depois da aprovação, gere os 12 individualmente.

## Trim sheet arquitetônico

```text
Use case: stylized-concept
Asset type: architectural trim sheet source for a game building
Primary request: one coherent vertical trim sheet for a worn late-19th-century Central European tenement
Subject: horizontal strips for cornice molding, dentil blocks, plaster band, stone windowsill, painted wooden window frame, weathered zinc flashing, red brick trim, dark granite plinth
Style/medium: realistic PBR material reference, consistent age and palette
Composition/framing: orthographic front view; eight clean horizontal strips; every strip runs seamlessly from left to right; clear padding between strips; no perspective
Lighting/mood: perfectly even neutral diffuse illumination; no cast shadows or highlights
Constraints: strip boundaries straight and aligned; repeatable horizontally; no labels; no scene; no objects; no logos; no watermark
Avoid: diagonal elements, perspective, unique end caps, lighting gradients, mixed scales inside one strip
```

Valide cada faixa em repetição horizontal e deixe margem para mip bleeding.

## Decals de sujeira e dano

Gere um decal por chamada. Exemplo:

```text
Use case: background-extraction
Asset type: transparent game decal
Primary request: irregular vertical rain-and-dirt streak that forms below an old stone windowsill
Style/medium: realistic weathering decal
Composition/framing: centered mark with generous transparent padding; vertical flow; feathered edges
Color palette: subtle dark gray-brown with faint green dampness
Constraints: genuinely transparent background; no wall texture; no frame; no text; no logo; no watermark; physically plausible gravity direction
Avoid: rectangular edge, symmetrical shape, opaque background, dramatic black stain
```

Variações úteis: ferrugem sob metal, umidade na base, fissura fina e escorrimento sob cano. Coloque-as por regras contextuais, não aleatoriamente.

## Interior falso para janela

```text
Use case: stylized-concept
Asset type: interior-mapping texture for a game window
Primary request: modest lived-in apartment room seen from outside through a window, suitable for parallax interior mapping
Scene/backdrop: shallow room with side walls, ceiling and floor converging toward a rear wall; a few restrained furnishings
Style/medium: realistic architectural interior render
Composition/framing: centered one-point perspective, camera perpendicular to the window plane, room-box boundaries readable, no visible exterior frame
Lighting/mood: dim cool ambient room with one small warm practical light
Constraints: no people; no text; no logos; no exterior reflection; no fisheye distortion; no watermark
```

Teste a imagem no shader de interior mapping; uma imagem bonita pode falhar se os planos de perspectiva não casarem com a caixa virtual.

## Pedido de correção direcionada

Para editar uma geração aprovada:

```text
Input images: Image 1: approved material source
Primary request: correct only the horizontal lighting gradient and make the left and right edges match more closely
Constraints: preserve material identity, brick layout, physical scale, color palette, wear, and all fine surface detail; do not add new damage, objects, shadows, highlights, text or borders
```

Repita as invariantes em cada iteração. Faça uma correção por vez.
