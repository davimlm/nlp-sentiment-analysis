## 📄 Especificação do JSON de Músicas (v1.1.0)

Este documento define o contrato de dados padrão para representar músicas em formato JSON. Essa estrutura deve ser usada para organizar, manipular e armazenar dados musicais de forma consistente, visando análise, geração de conteúdo, e uso em sistemas.

---

### ✅ Estrutura Geral

Cada música é representada como um objeto dentro de uma lista (`Array`):

```json
[
  {
    "name": "Nome da Música",
    "author": "Nome do Artista ou Banda",
    "lyrics": "Letra completa e limpa da música",
    "genre": "gênero normalizado",
    "year": 2001,
    "position": 1,
    "ref": "https://link-da-musica.com",
    "duration_in_seconds": 244,
    "explicit": false,
    "tempo_bpm": 92,
    "key": "C#m",
    "source": "spotify"
  }
]
```

---

### 🧩 Campos e Regras

| Campo                 | Tipo      | Obrigatório | Descrição                                                        |
| --------------------- | --------- | ----------- | ---------------------------------------------------------------- |
| `name`                | `string`  | ✅ Sim      | Nome completo da música                                          |
| `author`              | `string`  | ✅ Sim      | Nome do artista ou banda                                         |
| `lyrics`              | `string`  | ✅ Sim      | Letra completa e limpa (sem HTML, sem caracteres especiais)      |
| `genre`               | `string`  | ✅ Sim      | Gênero musical **normalizado** (ver abaixo)                      |
| `year`                | `int`     | ✅ Sim      | Ano de lançamento                                                |
| `position`            | `int`     | ❌ Opcional | Posição da música entre as mais ouvidas no ano                   |
| `ref`                 | `string`  | ✅ Sim      | Link da música (Spotify, YouTube, etc.)                          |
| `duration_in_seconds` | `int`     | ❌ Opcional | Duração da música em segundos                                    |
| `explicit`            | `boolean` | ❌ Opcional | Indica se a música possui conteúdo explícito (`true` ou `false`) |
| `tempo_bpm`           | `int`     | ❌ Opcional | Batidas por minuto da faixa (BPM)                                |
| `key`                 | `string`  | ❌ Opcional | Tom da música (ex: `"C#m"`, `"G"`)                               |
| `source`              | `string`  | ✅ Sim      | Fonte dos dados (`"spotify"`, `"genius"`, `"deezer"`, etc.)      |

---

### 🧼 Normalização de `genre`

O campo `genre` **deve estar em caixa baixa, sem espaços extras ou variações inconsistentes**. Exemplo de valores válidos:

- `"mpb"`
- `"samba"`
- `"rock"`
- `"rap"`
- `"sertanejo"`
- `"funk"`
