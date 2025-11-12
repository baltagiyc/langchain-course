# 📚 Récapitulatif LangChain - Premier Cours

## Table des matières
1. [Concepts Fondamentaux](#concepts-fondamentaux)
2. [Templates et Prompts](#templates-et-prompts)
3. [Chaînes (Chains)](#chaînes-chains)
4. [LLMs et Modèles](#llms-et-modèles)
5. [Variables d'Environnement](#variables-denvironnement)
6. [Exercices Pratiques](#exercices-pratiques)
7. [Outils et Écosystème](#outils-et-écosystème)
8. [Erreurs Communes](#erreurs-communes)

---

## Concepts Fondamentaux

### Qu'est-ce que LangChain ?
LangChain est un framework Python pour construire des applications avec des LLM (Large Language Models).

**Avantages :**
- Abstraction des différents fournisseurs (OpenAI, Groq, Ollama, etc.)
- Chaînage de composants (prompts, LLMs, outils)
- Gestion d'état et mémoire
- Intégration avec de nombreux outils

### Structure de base
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Créer un LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Créer un template
template = ChatPromptTemplate.from_template("Réponds à : {question}")

# 3. Créer une chaîne
chain = template | llm

# 4. Invoquer la chaîne
response = chain.invoke({"question": "Qu'est-ce que Python ?"})
print(response.content)
```

---

## Templates et Prompts

### ChatPromptTemplate

**Définition :** Un template est un "moule" avec des variables à remplir.

```python
from langchain_core.prompts import ChatPromptTemplate

# Template avec variable
template = ChatPromptTemplate.from_template(
    "Résume ce texte : {texte}"
)

# Template sans variable
simple_template = ChatPromptTemplate.from_template(
    "Explique-moi le machine learning"
)
```

### ⚠️ IMPORTANT : Template vs Prompt invoqué

**❌ MAUVAIS :**
```python
template = ChatPromptTemplate.from_template("Résume : {texte}")
prompt_rempli = template.invoke({"texte": "..."})  # ❌ Déjà rempli !
chain = prompt_rempli | llm  # ❌ ERREUR ! On ne peut pas chaîner un résultat
```

**✅ BON :**
```python
template = ChatPromptTemplate.from_template("Résume : {texte}")
chain = template | llm  # ✅ On chaîne le template (vide)
response = chain.invoke({"texte": "..."})  # ✅ On remplit au moment de l'invocation
```

**Analogie :**
- **Template** = Formulaire vide (réutilisable)
- **Prompt invoqué** = Formulaire rempli (résultat final)
- **Règle :** On chaîne les templates, pas les résultats !

---

## Chaînes (Chains)

### Création d'une chaîne

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Étape 1 : Créer le template
template = ChatPromptTemplate.from_template("Réponds à : {question}")

# Étape 2 : Créer le LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Étape 3 : Chaîner avec l'opérateur |
chain = template | llm

# Étape 4 : Invoquer avec les données
response = chain.invoke({"question": "Qu'est-ce que Python ?"})
```

### Invocation selon le template

| Template | `.invoke()` |
|----------|-------------|
| `"Résume : {texte}"` | `chain.invoke({"texte": "..."})` |
| `"Réponds : {query}"` | `chain.invoke({"query": "..."})` |
| `"Explique Python"` (sans variables) | `chain.invoke({})` |

### Chaîne directe (sans template)

```python
# Si vous voulez juste envoyer une query simple
llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke("Qu'est-ce que Python ?")
# OU
response = llm.invoke([("user", "Qu'est-ce que Python ?")])
```

---

## LLMs et Modèles

### OpenAI (ChatOpenAI)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",  # Modèle à utiliser
    temperature=0,        # 0 = déterministe, 1 = créatif
    api_key="sk-..."      # Optionnel si dans .env
)
```

### Groq (ChatGroq)

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.7
)
```

**Avantages Groq :**
- ⚡ Très rapide (10-100x plus rapide qu'OpenAI)
- 💰 Moins cher
- 🔓 Modèles open source (Llama, Mixtral)

### Paramètres importants

- **`temperature`** : 
  - `0` = Réponses déterministes, factuelles
  - `0.3-0.7` = Équilibre créativité/précision
  - `> 0.8` = Très créatif, moins prévisible

- **`model`** : Nom du modèle (doit correspondre exactement)

---

## Variables d'Environnement

### Configuration avec .env (Recommandé)

**Fichier `.env` :**
```bash
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk-...
```

**Code :**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Charge automatiquement le .env

# Les clés sont maintenant disponibles
api_key = os.environ.get("OPENAI_API_KEY")
```

### Configuration manuelle (pour exercices)

```python
import os

def set_api_key(api_key):
    """Définit une variable d'environnement."""
    os.environ["GROQ_API_KEY"] = api_key

# Utilisation
set_api_key("gsk-...")
```

### Vérification

```python
def check_api_key():
    if "GROQ_API_KEY" not in os.environ:
        raise Exception("GROQ_API_KEY not set")
```

---

## Exercices Pratiques

### Exercice 1 : Premier Prompt avec Template

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Données
informations = "Lionel Messi est un footballeur argentin..."

# Template avec variable
summary_template = """
Give me a short summary of: {informations}
and give 2 facts
"""

# Créer le template
summary_prompt_template = ChatPromptTemplate.from_template(summary_template)

# Créer le LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Créer la chaîne
chain = summary_prompt_template | llm

# Invoquer
response = chain.invoke({"informations": informations})
print(response.content)
```

### Exercice 2 : Gestion de Clés API

```python
import os

def implement_set_api_key(api_key):
    """Définit la variable d'environnement GROQ_API_KEY."""
    os.environ["GROQ_API_KEY"] = api_key

def check_api_key():
    """Vérifie si la clé API est définie."""
    if "GROQ_API_KEY" not in os.environ:
        raise Exception("GROQ_API_KEY environment variable is required")

# Utilisation
implement_set_api_key("gsk-...")
check_api_key()
```

### Exercice 3 : Changement de Modèle

```python
from langchain_groq import ChatGroq

def create_llama_4_model():
    """Crée un modèle Llama 4."""
    return ChatGroq("llama-4-8b-instant", temperature=0)

def create_llama_3_3_model():
    """Crée un modèle Llama 3.3 (plus créatif)."""
    return ChatGroq("llama-3.3-70b-versatile", temperature=0.3)

# Utilisation
llm1 = create_llama_4_model()
llm2 = create_llama_3_3_model()
```

### Exercice 4 : Comparaison de Modèles

```python
def compare_models(prompt):
    """Compare deux modèles avec le même prompt."""
    results = {}
    
    # Modèle 1
    llm1 = ChatGroq("llama-4-8b-instant", temperature=0)
    response1 = llm1.invoke([("user", prompt)])
    results["llama_4"] = response1.content
    
    # Modèle 2
    llm2 = ChatGroq("llama-3.3-70b-versatile", temperature=0.3)
    response2 = llm2.invoke([("user", prompt)])
    results["llama_3_3"] = response2.content
    
    return results

# Utilisation
comparison = compare_models("Explain machine learning")
print(comparison)
```

---

## Outils et Écosystème

### LangSmith (Monitoring)

**Qu'est-ce que c'est ?**
- Plateforme SaaS de monitoring pour applications LLM
- Traçage, évaluation, debugging
- Propriétaire (payant)

**Utilisation :**
```python
from langsmith import traceable

@traceable
def my_chain():
    llm = ChatOpenAI()
    return llm.invoke("Hello")
```

### Langfuse (Monitoring Open Source)

**Qu'est-ce que c'est ?**
- Alternative open source à LangSmith
- Self-hostable (gratuit)
- Même fonctionnalités de base

**Comparaison :**
| Critère | LangSmith | Langfuse |
|---------|-----------|----------|
| Open Source | ❌ | ✅ |
| Self-hosted | ❌ | ✅ |
| Gratuit | ⚠️ Limité | ✅ |
| Intégration LangChain | ✅ Excellente | ✅ Bonne |

### LangGraph (Workflows)

**Qu'est-ce que c'est ?**
- Framework pour créer des workflows complexes
- Gestion d'état, boucles, branches
- Pour agents et applications complexes

**Différence :**
- **LangChain** = Composants de base
- **LangGraph** = Workflows complexes avec état

### Groq vs OpenAI

| Critère | Groq | OpenAI |
|---------|-----|--------|
| Vitesse | ⚡ Très rapide | 🐢 Moyenne |
| Coût | 💰 Moins cher | 💰💰 Plus cher |
| Modèles | 🔓 Open source | 🔒 Propriétaires |
| Qualité | ✅ Bonne | ✅✅ Excellente |

---

## Erreurs Communes

### Erreur 1 : Chaîner un prompt invoqué

**❌ MAUVAIS :**
```python
template = ChatPromptTemplate.from_template("Résume : {texte}")
prompt_rempli = template.invoke({"texte": "..."})
chain = prompt_rempli | llm  # ❌ ERREUR !
```

**✅ BON :**
```python
template = ChatPromptTemplate.from_template("Résume : {texte}")
chain = template | llm  # ✅ Chaîner le template
response = chain.invoke({"texte": "..."})
```

### Erreur 2 : Oublier le return

**❌ MAUVAIS :**
```python
def create_model():
    llm = ChatGroq("llama-4-8b-instant")
    # ❌ Pas de return !
```

**✅ BON :**
```python
def create_model():
    llm = ChatGroq("llama-4-8b-instant")
    return llm  # ✅ Retourner le modèle
```

### Erreur 3 : Mauvais format d'invocation

**❌ MAUVAIS :**
```python
# Si template a {query}, mais vous passez autre chose
chain.invoke({"question": "..."})  # ❌ Variable doit être "query"
```

**✅ BON :**
```python
# Les noms de variables doivent correspondre
chain.invoke({"query": "..."})  # ✅ Nom correct
```

### Erreur 4 : Template sans variables

**❌ MAUVAIS :**
```python
template = ChatPromptTemplate.from_template("Explique Python")
chain = template | llm
response = chain.invoke({"texte": "..."})  # ❌ Pas de variable dans le template !
```

**✅ BON :**
```python
template = ChatPromptTemplate.from_template("Explique Python")
chain = template | llm
response = chain.invoke({})  # ✅ Dictionnaire vide
```

---

## Checklist de Mémorisation

### ✅ Concepts à retenir

- [ ] **Template** = Formulaire vide, réutilisable
- [ ] **Prompt invoqué** = Formulaire rempli, résultat final
- [ ] **Chaîne** = Template | LLM (avec l'opérateur `|`)
- [ ] **Invocation** = `chain.invoke({"variable": valeur})`
- [ ] **Temperature** = 0 (factuel) à 1 (créatif)
- [ ] **Variables d'env** = `os.environ["KEY"] = value`

### ✅ Patterns de code

- [ ] Créer un template : `ChatPromptTemplate.from_template("...")`
- [ ] Créer un LLM : `ChatOpenAI(model="...")`
- [ ] Créer une chaîne : `template | llm`
- [ ] Invoquer : `chain.invoke({"var": value})`
- [ ] Accéder au contenu : `response.content`

### ✅ Bonnes pratiques

- [ ] Utiliser `.env` pour les clés API
- [ ] Chaîner les templates, pas les prompts invoqués
- [ ] Toujours retourner les objets créés dans les fonctions
- [ ] Vérifier les noms de variables dans les templates

---

## Résumé Visuel

```
Template (vide)
    ↓ | LLM
Chaîne (vide → LLM)
    ↓ .invoke({"variable": valeur})
    ↓ (Template remplit automatiquement)
    ↓ (Passe au LLM)
Réponse (avec .content)
```

**Règle d'or :**
> On chaîne les machines (templates), on invoque les chaînes complètes !

---

## Prochaines Étapes

1. **RAG (Retrieval Augmented Generation)** : Ajouter des documents
2. **Agents** : Créer des agents qui utilisent des outils
3. **Memory** : Gérer la mémoire conversationnelle
4. **Streaming** : Réponses en temps réel
5. **Embeddings** : Vecteurs pour la recherche sémantique

---

**Bon courage pour la suite ! 🚀**

