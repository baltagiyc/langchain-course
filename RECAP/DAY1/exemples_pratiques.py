"""
Exemples Pratiques LangChain - Pour Révision Rapide
Copiez-collez ces exemples pour tester rapidement les concepts
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()


# ============================================
# EXEMPLE 1 : Template avec variable
# ============================================
def exemple_template_variable():
    """Template avec une variable à remplir."""
    print("\n=== EXEMPLE 1 : Template avec variable ===")
    
    template = ChatPromptTemplate.from_template(
        "Résume ce texte en 2 phrases : {texte}"
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = template | llm
    
    texte = "Python est un langage de programmation populaire..."
    response = chain.invoke({"texte": texte})
    print(response.content)


# ============================================
# EXEMPLE 2 : Template sans variable
# ============================================
def exemple_template_simple():
    """Template sans variable."""
    print("\n=== EXEMPLE 2 : Template sans variable ===")
    
    template = ChatPromptTemplate.from_template(
        "Explique-moi ce qu'est le machine learning"
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = template | llm
    
    response = chain.invoke({})  # Dictionnaire vide
    print(response.content)


# ============================================
# EXEMPLE 3 : LLM direct (sans template)
# ============================================
def exemple_llm_direct():
    """Utiliser le LLM directement sans template."""
    print("\n=== EXEMPLE 3 : LLM direct ===")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Option 1 : String simple
    response = llm.invoke("Qu'est-ce que Python ?")
    print(response.content)
    
    # Option 2 : Liste de messages
    response = llm.invoke([("user", "Qu'est-ce que Python ?")])
    print(response.content)


# ============================================
# EXEMPLE 4 : Gestion de clés API
# ============================================
def exemple_gestion_cles():
    """Gérer les clés API."""
    print("\n=== EXEMPLE 4 : Gestion de clés API ===")
    
    # Méthode 1 : Avec .env (recommandé)
    api_key = os.environ.get("OPENAI_API_KEY")
    print(f"Clé depuis .env : {api_key[:20]}..." if api_key else "Clé non trouvée")
    
    # Méthode 2 : Définir manuellement
    os.environ["GROQ_API_KEY"] = "gsk-..."
    print("Clé définie manuellement")


# ============================================
# EXEMPLE 5 : Différentes températures
# ============================================
def exemple_temperatures():
    """Tester différentes températures."""
    print("\n=== EXEMPLE 5 : Différentes températures ===")
    
    prompt = "Raconte une histoire courte sur un robot"
    
    # Temperature 0 (déterministe)
    llm_froid = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response_froid = llm_froid.invoke(prompt)
    print(f"Température 0 : {response_froid.content[:50]}...")
    
    # Temperature 0.7 (créatif)
    llm_chaud = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    response_chaud = llm_chaud.invoke(prompt)
    print(f"Température 0.7 : {response_chaud.content[:50]}...")


# ============================================
# EXEMPLE 6 : Template avec plusieurs variables
# ============================================
def exemple_template_multiple():
    """Template avec plusieurs variables."""
    print("\n=== EXEMPLE 6 : Template avec plusieurs variables ===")
    
    template = ChatPromptTemplate.from_template(
        "Écris un {type_texte} sur le sujet '{sujet}' en {langue} langues."
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    chain = template | llm
    
    response = chain.invoke({
        "type_texte": "poème",
        "sujet": "l'intelligence artificielle",
        "langue": "français"
    })
    print(response.content)


# ============================================
# EXEMPLE 7 : Erreur commune à éviter
# ============================================
def exemple_erreur_commune():
    """Montrer l'erreur commune et la correction."""
    print("\n=== EXEMPLE 7 : Erreur commune ===")
    
    template = ChatPromptTemplate.from_template("Résume : {texte}")
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # ❌ MAUVAIS : Invoquer le template puis chaîner
    try:
        prompt_rempli = template.invoke({"texte": "Python est..."})
        chain = prompt_rempli | llm  # ❌ ERREUR !
        print("❌ Cette ligne ne devrait pas s'exécuter")
    except Exception as e:
        print(f"❌ Erreur attendue : {type(e).__name__}")
    
    # ✅ BON : Chaîner le template puis invoquer
    chain = template | llm
    response = chain.invoke({"texte": "Python est un langage..."})
    print(f"✅ Réponse correcte : {response.content[:50]}...")


# ============================================
# EXEMPLE 8 : Fonction réutilisable
# ============================================
def creer_chain_resume():
    """Crée une chaîne réutilisable pour résumer."""
    template = ChatPromptTemplate.from_template(
        "Résume ce texte en maximum 3 phrases : {texte}"
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return template | llm


def exemple_fonction_reutilisable():
    """Utiliser une fonction qui retourne une chaîne."""
    print("\n=== EXEMPLE 8 : Fonction réutilisable ===")
    
    chain = creer_chain_resume()
    
    texte1 = "Python est un langage de programmation..."
    response1 = chain.invoke({"texte": texte1})
    print(f"Résumé 1 : {response1.content}")
    
    texte2 = "Le machine learning est une branche de l'IA..."
    response2 = chain.invoke({"texte": texte2})
    print(f"Résumé 2 : {response2.content}")


# ============================================
# MAIN : Exécuter tous les exemples
# ============================================
if __name__ == "__main__":
    print("🚀 Exemples Pratiques LangChain")
    print("=" * 50)
    
    # Décommentez les exemples que vous voulez tester
    
    # exemple_template_variable()
    # exemple_template_simple()
    # exemple_llm_direct()
    # exemple_gestion_cles()
    # exemple_temperatures()
    # exemple_template_multiple()
    # exemple_erreur_commune()
    # exemple_fonction_reutilisable()
    
    print("\n✅ Tous les exemples sont prêts à être testés !")
    print("💡 Décommentez les fonctions dans le main() pour les tester")

