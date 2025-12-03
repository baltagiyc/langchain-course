# 📋 Template : Tool Calling avec la Nouvelle API LangChain

## 🎯 Objectif
Créer un agent qui utilise des tools (outils) pour répondre à des questions, en utilisant la nouvelle API de LangChain (v1.0+).

---

## 📦 Étape 1 : Installation des Bibliothèques

```bash
uv add "langchain>=1.0.2" "langchain-openai>=1.0.1" "python-dotenv>=1.2.1"
```

**Bibliothèques nécessaires :**
- `langchain` : API principale (nouvelle version)
- `langchain-openai` : Intégration OpenAI (supporte tool calling)
- `python-dotenv` : Gestion des variables d'environnement

**Optionnel :**
- `langchain-community` : Tools prédéfinis (Wikipedia, DuckDuckGo, etc.)
- `langchain-tavily` : Tool de recherche Tavily (package séparé)

---

## 🔧 Étape 2 : Créer un Tool Personnalisé

### 2.1 Décorateur `@tool`

```python
from langchain_core.tools import tool

@tool
def nom_de_la_fonction(param1: type, param2: type) -> type_retour:
    """
    Description du tool.
    Le LLM utilise cette description pour décider quand utiliser ce tool.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description de ce qui est retourné
    """
    # Logique de la fonction
    return resultat
```

### 2.2 Exemple Concret

```python
@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y

@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters."""
    text = text.strip("'\n").strip('"')
    return len(text)
```

**Points importants :**
- La docstring devient la description du tool
- Le LLM lit cette description pour décider quel tool utiliser
- Les types sont importants pour la validation

---

## 🛠️ Étape 3 : Utiliser des Tools Prédéfinis

### 3.1 Tools de la Communauté

```python
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ShellTool,
    ReadFileTool
)

tools = [
    DuckDuckGoSearchRun(),
    WikipediaQueryRun(),
    ShellTool(),
    ReadFileTool()
]
```

### 3.2 Tools de Packages Séparés

```python
from langchain_tavily import TavilySearch

tools = [TavilySearch()]
```

**Note :** Tavily a son propre package (`langchain-tavily`) pour une maintenance indépendante.

---

## 🤖 Étape 4 : Créer le LLM

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# OpenAI (supporte tool calling)
llm = ChatOpenAI(
    model="gpt-4o-mini",  # ou "gpt-4", "gpt-4-turbo", etc.
    temperature=0
)

# Anthropic (supporte aussi tool calling)
llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0
)
```

**Points importants :**
- Le LLM doit supporter tool calling (OpenAI, Anthropic, etc.)
- `temperature=0` pour des réponses plus déterministes

---

## 📝 Étape 5 : Créer le Prompt

### 5.1 Prompt Simple (Recommandé)

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # ← Important pour la boucle
])
```

**Explication :**
- `system` : Rôle de l'assistant
- `human` : Question de l'utilisateur
- `placeholder` : Historique des interactions (tool calls, résultats, etc.)

### 5.2 Prompt Personnalisé

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert data scientist. Always explain your reasoning."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
```

---

## 🔗 Étape 6 : Créer l'Agent

### 6.1 Approche Automatique (Recommandée)

```python
from langchain.agents import create_agent, AgentExecutor

# Créer l'agent
agent = create_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)

# Créer l'executor (gère la boucle automatiquement)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # ← Affiche les détails dans la console
)
```

**Avantages :**
- Simple et rapide
- Gestion automatique de la boucle
- Moins de code

### 6.2 Approche Manuelle (Pour Comprendre)

```python
from langchain_core.messages import HumanMessage, ToolMessage

# Lier les tools au LLM
llm_with_tools = llm.bind_tools(tools)

# Boucle manuelle
messages = [HumanMessage(content="Votre question")]

while True:
    # Appeler le LLM
    ai_message = llm_with_tools.invoke(messages)
    
    # Vérifier si le LLM veut utiliser un tool
    tool_calls = getattr(ai_message, "tool_calls", None) or []
    
    if len(tool_calls) > 0:
        # Ajouter le message du LLM
        messages.append(ai_message)
        
        # Exécuter chaque tool
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})
            tool_call_id = tool_call.get("id")
            
            # Trouver et exécuter le tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            observation = tool_to_use.invoke(tool_args)
            
            # Ajouter le résultat comme ToolMessage
            messages.append(
                ToolMessage(
                    content=str(observation),
                    tool_call_id=tool_call_id
                )
            )
        
        # Continuer la boucle pour que le LLM utilise les résultats
        continue
    
    # Pas de tool calls → réponse finale
    print(ai_message.content)
    break
```

**Avantages :**
- Compréhension complète du mécanisme
- Contrôle total sur chaque étape
- Utile pour apprendre

---

## 🚀 Étape 7 : Exécuter l'Agent

### 7.1 Avec AgentExecutor (Automatique)

```python
resultat = agent_executor.invoke({
    "input": "Quelle est la météo à Paris ? Calcule 10 * 20"
})

