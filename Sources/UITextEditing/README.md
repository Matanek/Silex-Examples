# Text history and word navigation

The gallery combines a short field, a long line and multiline text.
It uses GFX.UI bindings, identities and viewports without an application-owned
history manager.

From the workspace or owning Spec group root:

```sh
silex run Silex-Examples/Sources/UITextEditing/Main.sx --release
```

Click a field and type several characters. Cmd/Ctrl+Z undoes contiguous typing;
Shift+Cmd/Ctrl+Z or Ctrl+Y redoes it. Move the caret before typing again to start
another unit. Select text before replacing it, then undo: the selection returns
with its original direction.

Option/Ctrl+arrows move by words; add Shift to select them.
Option/Ctrl+Backspace or Delete removes text to the corresponding boundary.
Combined accents and emoji remain whole. Punctuation and Unicode spaces follow
the editor rules documented in [GFX.UI](../../../Packages/GFX.UI/Docs/EN/Text-Editing.md).

F2 or the theme button preserves history. F3 or “Valeurs initiales” imposes the
initial values: histories whose value changes are reset. The long line and
multiline field reveal the caret after editing, navigation and undo/redo.
Resize the window to check the same gestures.

Click the long line, drag beyond its left or right edge, then hold the button
without moving: text and selection continue advancing. In multiline text,
also try the top, bottom and a diagonal, while staying inside the window.
Release to stop, replace the selection, then undo to recover text and selection.

The executable accepts `--cpu-check`: it exercises history, words, themes, held
selection and 900/480/200/1 widths without opening a window. Debug/Release tests qualify this
mode; trying the graphical gallery is separate. IME and touch are not
demonstrated here.

[Guide français](README.fr.md).

Bundled fallback fonts display the gallery’s ideographs and monochrome emojis.
Letter shortcuts follow the logical keyboard layout, including Cmd+Z on AZERTY.
CPU checks also verify that actual drawing has no missing glyphs and exercise
the event bridge.
