#%%
from dotenv import load_dotenv
load_dotenv()
import os
from typing import Any, Dict, List, Optional, Union, Callable

from simpleaichat import AIChat
from simpleaichat.utils import wikipedia_search, wikipedia_search_lookup

# This uses the Wikipedia Search API.
# Results from it are nondeterministic, your mileage will vary.
def search(query: str) -> Dict[str, Union[str, List[str]]]:
    """Search the internet."""
    wiki_matches: List[str] = wikipedia_search(query, n=3)
    return {"context": ", ".join(wiki_matches), "titles": wiki_matches}

def lookup(query: str) -> str:
    """Lookup more information about a topic."""
    page = wikipedia_search_lookup(query, sentences=3)
    return page


_BASE_TOOLS = {
    "search": search,
    "lookup": lookup,
}

def get_all_tool_names() -> List[str]:
    """Get a list of all possible tool names."""
    return list(_BASE_TOOLS)

def load_tools(tool_names: List[str] = None) -> List[Any]:
    """Load the tools."""
    if tool_names is None:
        tool_names = get_all_tool_names()
    tools: List[Any] = []
    for name in tool_names:
        if name in _BASE_TOOLS:
            tools.append(_BASE_TOOLS[name])
    return tools
