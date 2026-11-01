# AI Game Textures

Skill para criar, preparar e validar texturas de jogos com foco em GPT Images, materiais PBR, seamless tiling, trim sheets, decals e integração em Godot ou Unreal.

O fluxo foi inspirado no vídeo [This Is How to Make Game Textures With AI](https://www.youtube.com/watch?v=_rMMP7GPgt4), do canal Can It Code?, e ampliado com critérios de produção, limites explícitos e validação reproduzível.

## O que a skill cobre

- comparação entre GPT Images, shaders procedurais, Blender e bibliotecas PBR;
- prompts para materiais, variações, trim sheets, decals e interior mapping;
- preparação de base color, height, normal e roughness;
- correção de tiling estruturado e orgânico;
- macrovariação, hex tiling, mipmaps, triplanar e POM;
- estados de entrega `source`, `prepared` e `game-ready`;
- validação em mosaicos 3×3 e 8×8.

## Estrutura

```text
SKILL.md
agents/openai.yaml
references/
  gpt-images-workflow.md
  pbr-integration.md
  prompt-recipes.md
  video-methods.md
scripts/
  validate_texture.py
```

## Validador de textura

O script requer Python e Pillow:

```powershell
python -m pip install Pillow
python scripts/validate_texture.py caminho\material_basecolor.png --output caminho\validacao
```

Ele gera mosaicos, visualizações da diferença entre bordas e um relatório JSON com métricas heurísticas. A aprovação final ainda deve acontecer no mesh e no engine-alvo.

## Uso no Codex

Depois de instalar a skill, invoque:

```text
$ai-game-textures
```

Exemplo:

```text
Use $ai-game-textures para criar um material PBR de tijolo antigo com GPT Images e validar o tiling para Godot.
```

## Observação importante

A ferramenta automática mostrada no vídeo pertence ao autor e não é distribuída aqui. Esta skill documenta como reproduzir o pipeline e deixa explícito o que foi apenas gerado, preparado ou realmente validado no engine.
