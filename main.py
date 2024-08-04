import io
import autopep8
from fasthtml.common import (
    fast_app, serve,
    Form, Textarea, Button, Titled, Div, H1, H2, Pre, Script, Link, Code,
)


app,rt = fast_app(
    hdrs=[
        Script(src="https://cdn.tailwindcss.com"),
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"),
        Script("hljs.highlightAll();"),
    ],
)

def CodeInput(source: str):
    return Form(
        Textarea(source, id="source", name="source", placeholder="Input Python Code", rows="40", cols="50"),
        Button("Submit", cls="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        action="/", method="post",
    )

def Content(source: str, formatted: str):
    input_python_code = CodeInput(source)
    content = Div(
        Div(H2("input", cls="text-lg font-bold"), input_python_code),
        Div(H2("Formatted", cls="text-lg font-bold"), Pre(Code(formatted, cls="language-diff"))),
        cls="grid grid-cols-2 gap-4",
    )
    return Titled(H1("autopep8", cls="text-2xl font-bold"), content)

@rt('/')
def get():
    return Content(source="", formatted="")

@rt('/')
def post(source: str):
    configuration = {
        "max_line_length": 120,
        "ignore": set(autopep8.DEFAULT_IGNORE.split(",")),
        "diff": True,
    }
    formatted = autopep8.fix_code(source, configuration)
    old = io.StringIO(source)
    old = old.readlines()
    new = io.StringIO(formatted)
    new = new.readlines()
    formatted = autopep8.get_diff_text(old, new, "")
    return Content(source, formatted)


serve()
