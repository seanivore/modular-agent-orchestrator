# Setting Up Markdown Color Highlighting in Zed

## Important Update: Theme Confusion Solved!

I found the issue! The Blankeos Zen theme has two variants in the same file:

1. "Blankeos Zen Dark" (regular version)  
2. "Blankeos Zen Dark (Blurred)" (blurred version) 

According to your settings, you're using the *blurred* version, but we were editing the regular version. That's why some changes weren't showing up!

## What's Included

I've created an updated settings template for Zed that will help you get the vibrant Markdown color highlighting you're used to from VSCode/Cursor. This includes:

- Setting JetBrains Mono as your editor font
- Customized colors for Markdown elements:
  - Headings (titles) in orange
  - Bold text in gold
  - Italic text in light blue
  - Code blocks in teal
  - Inline code in green
  - Links in purple/blue
  - List markers in gold

## How to Apply These Settings

1. Open your Zed settings file:

```bash
open ~/.config/zed/settings.json
```

2. Add/replace these settings in your `settings.json` file. Be careful to merge these with your existing settings rather than completely replacing the file.

```json
{
  "editor.font_family": "JetBrains Mono",
  "experimental.theme_overrides": {
    "syntax": {
      "title": {
        "color": "#FF9D00",
        "font_style": "oblique",
        "font_weight": null
      },
      "emphasis.strong": {
        "color": "#FFD866",
        "font_style": "oblique",
        "font_weight": null
      },
      "emphasis": {
        "color": "#78DCE8",
        "font_style": "italic",
        "font_weight": null
      },
      "punctuation.list_marker": {
        "color": "#dfc532",
        "font_style": "oblique",
        "font_weight": null
      },
      "text.literal": {
        "color": "#67fc85",
        "font_style": null,
        "font_weight": null
      },
      "string.special": {
        "color": "#67fce8",
        "font_style": null,
        "font_weight": null
      },
      "link_text": {
        "color": "#AB9DF2",
        "font_style": null,
        "font_weight": null
      },
      "link_uri": {
        "color": "#8BE9FD",
        "font_style": null,
        "font_weight": null
      }
    }
  }
}
```

## Understanding Zed's Syntax Highlighting

Zed uses a different system from VSCode for syntax highlighting:

- VSCode uses TextMate scopes (like `markup.heading`, `entity.name.section`)
- Zed uses Tree-sitter captures (like `@title`, `@emphasis.strong`)

Here's how they map:

| VSCode TextMate Scope               | Zed Capture               | Element                                             |
| ----------------------------------- | ------------------------- | --------------------------------------------------- |
| `markup.heading`                    | `title`                   | Headings (# Title)                                  |
| `markup.bold`                       | `emphasis.strong`         | Bold text (**bold**)                                |
| `markup.italic`                     | `emphasis`                | Italic text (*italic*)                              |
| `markup.fenced_code`                | `string.special`          | Code blocks (```code```)                            |
| `markup.inline.raw`                 | `text.literal`            | Inline code (`code`)                                |
| `markup.link`                       | `link_text`               | Link text ([text](../../../single-file-agents/url)) |
| `string.other.link.destination`     | `link_uri`                | Link URLs                                           |
| `punctuation.definition.list.begin` | `punctuation.list_marker` | List bullets/numbers                                |

## Special Note About Font Styles

In Zed, there appear to be some limitations with font styles in the Blankeos theme:

- `bold` font weight doesn't seem to work properly
- Use `oblique` instead of `bold` for emphasis
- `italic` works fine for standard emphasis

This is why we're using `oblique` for titles, bold text, and list markers.

## Feedback for Zed Developers

Possible improvements for Zed:
1. Add color picker UI for hex colors in theme/settings files
2. Support comments in settings.json files (like JSONC format)
3. Add more granular control over Markdown styling
4. Improve documentation about the @capture system
5. Fix font weight handling in themes
6. Add a visual preview of themes in settings