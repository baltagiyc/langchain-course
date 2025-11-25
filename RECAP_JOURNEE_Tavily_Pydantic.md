# 📚 Récapitulatif du Jour : Tavily & Pydantic

## Table des matières
1. [Tavily - Recherche Web](#tavily---recherche-web)
2. [Pydantic - Validation de Données](#pydantic---validation-de-données)
3. [Agents LangChain avec Outils](#agents-langchain-avec-outils)
4. [Concepts Clés](#concepts-clés)

---

## Tavily - Recherche Web

### Qu'est-ce que Tavily ?
Tavily est un service API qui permet de faire des recherches web intelligentes et d'extraire du contenu depuis des URLs.

### Installation et Configuration

```python
from tavily import TavilyClient
import os

# Configuration
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
```

### Fonctionnalités Principales

#### 1. Recherche Web (`search`)

```python
# Recherche simple
results = tavily.search("freelance AI jobs France")

# Retourne :
# - Des résultats de recherche pertinents
# - Des URLs sources
# - Du contenu extrait
# - Des scores de pertinence
```

**Utilisation dans LangChain :**
```python
from langchain_tavily import TavilySearch

# Intégration directe avec LangChain
tool = TavilySearch()
tools = [tool]
```

#### 2. Extraction d'URL (`extract`)

```python
# Extraire le contenu d'une URL spécifique
result = tavily.extract(url="https://example.com/article")

# Retourne le contenu nettoyé de la page
```

### Scraping avec Tavily

**C'est du scraping ?** Oui, Tavily fait du scraping pour vous.

**Avantages :**
- ✅ Gère automatiquement `robots.txt`
- ✅ Gère le rate limiting
- ✅ User-Agent approprié
- ✅ Gestion des erreurs

**Limitations :**
- ❌ Sites protégés (login, cookies)
- ❌ JavaScript complexe (contenu dynamique)
- ❌ CAPTCHA
- ❌ Paywalls

**Gouvernance :**
- Tavily respecte les règles des sites
- Vous devez respecter la légalité et les conditions d'utilisation
- Attention au RGPD si données personnelles

### Exemple Complet

```python
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Créer l'outil Tavily
tavily_tool = TavilySearch()

# Créer l'agent
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(model=llm, tools=[tavily_tool])

# Utiliser l'agent
result = agent.invoke({
    "messages": [HumanMessage(content="Trouve des offres d'emploi AI en France")]
})
```

---

## Pydantic - Validation de Données

### Qu'est-ce que Pydantic ?
Pydantic est une bibliothèque Python pour la validation de données et la création de modèles avec validation automatique.

### Concepts de Base

#### 1. Créer un Modèle

```python
from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    """Modèle pour une source"""
    url: str = Field(description="L'URL de la source")

class AgentResponse(BaseModel):
    """Modèle pour la réponse de l'agent"""
    answer: str = Field(description="La réponse à la question")
    sources: List[Source] = Field(
        default_factory=list, 
        description="Les sources utilisées"
    )
```

#### 2. Field et ses Paramètres

**`description`** : Description du champ (pour la documentation)
```python
url: str = Field(description="L'URL de la source")
```

**`default`** : Valeur par défaut (pour types immutables)
```python
name: str = Field(default="Unknown")
age: int = Field(default=0)
```

**`default_factory`** : Fonction qui crée la valeur par défaut (pour types mutables)
```python
sources: List[Source] = Field(default_factory=list)
tags: List[str] = Field(default_factory=list)
metadata: Dict[str, str] = Field(default_factory=dict)
```

### ⚠️ IMPORTANT : `default` vs `default_factory`

#### Le Piège Python

**❌ MAUVAIS :**
```python
class Panier(BaseModel):
    fruits: List[str] = Field(default=[])  # ❌ PIÈGE !

# Problème : Tous les objets partagent la même liste !
panier1 = Panier()
panier2 = Panier()
panier1.fruits.append("pomme")
# ❌ panier2.fruits contient aussi "pomme" !
```

**✅ BON :**
```python
class Panier(BaseModel):
    fruits: List[str] = Field(default_factory=list)  # ✅

# Solution : Chaque objet a sa propre liste
panier1 = Panier()
panier2 = Panier()
panier1.fruits.append("pomme")
# ✅ panier2.fruits est toujours vide
```

**Règle d'or :**
- **Types immutables** (str, int, bool) → `default="valeur"`
- **Types mutables** (list, dict, set) → `default_factory=list`

### Utilisation des Modèles

```python
# Créer une instance
response = AgentResponse(
    answer="Voici la réponse...",
    sources=[
        Source(url="https://example.com"),
        Source(url="https://example2.com")
    ]
)

# Accéder aux champs
print(response.answer)
print(response.sources[0].url)

# Validation automatique
# Si vous passez un mauvais type, Pydantic lève une erreur
```

### Validation Automatique

```python
# ✅ Valide
response = AgentResponse(answer="Test", sources=[])

# ❌ Erreur de validation
response = AgentResponse(answer=123)  # answer doit être str
response = AgentResponse(sources="not a list")  # sources doit être List
```

---

## Agents LangChain avec Outils

### Structure d'un Agent

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# 1. Créer le LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Créer les outils
tools = [TavilySearch()]

# 3. Créer l'agent
agent = create_agent(model=llm, tools=tools)

# 4. Utiliser l'agent
result = agent.invoke({
    "messages": [HumanMessage(content="Votre question")]
})
```

### Créer un Outil Personnalisé

```python
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """
    Search the web for information
    
    Args:
        query: The query to search for
        
    Returns:
        The search results
    """
    print(f"Searching the web for {query}")
    return tavily.search(query)

# Utiliser dans l'agent
tools = [search]
agent = create_agent(model=llm, tools=tools)
```

### Format d'Invocation

**✅ CORRECT :**
```python
from langchain_core.messages import HumanMessage

result = agent.invoke({
    "messages": [HumanMessage(content="Votre question")]
})
```

**❌ INCORRECT :**
```python
# Ne fonctionne pas
result = agent.invoke({"input": "Votre question"})
```

---

## Concepts Clés

### 1. Tavily
- **Recherche web** : `tavily.search(query)`
- **Extraction URL** : `tavily.extract(url)`
- **Intégration LangChain** : `TavilySearch()`
- **Scraping** : Oui, mais géré par Tavily

### 2. Pydantic
- **BaseModel** : Classe de base pour les modèles
- **Field** : Définit un champ avec description/validation
- **default** : Pour types immutables
- **default_factory** : Pour types mutables (list, dict)
- **Validation automatique** : Pydantic valide les types

### 3. Agents
- **create_agent** : Crée un agent avec LLM + outils
- **@tool** : Décorateur pour créer des outils
- **Invocation** : Format `{"messages": [HumanMessage(...)]}`

### 4. Erreurs Communes Résolues

1. **Import `tool`** :
   - ❌ `from langchain.agents import tool`
   - ✅ `from langchain_core.tools import tool`

2. **Modèle inexistant** :
   - ❌ `model="gpt-5"`
   - ✅ `model="gpt-4o-mini"`

3. **Format d'invocation** :
   - ❌ `{"input": "..."}`
   - ✅ `{"messages": [HumanMessage(...)]}`

4. **Liste partagée** :
   - ❌ `Field(default=[])`
   - ✅ `Field(default_factory=list)`

---

## Exemple Complet du Jour

```python
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

# Modèle Pydantic
class Source(BaseModel):
    url: str = Field(description="L'URL de la source")

class AgentResponse(BaseModel):
    answer: str = Field(description="La réponse")
    sources: List[Source] = Field(
        default_factory=list,  # ✅ default_factory pour liste
        description="Les sources"
    )

# Créer l'agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

# Utiliser l'agent
def main():
    result = agent.invoke({
        "messages": [HumanMessage(content="Trouve des offres d'emploi AI en France")]
    })
    print(result)

if __name__ == "__main__":
    main()
```

---

## Checklist de Mémorisation

### Tavily
- [ ] Tavily fait de la recherche web intelligente
- [ ] `TavilySearch()` s'intègre directement avec LangChain
- [ ] Tavily gère le scraping pour vous (robots.txt, rate limiting)
- [ ] Limitations : sites protégés, JavaScript complexe

### Pydantic
- [ ] `BaseModel` pour créer des modèles
- [ ] `Field()` pour définir les champs
- [ ] `default` pour types immutables (str, int)
- [ ] `default_factory` pour types mutables (list, dict)
- [ ] Validation automatique des types

### Agents
- [ ] `create_agent(model=llm, tools=tools)`
- [ ] `@tool` pour créer des outils personnalisés
- [ ] Format d'invocation : `{"messages": [HumanMessage(...)]}`

---

**Bon travail aujourd'hui ! 🎉**

