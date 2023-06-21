# SimpleAIChat Plugin

This is a ChatGPT plugin that uses the SimpleAIChat Python package to generate responses. It's designed to work in conjunction with the ChatGPT plugins system.

## Setup Locally

---

See steps in [plugins-quickstart](https://github.com/openai/plugins-quickstart#setup-locally.) but instead enter in `localhost:5000` for the local URL and port.

The plugin should now be installed and enabled! You can start with a question like "What is the weather like today?" and the SimpleAIChat plugin will generate a response.

## Directory Structure

---

```shell
simpleaichat_plugin/
├── .well-known/
│   └── ai-plugin.json
├── main.py
├── openapi.yaml
└── requirements.txt
```

## To-Do List

---

1. Create the directory structure.
2. Write the ai-plugin.json file.
3. Write the openapi.yaml file.
4. Write the main.py file.
5. Write the requirements.txt file.

## Files
---

### .well-known/ai-plugin.json
```json
{
  "schema_version": "v1",
  "name_for_human": "SimpleAIChat Plugin",
  "name_for_model": "simpleaichat",
  "description_for_human": "A plugin that uses the SimpleAIChat Python package to generate responses.",
  "description_for_model": "Plugin for generating responses using the SimpleAIChat Python package.",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "http://localhost:5000/openapi.yaml"
  }
}
```

### openapi.yaml
```yaml
openapi: 3.0.1
info:
  title: SimpleAIChat Plugin
  description: A plugin that uses the SimpleAIChat Python package to generate responses.
  version: 'v1'
servers:
  - url: http://localhost:5000
paths:
  /chat:
    post:
      operationId: chat
      summary: Generate a response using the SimpleAIChat Python package.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: The query to generate a response for.
              required:
                - query
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  response:
                    type: string
                    description: The generated response.

```

### main.py
```python
import quart
from quart import request, jsonify
from simpleaichat import AIChat

app = quart.Quart(__name__)

@app.route('/chat', methods=['POST'])
async def chat():
    data = await request.get_json()
    query = data.get('query')
    ai = AIChat(console=False)
    response = ai(query)
    return jsonify({'response': response})

@app.route('/.well-known/ai-plugin.json')
async def plugin_manifest():
    with open('./.well-known/ai-plugin.json') as f:
        return f.read(), {'Content-Type': 'application/json'}

@app.route('/openapi.yaml')
async def openapi_spec():
    with open('openapi.yaml') as f:
        return f.read(), {'Content-Type': 'text/yaml'}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

```

### requirements.txt
```text
quart
simpleaichat
```

Please note that you'll need to replace the simpleaichat package in the requirements.txt file with the correct package name if it's different. Also, the openapi.yaml file and the ai-plugin.json file should contain the correct URLs and other details specific to your plugin.