print(resultat["output"])
```

### 7.2 Avec Boucle Manuelle

```python
# Déjà fait dans l'étape 6.2
# Le résultat est dans ai_message.content
```

---

## 📊 Flux Complet : De la Question à la Réponse

### Flux Automatique (AgentExecutor)

```
1. Question utilisateur
   ↓
2. create_agent() crée l'agent avec tools
   ↓
3. AgentExecutor.invoke() démarre
   ↓
4. LLM reçoit la question + descriptions des tools
   ↓
5. LLM décide d'utiliser un tool (tool calling natif)
   ↓
6. AgentExecutor exécute le tool automatiquement
   ↓
7. AgentExecutor renvoie le résultat au LLM
   ↓
8. LLM génère la réponse finale (ou utilise un autre tool)
   ↓
9. AgentExecutor retourne la réponse finale
```

### Flux Manuel (bind_tools)

```
1. llm.bind_tools(tools) → Lie les tools au LLM
   ↓
2. llm.invoke(messages) → LLM génère un tool call
   ↓
3. Vérifier tool_calls dans ai_message
   ↓
4. Si tool_calls existent :
   - Exécuter le tool manuellement
   - Créer ToolMessage avec le résultat
   - Ajouter à messages
   - Revenir à l'étape 2
   ↓
5. Si pas de tool_calls :
   - Afficher ai_message.content (réponse finale)
```

---

## 🔍 Points Clés à Retenir

### 1. Tool Calling vs ReAct

| Aspect | Tool Calling (Nouvelle API) | ReAct (Ancienne API) |
|--------|----------------------------|---------------------|
| **Format** | Function calls structurés | Texte (Action: ...) |
| **Parsing** | Automatique (natif) | Regex (manuel) |
| **Visibilité** | Moins visible | Très visible |
| **Performance** | Plus rapide | Plus lent |
| **Complexité** | Simple | Complexe |

### 2. Différence entre `bind_tools` et `create_agent`

- **`bind_tools`** : Lie les tools au LLM, mais vous gérez la boucle manuellement
- **`create_agent`** : Crée un agent complet qui gère tout automatiquement

### 3. AgentExecutor

- Gère la boucle automatiquement
- Exécute les tools automatiquement
- Ajoute les ToolMessage automatiquement
- Continue jusqu'à obtenir une réponse finale

### 4. Descriptions des Tools

- **Cruciales** : Le LLM les lit pour décider quel tool utiliser
- **Format** : Docstring de la fonction
- **Contenu** : Explique QUAND et COMMENT utiliser le tool

---

## 📝 Checklist de Création

- [ ] Installer les bibliothèques (`langchain`, `langchain-openai`, etc.)
- [ ] Créer les tools (personnalisés ou prédéfinis)
- [ ] Créer le LLM (ChatOpenAI, ChatAnthropic, etc.)
- [ ] Créer le prompt (ChatPromptTemplate)
- [ ] Créer l'agent (`create_agent` ou `bind_tools`)
- [ ] Créer l'executor (`AgentExecutor` si approche automatique)
- [ ] Exécuter (`invoke()`)
- [ ] Afficher le résultat

---

## 🎓 Exemple Complet

```python
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

# 1. Créer un tool personnalisé
@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y

# 2. Créer le LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Créer le prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Créer la liste des tools
tools = [multiply, TavilySearch()]

# 5. Créer l'agent
agent = create_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)

# 6. Créer l'executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# 7. Exécuter
resultat = agent_executor.invoke({
    "input": "Quelle est la météo à Paris ? Calcule 10 * 20"
})

print(resultat["output"])
```

---

## 🐛 Debugging

### Voir ce qui se passe

```python
# Option 1 : verbose=True
agent_executor = AgentExecutor(..., verbose=True)

# Option 2 : Callbacks personnalisés
from langchain_core.callbacks import BaseCallbackHandler

class MonCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str):
        print(f"🔧 Tool {serialized['name']} démarre")
    
    def on_tool_end(self, output):
        print(f"✅ Tool terminé: {output}")

agent_executor = AgentExecutor(
    ...,
    callbacks=[MonCallback()]
)
```

### LangSmith

- Les traces sont automatiquement envoyées à LangSmith
- Vous pouvez voir les tool calls dans l'interface
- Utile pour comprendre le flux d'exécution

---

## 📚 Résumé

**Nouvelle API = Tool Calling Natif**

1. **Créer les tools** → `@tool` ou tools prédéfinis
2. **Créer le LLM** → `ChatOpenAI` (supporte tool calling)
3. **Créer le prompt** → `ChatPromptTemplate`
4. **Créer l'agent** → `create_agent()` ou `bind_tools()`
5. **Exécuter** → `AgentExecutor.invoke()` ou boucle manuelle

**Avantages :**
- Plus simple que ReAct
- Plus rapide (moins de tokens)
- Plus robuste (pas de parsing texte)
- Moins de code

**Inconvénients :**
- Moins transparent (tool calling caché)
- Moins de contrôle fin
- Nécessite un LLM qui supporte tool calling

---

**Bon apprentissage ! 🚀**

