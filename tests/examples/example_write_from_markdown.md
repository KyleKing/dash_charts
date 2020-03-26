# Hello Markdown!

Example writing a Markdown with Plotly figures. Easier to write longer form text than in Python. You can even use the VSCode/Sublime/etc "Markdown TOC" extension:

**Table of Contents**

<!-- TOC -->

- [Hello Markdown!](#hello-markdown)
  - [Plotly-Stuff](#plotly-stuff)
  - [Example Markdown](#example-markdown)
    - [Unordered](#unordered)
    - [Ordered](#ordered)
    - [Images](#images)
  - [Github Flavored Markdown](#github-flavored-markdown)
    - [Task Lists](#task-lists)
    - [Tables](#tables)
    - [Code](#code)

<!-- /TOC -->

## Plotly-Stuff

Plotly Figure

>>lookup:make_div(figure_px)

Bootstrap Table

>>lookup:table(iris_data)

---

## Example Markdown

Experimenting with gfm syntax based on: [Mastering Markdown](https://guides.github.com/features/mastering-markdown/)

It's very easy to make some words **bold** and other words *italic* with Markdown. You can even [link to Google!](http://google.com)

*This text will be italic*

_This will also be italic_

**This text will be bold**

__This will also be bold__

_You **can** combine them_

### Unordered

* Item 1
* Item 2
    * Item 2a  (note: four spaces)
    * Item 2b

### Ordered

1. Item 1
1. Item 2
1. Item 3
    1. Item 3a  (note: four spaces)
        1. Item 3aa
            1. Item 3aaa
                1. Item 3aaaa
    1. Item 3b

### Images

Using alt-text: ![Alt Text](not_a_url)

Actual Image:

![GitHub Logo](https://upload.wikimedia.org/wikipedia/commons/2/29/GitHub_logo_2013.svg)

---

## Github Flavored Markdown

gfm-specific syntax

### Task Lists

- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] list syntax required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item

### Tables

| First Header | Second Header |
| ------------ | ------------- |
| Content from cell 1 | Content from cell 2 |
| Content in the first column | Content in the second column |

### Code

`import markdown`

```
import markdown
```

```py
import markdown
```
