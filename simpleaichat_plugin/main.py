import quart
import quart_cors
from quart import request, jsonify
from simpleaichat import AIChat
from tools import load_tools
from typing import Any, Dict, List, Optional, Union

import json
import pprint as pp
from pprint import PrettyPrinter, pprint, pformat
pprint = pp.PrettyPrinter(sort_dicts=False).pprint
pformat = pp.PrettyPrinter(sort_dicts=False).pformat

from rich.console import Console
console = Console()

def pretty_print(json_object):
    print(json.dumps(json_object, indent=2, sort_keys=False, default=pformat))

def console_print(*objects: Any, title=None, title_color="bold white", sep="\n\n", **kwargs: Any) -> None:
    title = f"{objects[0].__class__.__name__}:" if title is None else title # if inspect.isclass(obj) else title
    title = f"[{title_color}]{title}[/{title_color}]" if title_color is not None else title
    console.print(title, *objects, sep="\n\n", **kwargs)

def print_ai(ai: AIChat, default=repr):
    for i, (key, val) in enumerate(zip(ai.sessions.keys(), ai.sessions.values())):
        console_print(val, title=f"{val.__repr_name__()} {i}: {default(key)}")


TOOL_NAMES = [
    "search",
    "lookup"
]

TOOLS = load_tools(TOOL_NAMES)

PARAMS = {
    "temperature": 0.0,
    "max_tokens": 100
}
AI_CHAT_ID = "simpleaichat-plugin"

AI = AIChat(params=PARAMS, console=False, id=AI_CHAT_ID)
print_ai(AI)

# Create a Quart application with CORS enabled
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.route('/chat', methods=['POST'])
async def chat():
    global AI
    data = await request.get_json()
    query = data.get('query')
    # Create AIChat instance
    response = AI(query, tools=TOOLS, id=AI_CHAT_ID)
    console_print(response, title=f"Response: \"{query}\"")
    print_ai(AI)
    return jsonify({'response': response})

@app.route('/.well-known/ai-plugin.json')
async def plugin_manifest():
    with open('./.well-known/ai-plugin.json') as f:
        return f.read(), {'Content-Type': 'application/json'}

@app.route('/openapi.yaml')
async def openapi_spec():
    with open('openapi.yaml') as f:
        return f.read(), {'Content-Type': 'text/yaml'}

@app.get("/logo.png")
async def plugin_logo():
    """ GET requests for the plugin's logo. """
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

def main():
    """ Start the Quart server.
    """
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=5000)
    main()
