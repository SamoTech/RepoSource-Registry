# RepoSource Registry

> **A living, machine-readable index of notable public GitHub repositories.**
>
> GitHub is the upstream source; RepoSource Registry normalizes, validates, classifies, and publishes the resulting dataset for humans and machines.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Minimum Stars](https://img.shields.io/badge/minimum%20stars-2,000%2B-blue)](config.json)

---

## Index at a glance

| Metric | Value |
|---|---:|
| Indexed repositories | **33,180** |
| Minimum stars | **2,000+** |
| Languages represented | **213** |
| Derived categories | **7** |
| Last synchronized | **2026-09-13T06:39:43Z** |

> **Popularity index, not an endorsement.** Stars indicate popularity, not software quality, security, or suitability.

## Machine-readable data

The README is a presentation layer. Applications should consume the published datasets directly.

| Resource | Purpose |
|---|---|
| [`repositories.json`](data/repositories.json) | Canonical dataset |
| [`repositories.csv`](data/repositories.csv) | Tabular export |
| [`manifest.json`](data/manifest.json) | Dataset metadata and SHA-256 integrity data |
| [`statistics.json`](data/statistics.json) | Dataset analytics |
| [`sync.json`](data/sync.json) | Synchronization audit record |
| [`changes.json`](data/changes.json) | Added/removed/changed repository feed |
| [`schema/repository.schema.json`](schema/repository.schema.json) | Data contract |

### Quick consumption

```bash
curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json
```

## Most starred

| # | Repository | Stars | Language | Activity |
|---:|---|---:|---|---|
| 1 | [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 546,891 | Markdown | active |
| 2 | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | 505,537 | No declared language | active |
| 3 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | 479,508 | Python | active |
| 4 | [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) | 455,371 | TypeScript | active |
| 5 | [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books) | 396,641 | Python | active |
| 6 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 389,546 | TypeScript | active |
| 7 | [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 369,659 | Python | active |
| 8 | [nilbuild/developer-roadmap](https://github.com/nilbuild/developer-roadmap) | 367,012 | TypeScript | active |
| 9 | [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) | 360,809 | No declared language | inactive |
| 10 | [vinta/awesome-python](https://github.com/vinta/awesome-python) | 320,304 | Python | active |
| 11 | [awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) | 318,872 | No declared language | active |
| 12 | [obra/superpowers](https://github.com/obra/superpowers) | 285,890 | Shell | active |
| 13 | [practical-tutorials/project-based-learning](https://github.com/practical-tutorials/project-based-learning) | 283,108 | Python | active |
| 14 | [996icu/996.ICU](https://github.com/996icu/996.ICU) | 276,996 | No declared language | inactive |
| 15 | [mattpocock/skills](https://github.com/mattpocock/skills) | 260,667 | Shell | active |
| 16 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 257,258 | JavaScript | active |
| 17 | [react/react](https://github.com/react/react) | 250,094 | JavaScript | active |
| 18 | [torvalds/linux](https://github.com/torvalds/linux) | 248,447 | C | active |
| 19 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 244,960 | Python | active |
| 20 | [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 243,446 | No declared language | inactive |
| 21 | [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | 224,519 | Python | active |
| 22 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 221,870 | TypeScript | active |
| 23 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 212,652 | No declared language | active |
| 24 | [vuejs/vue](https://github.com/vuejs/vue) | 212,484 | TypeScript | inactive |
| 25 | [ossu/computer-science](https://github.com/ossu/computer-science) | 208,958 | HTML | active |

## Language index

| Language | Repositories | Dataset |
|---|---:|---|
| **Python** | 5,871 | [`python.json`](data/languages/python.json) |
| **JavaScript** | 3,980 | [`javascript.json`](data/languages/javascript.json) |
| **TypeScript** | 3,607 | [`typescript.json`](data/languages/typescript.json) |
| **No declared language** | 2,726 | [`no-declared-language.json`](data/languages/no-declared-language.json) |
| **Go** | 2,298 | [`go.json`](data/languages/go.json) |
| **Java** | 1,945 | [`java.json`](data/languages/java.json) |
| **C++** | 1,702 | [`c-3.json`](data/languages/c-3.json) |
| **Rust** | 1,238 | [`rust.json`](data/languages/rust.json) |
| **C** | 1,211 | [`c.json`](data/languages/c.json) |
| **C#** | 930 | [`c-2.json`](data/languages/c-2.json) |
| **Shell** | 793 | [`shell.json`](data/languages/shell.json) |
| **PHP** | 752 | [`php.json`](data/languages/php.json) |
| **HTML** | 737 | [`html.json`](data/languages/html.json) |
| **Jupyter Notebook** | 722 | [`jupyter-notebook.json`](data/languages/jupyter-notebook.json) |
| **Swift** | 680 | [`swift.json`](data/languages/swift.json) |
| **Ruby** | 480 | [`ruby.json`](data/languages/ruby.json) |
| **Kotlin** | 469 | [`kotlin.json`](data/languages/kotlin.json) |
| **Objective-C** | 426 | [`objective-c.json`](data/languages/objective-c.json) |
| **CSS** | 290 | [`css.json`](data/languages/css.json) |
| **Vue** | 238 | [`vue.json`](data/languages/vue.json) |
| **Dart** | 214 | [`dart.json`](data/languages/dart.json) |
| **Lua** | 187 | [`lua.json`](data/languages/lua.json) |
| **PowerShell** | 92 | [`powershell.json`](data/languages/powershell.json) |
| **Vim Script** | 90 | [`vim-script-2.json`](data/languages/vim-script-2.json) |
| **Scala** | 83 | [`scala.json`](data/languages/scala.json) |
| **TeX** | 75 | [`tex.json`](data/languages/tex.json) |
| **SCSS** | 66 | [`scss.json`](data/languages/scss.json) |
| **Makefile** | 54 | [`makefile.json`](data/languages/makefile.json) |
| **Elixir** | 47 | [`elixir.json`](data/languages/elixir.json) |
| **Markdown** | 47 | [`markdown.json`](data/languages/markdown.json) |
| **Haskell** | 46 | [`haskell.json`](data/languages/haskell.json) |
| **Clojure** | 45 | [`clojure.json`](data/languages/clojure.json) |
| **MDX** | 45 | [`mdx.json`](data/languages/mdx.json) |
| **Dockerfile** | 43 | [`dockerfile.json`](data/languages/dockerfile.json) |
| **Perl** | 39 | [`perl.json`](data/languages/perl.json) |
| **CoffeeScript** | 37 | [`coffeescript.json`](data/languages/coffeescript.json) |
| **Assembly** | 35 | [`assembly.json`](data/languages/assembly.json) |
| **Emacs Lisp** | 34 | [`emacs-lisp.json`](data/languages/emacs-lisp.json) |
| **Batchfile** | 30 | [`batchfile.json`](data/languages/batchfile.json) |
| **R** | 27 | [`r.json`](data/languages/r.json) |
| **Zig** | 26 | [`zig.json`](data/languages/zig.json) |
| **HCL** | 23 | [`hcl.json`](data/languages/hcl.json) |
| **Cuda** | 21 | [`cuda.json`](data/languages/cuda.json) |
| **Svelte** | 21 | [`svelte.json`](data/languages/svelte.json) |
| **Astro** | 20 | [`astro.json`](data/languages/astro.json) |
| **Nix** | 20 | [`nix.json`](data/languages/nix.json) |
| **Vim script** | 20 | [`vim-script.json`](data/languages/vim-script.json) |
| **GDScript** | 19 | [`gdscript.json`](data/languages/gdscript.json) |
| **OCaml** | 19 | [`ocaml.json`](data/languages/ocaml.json) |
| **Solidity** | 18 | [`solidity.json`](data/languages/solidity.json) |
| **Objective-C++** | 17 | [`objective-c-2.json`](data/languages/objective-c-2.json) |
| **CMake** | 14 | [`cmake.json`](data/languages/cmake.json) |
| **QML** | 13 | [`qml.json`](data/languages/qml.json) |
| **Common Lisp** | 12 | [`common-lisp.json`](data/languages/common-lisp.json) |
| **Erlang** | 12 | [`erlang.json`](data/languages/erlang.json) |
| **Groovy** | 12 | [`groovy.json`](data/languages/groovy.json) |
| **Jinja** | 12 | [`jinja.json`](data/languages/jinja.json) |
| **MATLAB** | 12 | [`matlab-2.json`](data/languages/matlab-2.json) |
| **Pascal** | 12 | [`pascal.json`](data/languages/pascal.json) |
| **Verilog** | 12 | [`verilog.json`](data/languages/verilog.json) |
| **Rich Text Format** | 11 | [`rich-text-format.json`](data/languages/rich-text-format.json) |
| **Vala** | 11 | [`vala.json`](data/languages/vala.json) |
| **GLSL** | 9 | [`glsl.json`](data/languages/glsl.json) |
| **Julia** | 9 | [`julia.json`](data/languages/julia.json) |
| **PLpgSQL** | 9 | [`plpgsql.json`](data/languages/plpgsql.json) |
| **Pug** | 9 | [`pug.json`](data/languages/pug.json) |
| **Crystal** | 8 | [`crystal.json`](data/languages/crystal.json) |
| **F#** | 7 | [`f.json`](data/languages/f.json) |
| **Go Template** | 7 | [`go-template.json`](data/languages/go-template.json) |
| **Haxe** | 7 | [`haxe.json`](data/languages/haxe.json) |
| **Less** | 7 | [`less.json`](data/languages/less.json) |
| **ShaderLab** | 7 | [`shaderlab.json`](data/languages/shaderlab.json) |
| **VimL** | 7 | [`viml.json`](data/languages/viml.json) |
| **Visual Basic .NET** | 7 | [`visual-basic-net.json`](data/languages/visual-basic-net.json) |
| **YARA** | 7 | [`yara.json`](data/languages/yara.json) |
| **Adblock Filter List** | 6 | [`adblock-filter-list.json`](data/languages/adblock-filter-list.json) |
| **AutoIt** | 6 | [`autoit.json`](data/languages/autoit.json) |
| **Cython** | 6 | [`cython.json`](data/languages/cython.json) |
| **Elm** | 6 | [`elm.json`](data/languages/elm.json) |
| **Roff** | 6 | [`roff.json`](data/languages/roff.json) |
| **YAML** | 6 | [`yaml.json`](data/languages/yaml.json) |
| **Bikeshed** | 5 | [`bikeshed.json`](data/languages/bikeshed.json) |
| **Blade** | 5 | [`blade.json`](data/languages/blade.json) |
| **EJS** | 5 | [`ejs.json`](data/languages/ejs.json) |
| **Jsonnet** | 5 | [`jsonnet.json`](data/languages/jsonnet.json) |
| **Matlab** | 5 | [`matlab.json`](data/languages/matlab.json) |
| **Nim** | 5 | [`nim.json`](data/languages/nim.json) |
| **Nunjucks** | 5 | [`nunjucks.json`](data/languages/nunjucks.json) |
| **TSQL** | 5 | [`tsql.json`](data/languages/tsql.json) |
| **XSLT** | 5 | [`xslt.json`](data/languages/xslt.json) |
| **ActionScript** | 4 | [`actionscript.json`](data/languages/actionscript.json) |
| **AutoHotkey** | 4 | [`autohotkey.json`](data/languages/autohotkey.json) |
| **D** | 4 | [`d.json`](data/languages/d.json) |
| **Inno Setup** | 4 | [`inno-setup.json`](data/languages/inno-setup.json) |
| **NSIS** | 4 | [`nsis.json`](data/languages/nsis.json) |
| **OpenSCAD** | 4 | [`openscad.json`](data/languages/openscad.json) |
| **Reason** | 4 | [`reason.json`](data/languages/reason.json) |
| **Smali** | 4 | [`smali.json`](data/languages/smali.json) |
| **Starlark** | 4 | [`starlark.json`](data/languages/starlark.json) |
| **SystemVerilog** | 4 | [`systemverilog.json`](data/languages/systemverilog.json) |
| **Vim Snippet** | 4 | [`vim-snippet.json`](data/languages/vim-snippet.json) |
| **Awk** | 3 | [`awk.json`](data/languages/awk.json) |
| **Bicep** | 3 | [`bicep.json`](data/languages/bicep.json) |
| **Fluent** | 3 | [`fluent.json`](data/languages/fluent.json) |
| **Handlebars** | 3 | [`handlebars.json`](data/languages/handlebars.json) |
| **HLSL** | 3 | [`hlsl.json`](data/languages/hlsl.json) |
| **Just** | 3 | [`just.json`](data/languages/just.json) |
| **Mustache** | 3 | [`mustache.json`](data/languages/mustache.json) |
| **Processing** | 3 | [`processing.json`](data/languages/processing.json) |
| **Sass** | 3 | [`sass.json`](data/languages/sass.json) |
| **Stylus** | 3 | [`stylus.json`](data/languages/stylus.json) |
| **SVG** | 3 | [`svg.json`](data/languages/svg.json) |
| **SWIG** | 3 | [`swig.json`](data/languages/swig.json) |
| **V** | 3 | [`v.json`](data/languages/v.json) |
| **WebAssembly** | 3 | [`webassembly.json`](data/languages/webassembly.json) |
| **ASL** | 2 | [`asl.json`](data/languages/asl.json) |
| **Classic ASP** | 2 | [`classic-asp.json`](data/languages/classic-asp.json) |
| **DIGITAL Command Language** | 2 | [`digital-command-language.json`](data/languages/digital-command-language.json) |
| **Fennel** | 2 | [`fennel.json`](data/languages/fennel.json) |
| **G-code** | 2 | [`g-code.json`](data/languages/g-code.json) |
| **Gleam** | 2 | [`gleam.json`](data/languages/gleam.json) |
| **Hack** | 2 | [`hack.json`](data/languages/hack.json) |
| **HolyC** | 2 | [`holyc.json`](data/languages/holyc.json) |
| **JSON** | 2 | [`json.json`](data/languages/json.json) |
| **Lean** | 2 | [`lean.json`](data/languages/lean.json) |
| **LLVM** | 2 | [`llvm.json`](data/languages/llvm.json) |
| **Logos** | 2 | [`logos.json`](data/languages/logos.json) |
| **Mermaid** | 2 | [`mermaid.json`](data/languages/mermaid.json) |
| **Mojo** | 2 | [`mojo.json`](data/languages/mojo.json) |
| **Move** | 2 | [`move.json`](data/languages/move.json) |
| **Nushell** | 2 | [`nushell.json`](data/languages/nushell.json) |
| **PureScript** | 2 | [`purescript.json`](data/languages/purescript.json) |
| **reStructuredText** | 2 | [`restructuredtext.json`](data/languages/restructuredtext.json) |
| **Scheme** | 2 | [`scheme.json`](data/languages/scheme.json) |
| **Text** | 2 | [`text.json`](data/languages/text.json) |
| **Tree-sitter Query** | 2 | [`tree-sitter-query.json`](data/languages/tree-sitter-query.json) |
| **Twig** | 2 | [`twig.json`](data/languages/twig.json) |
| **TypeSpec** | 2 | [`typespec.json`](data/languages/typespec.json) |
| **VBScript** | 2 | [`vbscript.json`](data/languages/vbscript.json) |
| **VHDL** | 2 | [`vhdl.json`](data/languages/vhdl.json) |
| **Visual Basic** | 2 | [`visual-basic.json`](data/languages/visual-basic.json) |
| **Wolfram Language** | 2 | [`wolfram-language.json`](data/languages/wolfram-language.json) |
| **AGS Script** | 1 | [`ags-script.json`](data/languages/ags-script.json) |
| **AngelScript** | 1 | [`angelscript.json`](data/languages/angelscript.json) |
| **ANTLR** | 1 | [`antlr.json`](data/languages/antlr.json) |
| **ApacheConf** | 1 | [`apacheconf.json`](data/languages/apacheconf.json) |
| **AppleScript** | 1 | [`applescript.json`](data/languages/applescript.json) |
| **AsciiDoc** | 1 | [`asciidoc.json`](data/languages/asciidoc.json) |
| **ASP** | 1 | [`asp.json`](data/languages/asp.json) |
| **Ballerina** | 1 | [`ballerina.json`](data/languages/ballerina.json) |
| **BitBake** | 1 | [`bitbake.json`](data/languages/bitbake.json) |
| **BlitzBasic** | 1 | [`blitzbasic.json`](data/languages/blitzbasic.json) |
| **Boo** | 1 | [`boo.json`](data/languages/boo.json) |
| **C3** | 1 | [`c3.json`](data/languages/c3.json) |
| **Chapel** | 1 | [`chapel.json`](data/languages/chapel.json) |
| **COBOL** | 1 | [`cobol.json`](data/languages/cobol.json) |
| **CodeQL** | 1 | [`codeql.json`](data/languages/codeql.json) |
| **Common Workflow Language** | 1 | [`common-workflow-language.json`](data/languages/common-workflow-language.json) |
| **Dhall** | 1 | [`dhall.json`](data/languages/dhall.json) |
| **F*** | 1 | [`f-2.json`](data/languages/f-2.json) |
| **Flix** | 1 | [`flix.json`](data/languages/flix.json) |
| **FreeMarker** | 1 | [`freemarker.json`](data/languages/freemarker.json) |
| **Frege** | 1 | [`frege.json`](data/languages/frege.json) |
| **GDShader** | 1 | [`gdshader.json`](data/languages/gdshader.json) |
| **Gherkin** | 1 | [`gherkin.json`](data/languages/gherkin.json) |
| **Git Attributes** | 1 | [`git-attributes.json`](data/languages/git-attributes.json) |
| **Haml** | 1 | [`haml.json`](data/languages/haml.json) |
| **hoon** | 1 | [`hoon.json`](data/languages/hoon.json) |
| **IDL** | 1 | [`idl.json`](data/languages/idl.json) |
| **Idris** | 1 | [`idris.json`](data/languages/idris.json) |
| **Jai** | 1 | [`jai.json`](data/languages/jai.json) |
| **Janet** | 1 | [`janet.json`](data/languages/janet.json) |
| **KiCad Layout** | 1 | [`kicad-layout.json`](data/languages/kicad-layout.json) |
| **Koka** | 1 | [`koka.json`](data/languages/koka.json) |
| **Liquid** | 1 | [`liquid.json`](data/languages/liquid.json) |
| **LiveScript** | 1 | [`livescript.json`](data/languages/livescript.json) |
| **Mathematica** | 1 | [`mathematica.json`](data/languages/mathematica.json) |
| **Meson** | 1 | [`meson.json`](data/languages/meson.json) |
| **Metal** | 1 | [`metal.json`](data/languages/metal.json) |
| **MLIR** | 1 | [`mlir.json`](data/languages/mlir.json) |
| **MoonBit** | 1 | [`moonbit.json`](data/languages/moonbit.json) |
| **MoonScript** | 1 | [`moonscript.json`](data/languages/moonscript.json) |
| **Nu** | 1 | [`nu.json`](data/languages/nu.json) |
| **Objective-J** | 1 | [`objective-j.json`](data/languages/objective-j.json) |
| **Odin** | 1 | [`odin.json`](data/languages/odin.json) |
| **Open Policy Agent** | 1 | [`open-policy-agent.json`](data/languages/open-policy-agent.json) |
| **OpenQASM** | 1 | [`openqasm.json`](data/languages/openqasm.json) |
| **PlantUML** | 1 | [`plantuml.json`](data/languages/plantuml.json) |
| **PLSQL** | 1 | [`plsql.json`](data/languages/plsql.json) |
| **Pony** | 1 | [`pony.json`](data/languages/pony.json) |
| **PostScript** | 1 | [`postscript.json`](data/languages/postscript.json) |
| **Prolog** | 1 | [`prolog.json`](data/languages/prolog.json) |
| **PureBasic** | 1 | [`purebasic.json`](data/languages/purebasic.json) |
| **Racket** | 1 | [`racket.json`](data/languages/racket.json) |
| **Red** | 1 | [`red.json`](data/languages/red.json) |
| **Ren'Py** | 1 | [`ren-py.json`](data/languages/ren-py.json) |
| **RenderScript** | 1 | [`renderscript.json`](data/languages/renderscript.json) |
| **Riot** | 1 | [`riot.json`](data/languages/riot.json) |
| **RobotFramework** | 1 | [`robotframework.json`](data/languages/robotframework.json) |
| **Rocq Prover** | 1 | [`rocq-prover.json`](data/languages/rocq-prover.json) |
| **Smarty** | 1 | [`smarty.json`](data/languages/smarty.json) |
| **SQL** | 1 | [`sql.json`](data/languages/sql.json) |
| **Standard ML** | 1 | [`standard-ml.json`](data/languages/standard-ml.json) |
| **Stata** | 1 | [`stata.json`](data/languages/stata.json) |
| **Tape** | 1 | [`tape.json`](data/languages/tape.json) |
| **Tcl** | 1 | [`tcl.json`](data/languages/tcl.json) |
| **Thrift** | 1 | [`thrift.json`](data/languages/thrift.json) |
| **Typst** | 1 | [`typst.json`](data/languages/typst.json) |
| **Visual Basic 6.0** | 1 | [`visual-basic-6-0.json`](data/languages/visual-basic-6-0.json) |
| **Wikitext** | 1 | [`wikitext.json`](data/languages/wikitext.json) |
| **Wren** | 1 | [`wren.json`](data/languages/wren.json) |
| **XML** | 1 | [`xml.json`](data/languages/xml.json) |
| **ZIL** | 1 | [`zil.json`](data/languages/zil.json) |

## Category index

| Category | Repositories | Dataset |
|---|---:|---|
| **ai** | 2,752 | [`ai.json`](data/categories/ai.json) |
| **web** | 2,054 | [`web.json`](data/categories/web.json) |
| **devops** | 1,238 | [`devops.json`](data/categories/devops.json) |
| **developer-tools** | 915 | [`developer-tools.json`](data/categories/developer-tools.json) |
| **database** | 909 | [`database.json`](data/categories/database.json) |
| **security** | 857 | [`security.json`](data/categories/security.json) |
| **networking** | 501 | [`networking.json`](data/categories/networking.json) |

## Methodology

The default inclusion policy is `stars >= 2000` with no fixed maximum repository count. The collector uses GitHub's official Search API, partitions result ranges when required by GitHub's search limits, normalizes source metadata, applies deterministic RepoSource classifications, validates the dataset, and publishes machine-readable outputs.

## Provenance

RepoSource Registry is a derived public dataset based on GitHub public repository metadata. It is not an official GitHub database and is not a real-time feed. Repository metadata can change between synchronization runs.

Derived fields including categories, popularity bands, and activity status are RepoSource classifications and must not be interpreted as GitHub-provided facts.

## AI-agent consumption

AI agents should start with [`AGENTS.md`](AGENTS.md) and [`llms.txt`](llms.txt), then consume [`data/manifest.json`](data/manifest.json) and [`data/repositories.json`](data/repositories.json). Validate records against the published schema. Do not scrape this README when machine-readable data is available.

## Limitations

Star counts are popularity signals. Search indexing and GitHub API behavior can change. The collector fails closed when it cannot safely establish a complete eligible result set rather than publishing known-incomplete data.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Security issues should follow [`SECURITY.md`](SECURITY.md).

## License

Project code and documentation are MIT licensed. Upstream repository metadata remains subject to GitHub's terms and the respective repositories' licenses.

---

**RepoSource Registry** · Reliable data. Clear provenance. Stable schema. Simple consumption.
