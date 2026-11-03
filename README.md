# md2canvas

Konverterar Markdown-filer till Canvas-vänlig HTML med inline-stilar som är redo att klistras in direkt i Canvas LMS.

## Filstruktur

```
md2canvas_script/
├── converter.py            # Startpunkt – CLI och konverteringslogik
├── markdown_extension.py   # Egna Markdown-extensions
├── styles/
│   ├── pages.css           # Inbyggd stil för Canvas-sidor (-p)
│   └── feedback.css        # Inbyggd stil för feedback (-g)
└── utils/
    ├── darcula_theme.py    # Pygments-tema för syntaxmarkering
    ├── parser.py           # Hjälpfunktion för att tolka egna block
    └── stdout_kit.py       # Färgad terminal-output
```

---

## Vad gör skriptet?

`converter.py` läser en `.md`-fil, konverterar den till HTML via [Markdown](https://pypi.org/project/Markdown/) och bäddar in stilarna inline med [css-inline](https://pypi.org/project/css-inline/). Det gör HTML-koden portabel och självständig, vilket är ett krav för att stilar ska fungera korrekt i Canvas.

### Aktiverade Markdown-extensions

| Extension     | Vad den gör                                 |
|---------------|---------------------------------------------|
| `fenced_code` | Kodblock med ` ```språk `                   |
| `codehilite`  | Syntaxmarkering via Pygments                |
| `toc`         | Automatisk innehållsförteckning med `[TOC]` |
| `nl2br`       | Enkla radbrytningar → `<br>`                |
| `sane_lists`  | Mer förutsägbar lista-hantering             |
| `tables`      | GFM-tabeller                                |
| `footnotes`   | Fotnoter med `[^1]`                         |

### Egna extensions

Skriptet lägger till ett antal egna syntaxkonstruktioner utöver standard-Markdown:

#### Inline-färg
Färglägg text med valfri CSS-färg (hex, rgb, namngivna färger, osv.):
```
::röd| Det här är röd text::
::#3498db| Det här är blå text::
::rgb(0,200,0)| Grön text::
```

#### Expanderbart block (collapsible)
Skapa ett `<details>`/`<summary>`-element:
```
^^^^ Rubrik på blocket
Innehåll som döljs som standard.
^^^^
```

#### Sidokommentar / callout-block
Markerat block med färgad vänsterkant. Inbyggda typer: `info`, `message`, `success`, `warning`.
```
!!!! info
Det här är ett informationsblock.
!!!!

!!!! warning
Varning! Något viktigt att notera.
!!!!
```
Du kan också ange en godtycklig CSS-färg direkt istället för ett nyckelord:

```
!!!! #8B5CF6
Lila callout-block.
!!!!
```

| Typ       | Färg           |
|-----------|----------------|
| `info`    | Gul `#FFC000`  |
| `message` | Blå `#00699D`  |
| `success` | Grön `#2B8D50` |
| `warning` | Röd `#C85550`  |

#### Länkhantering
- Alla externa länkar får automatiskt `target="_blank"` (öppnas i ny flik).
- Klassen `inline_disabled` läggs till på alla `<a>`-taggar för att förhindra att Canvas genererar förhandsvisningar (t.ex. för YouTube-länkar). Detta gör att Canvas-sidor ser ut renare.

---

## Installation

```bash
pip install markdown css-inline pygments
```

eller 

```bash
pip install -r requirements.txt
```

---

## Köra skriptet


```bash
python converter.py -f <fil.md> [alternativ]
```

### Flaggor

| Flagga                          | Beskrivning                                                                                                                                  |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `-f`, `--file`                  | **(Obligatorisk)** Sökväg till Markdown-filen som ska konverteras                                                                            |
| `-d`, `--dir`, `--dist`         | Utdatamapp. Standard: samma mapp som indatafilen                                                                                             |
| `-p`, `--page`                  | Använd den inbyggda stilen för **Canvas-sidor** (`styles/pages.css`)                                                                         |
| `-g`, `--grading`, `--feedback` | Använd den inbyggda stilen för **feedback** (**OBS!** Använd om du vill bifoga din feedback som en separat HTML-fil) (`styles/feedback.css`) |
| `-s`, `--styles`, `--css`       | Sökväg till en **egen** CSS-fil                                                                                                              |

> [!NOTE]
> Flaggorna `-p`, `-g` och `-s` är ömsesidigt uteslutande, du kan bara använda en åt gången.

### Exempel

```bash
# Konvertera till Canvas-sida med inbyggd stil, spara i samma mapp som filen
python converter.py -f ../vecka3/lektion.md -p

# Konvertera feedback med inbyggd stil, spara i en specifik mapp
python converter.py -f ../inlamning1/feedback.md -g -d ../dist/

# Konvertera med en helt egen CSS-fil
python converter.py -f ../modul2/intro.md -s ~/mina_stilar/canvas_custom.css
```

---

## Anpassa skriptet

### Byta syntaxmarkeringens färgtema

Färgtemat för kodblock definieras i [`utils/darcula_theme.py`](utils/darcula_theme.py) och är baserat på JetBrains Darcula. Du kan:

**Alternativ 1 – Använd ett inbyggt Pygments-tema**

Öppna [`converter.py`](converter.py) och ändra rad 46:

```python
# Byt ut DarculaStyle mot ett av Pygments inbyggda teman, t.ex.:
# 'monokai', 'dracula', 'github-dark', 'solarized-dark', 'nord', 'material', ...
formatter = HtmlFormatter(style="monokai")
```

Lista alla tillgängliga teman:

```bash
python -c "from pygments.styles import get_all_styles; print(list(get_all_styles()))"
```

Eller kika här: [pygments styles](https://pygments.org/styles/).

**Alternativ 2 – Skapa ett eget Pygments-tema**

Kopiera [`utils/darcula_theme.py`](utils/darcula_theme.py), byt namn på klassen och justera färgerna i `Colors`- och `styles`-diktionären. Importera sedan din nya klass i `converter.py`.

### Lägga till en Markdown-extension

Standardbiblioteket har fler extensions än de som aktiveras just nu. Se [Python-Markdowns dokumentation](https://python-markdown.github.io/extensions/) för en fullständig lista.

Lägg till en extension i [`converter.py`](converter.py), rad 34–41:

```python
md = markdown.Markdown(
    extensions=[
        ExtensionsRegister(),
        "fenced_code",
        "codehilite",
        "toc",
        "nl2br",
        "sane_lists",
        "tables",
        "footnotes",
        "attr_list",   # ← lägg till här, t.ex. attr_list för att sätta HTML-attribut
        "def_list",    # ← t.ex. definitionslistor
    ]
)
```

### Anpassa stilarna

**Snabbaste vägen** – skicka en egen CSS-fil med `-s`-flaggan:
```bash
python converter.py -f lektion.md -s min_stil.css
```

**Ändra de inbyggda stilarna** direkt i [`styles/pages.css`](styles/pages.css) eller [`styles/feedback.css`](styles/feedback.css). Några viktiga klasser:

| Selektor               | Vad den styr                                          |
|------------------------|-------------------------------------------------------|
| `.codehilite`          | Wrapper runt kodblock (padding, bredd, border-radius) |
| `.side-block`          | Callout/sidokommentar-block                           |
| `.collapsible-content` | Innehållet i ett expanderbart block                   |
| `summary`              | Rubrikraden i ett expanderbart block                  |
| `table th`             | Tabellhuvuden                                         |

### Lägga till en ny typ av callout-block

Öppna [`markdown_extension.py`](markdown_extension.py) och lägg till ett nytt nyckelord i `SideBlockProcessor.BLOCK_TYPES`:

```python
BLOCK_TYPES = {
    "info":    "#FFC000",
    "message": "#00699D",
    "success": "#2B8D50",
    "warning": "#C85550",
    "tip":     "#9B59B6",   # ← ny typ
}
```

Använd sedan `!!!! tip` i din Markdown-fil.

### Ändra breddbegränsningen för Canvas-sidor

I [`styles/pages.css`](styles/pages.css) begränsas bredden till `65ch` för att matcha MIUNs standardlayout för Canvas. Justera detta om du vill (kanske för att ta bort begränsningen?):

```css
body, hr, blockquote, summary, details, .side-block {
    max-width: none; /* justera efter behov */
}
```
