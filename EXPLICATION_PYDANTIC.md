# 🎯 Pydantic : Structurer et Valider les Données

## Qu'est-ce que Pydantic ?

**Pydantic = Bibliothèque Python pour structurer et valider des données**

Imaginez que vous avez une fonction qui retourne des données, mais vous voulez être sûr que :
- Les types sont corrects (string, int, etc.)
- Les données sont valides
- La structure est toujours la même

**C'est exactement ce que fait Pydantic !**

---

## BaseModel : Le Fondement

### Concept Simple

`BaseModel` = Un "moule" pour vos données

**Analogie :** C'est comme un formulaire avec des cases à remplir. Chaque case a un type précis.

### Exemple Basique

```python
from pydantic import BaseModel

# Définir le "moule"
class Personne(BaseModel):
    nom: str
    age: int
    email: str

# Créer une instance (remplir le formulaire)
personne = Personne(
    nom="Jean",
    age=30,
    email="jean@example.com"
)

# Accéder aux données
print(personne.nom)   # "Jean"
print(personne.age)    # 30
```

### Validation Automatique

```python
# ✅ Valide
personne = Personne(nom="Jean", age=30, email="jean@example.com")

# ❌ Erreur : age doit être un int
personne = Personne(nom="Jean", age="trente", email="jean@example.com")
# ValidationError: age must be an integer

# ❌ Erreur : champ manquant
personne = Personne(nom="Jean", age=30)
# ValidationError: email field required
```

**Avantage :** Pydantic vérifie automatiquement que les données sont correctes !

---

## Field : Définir les Détails

### Qu'est-ce que Field ?

`Field()` = Des instructions supplémentaires pour chaque champ

**Exemple :**
```python
from pydantic import BaseModel, Field

class Personne(BaseModel):
    nom: str = Field(description="Le nom de la personne")
    age: int = Field(description="L'âge de la personne", ge=0, le=150)
    email: str = Field(description="L'email de la personne")
```

### Paramètres Utiles de Field

#### 1. `description` : Documentation

```python
nom: str = Field(description="Le nom de la personne")
```

**Utilité :** 
- Documentation automatique
- Les LLM comprennent mieux ce que doit contenir le champ
- Utile pour `response_format` dans LangChain

#### 2. `default` : Valeur par défaut (types immutables)

```python
status: str = Field(default="actif", description="Le statut")
```

**Exemple :**
```python
personne = Personne(nom="Jean", age=30)  # status = "actif" automatiquement
```

#### 3. `default_factory` : Valeur par défaut (types mutables)

```python
tags: List[str] = Field(default_factory=list, description="Les tags")
```

**Pourquoi ?** Pour éviter que tous les objets partagent la même liste.

#### 4. Validation : `ge`, `le`, `min_length`, etc.

```python
age: int = Field(ge=0, le=150)  # ge = greater or equal, le = less or equal
email: str = Field(min_length=5, max_length=100)
```

**Exemple :**
```python
# ✅ Valide
personne = Personne(nom="Jean", age=30, email="jean@example.com")

# ❌ Erreur : age négatif
personne = Personne(nom="Jean", age=-5, email="jean@example.com")
# ValidationError: age must be >= 0
```

---

## Structurer des Réponses : Votre Cas d'Usage

### Pourquoi Structurer les Réponses ?

**Sans Pydantic :**
```python
# Réponse non structurée (juste du texte)
response = "Voici la réponse... Sources: https://example.com, https://example2.com"

# Problèmes :
# - Difficile à parser
# - Pas de validation
# - Structure inconsistante
```

**Avec Pydantic :**
```python
# Réponse structurée
class AgentResponse(BaseModel):
    answer: str = Field(description="La réponse")
    sources: List[Source] = Field(default_factory=list, description="Les sources")

response = AgentResponse(
    answer="Voici la réponse...",
    sources=[
        Source(url="https://example.com"),
        Source(url="https://example2.com")
    ]
)

# Avantages :
# - Structure garantie
# - Validation automatique
# - Accès facile : response.answer, response.sources[0].url
```

### Exemple Complet : Votre Code

```python
from pydantic import BaseModel, Field
from typing import List

# 1. Modèle pour une source
class Source(BaseModel):
    """Une source d'information"""
    url: str = Field(description="L'URL de la source")

# 2. Modèle pour la réponse complète
class AgentResponse(BaseModel):
    """La réponse structurée de l'agent"""
    answer: str = Field(description="La réponse à la question")
    sources: List[Source] = Field(
        default_factory=list, 
        description="Les sources utilisées pour répondre"
    )

# 3. Utilisation avec LangChain
agent = create_agent(
    model=llm, 
    tools=tools, 
    response_format=AgentResponse  # ← Force le LLM à retourner cette structure
)
```

