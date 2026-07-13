'''
Knowledge Base
Provides domain specific knowledge to AI agents.

Responsiblities:
1. Load knowledge from JSON files
2. Retrieve the knowledge based on a search key.
3. Hide the underlying data source from AI agents
4. Prepare the project for future RAG implementation
'''

import json
from pathlib import Path
from typing import Any

class KnowledgeBase:
   '''
   Loads and manages domain specific knowledge
   Currently, knowledge is loaded from a JSON file.
   Later the implementeation can be replaced with a vector DB
   '''

   def __init__(self, knowledge_file: str) -> None:
      self._knowledge = self._load_knowledge(knowledge_file)
   
   def _load_knowledge(self, knowledge_file: str) -> dict[str, Any]:
      '''
      Load knowledge from a JSON file
      Args:
        knowledge_file: JSON file path
      Returns:
        Dictionary containing knowledge
      '''

      file_path = Path(knowledge_file)
      if not file_path.exists():
         raise FileNotFoundError(f"Knowledge file not found: {knowledge_file}")
      
      with open(file_path, 'r', encoding='utf-8') as file:
         return json.load(file)

   def get(self, key:str) -> Any:
      '''
      Retrieve knowledge for a given key
      Args:
        key: knowledge key.
      Returns:
        Matching knowledge or None
    '''
      return self._knowledge.get(key)
   
   def retrieve(self, query: str) -> dict:
      query = query.lower()
      for key, value in self._knowledge.items():
         if key.lower().replace("_", " ") in query:
            return value
         
      return {}
   
   def get_all(self) -> dict[str, Any]:
      '''
      Return the complete knowledge base
      '''
      return self._knowledge
   
   def exists(self, key: str) -> bool:
      '''
      Check whether a key exisits
      Args:
        key: knowledge key
      return:
        True if present
      '''
      return key in self._knowledge
   
   def display(self) -> None:
      '''
      Display all available knowledge key
      '''

      print("\n" * "=" * 60)
      print("KNOWLEDGE BASE")
      print("\n" * "=" * 60)

      if not key in self._knowledge.keys():
         print("Knowledge base is empty")

      for key in self._knowledge.keys():
         print(f"- {key}")

      print("\n" * "=" * 60)