### Comment ça Marche avec LangChain ?

Quand vous utilisez `response_format=AgentResponse` :

1. **Le LLM reçoit le schéma** : "Tu dois retourner un objet avec `answer` (string) et `sources` (liste de Source)"

2. **Le LLM génère la réponse** en respectant la structure

3. **Pydantic valide** que la réponse correspond au schéma

4. **Vous obtenez un objet structuré** :
```python
result = agent.invoke({...})

# Accès facile et sûr
print(result["messages"][-1].content.answer)  # La réponse
print(result["messages"][-1].content.sources[0].url)  # Première source
```

---

## Exemples Pratiques

### Exemple 1 : API REST

```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(description="Email de l'utilisateur")
    age: Optional[int] = Field(None, ge=0, le=150)
    is_active: bool = Field(default=True)

# Utilisation
user = User(
    id=1,
    name="Jean",
    email="jean@example.com",
    age=30
)

# Validation automatique
# Si vous passez des données invalides, Pydantic lève une erreur
```

### Exemple 2 : Données d'API Externe

```python
class WeatherResponse(BaseModel):
    city: str = Field(description="La ville")
    temperature: float = Field(description="Température en Celsius")
    condition: str = Field(description="Condition météo")
    humidity: int = Field(ge=0, le=100, description="Humidité en %")

# Quand vous recevez des données d'une API
data = {
    "city": "Paris",
    "temperature": 22.5,
    "condition": "Ensoleillé",
    "humidity": 65
}

# Validation et structuration
weather = WeatherResponse(**data)  # ✅ Valide automatiquement

# Accès typé
print(f"{weather.city}: {weather.temperature}°C")
```

### Exemple 3 : Configuration

```python
class Config(BaseModel):
    api_key: str = Field(description="Clé API")
    timeout: int = Field(default=30, ge=1, le=300)
    retries: int = Field(default=3, ge=0, le=10)
    enabled: bool = Field(default=True)

# Utilisation
config = Config(api_key="sk-...")
# timeout = 30, retries = 3, enabled = True automatiquement
```

---

## Avantages de Pydantic

### 1. Validation Automatique

```python
# ❌ Sans Pydantic
def process_user(name, age, email):
    if not isinstance(age, int):
        raise ValueError("age must be int")
    if age < 0:
        raise ValueError("age must be positive")
    if not isinstance(email, str):
        raise ValueError("email must be str")
    # ... beaucoup de code de validation

# ✅ Avec Pydantic
class User(BaseModel):
    name: str
    age: int = Field(ge=0)
    email: str

# Validation automatique !
```

### 2. Documentation Automatique

```python
class User(BaseModel):
    name: str = Field(description="Le nom de l'utilisateur")
    age: int = Field(description="L'âge", ge=0)

# Pydantic génère automatiquement la documentation
print(User.model_json_schema())
# {
#   "properties": {
#     "name": {"description": "Le nom de l'utilisateur", "type": "string"},
#     "age": {"description": "L'âge", "minimum": 0, "type": "integer"}
#   }
# }
```

### 3. Intégration avec LangChain

```python
# Le LLM comprend le schéma et génère la bonne structure
agent = create_agent(
    model=llm,
    tools=tools,
    response_format=AgentResponse  # Le LLM sait quoi retourner
)
```

### 4. Type Safety

```python
# Avec Pydantic, votre IDE connaît les types
response = AgentResponse(...)
response.answer  # ✅ IDE sait que c'est un str
response.sources[0].url  # ✅ IDE sait que c'est un str
```

---

## Résumé Visuel

```
BaseModel
    ↓
Définit la STRUCTURE (quels champs)
    ↓
Field()
    ↓
Définit les DÉTAILS (description, validation, default)
    ↓
Résultat
    ↓
Objet structuré et validé automatiquement
```

---

## Checklist de Compréhension

- [ ] **BaseModel** = Moule pour structurer les données
- [ ] **Field** = Instructions pour chaque champ (description, validation, default)
- [ ] **Validation automatique** = Pydantic vérifie les types et valeurs
- [ ] **Structurer les réponses** = Garantir un format cohérent
- [ ] **Avec LangChain** = `response_format` force le LLM à respecter le schéma
- [ ] **default_factory** = Pour les listes/dicts (évite le partage)

---

## En Bref

**Pydantic = Structurer + Valider**

1. **BaseModel** : Définit la structure (quels champs)
2. **Field** : Définit les détails (description, validation, valeurs par défaut)
3. **Résultat** : Objet structuré, validé, et facile à utiliser

**Dans votre cas :** Vous structurez les réponses de l'agent pour qu'elles soient toujours au même format (answer + sources), validées automatiquement, et faciles à utiliser dans votre code.

