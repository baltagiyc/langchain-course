from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import os

load_dotenv()


def main():
    print("Hello from langchain-course!")
    print(os.environ.get("OPENAI_API_KEY"))

    informations = """
    Lionel Messi, parfois surnommé Leo Messi, né le 24 juin 1987 à Rosario (Argentine), est un footballeur international argentin qui évolue au poste d'attaquant à l’Inter Miami. Il est considéré comme l'un des plus grands footballeurs de l'histoire[4],[5],[6].

L'IFFHS l'a considéré meilleur meneur de jeu et meilleur joueur de la décennie 2011-2020 ainsi[7],[8]. Il a remporté 46 trophées collectifs officiels au cours de sa carrière. Son palmarès comprend notamment quatre Ligues des champions, trois Coupes du monde des clubs de la FIFA, trois supercoupes de l'UEFA. dix championnats d'Espagne, sept Coupes d'Espagne, huit Supercoupes d'Espagne ainsi que deux championnats de France et un Trophée des champions. Avec la sélection argentine, Messi a remporté la médaille d'or aux Jeux olympiques de 2008, la Copa América à deux reprises en 2021 et en 2024, la Finalissima et la Coupe du monde en 2022.

En 21 ans de carrière, il est inclus dans la liste des footballeurs avec au moins 1000 apparitions en carrière. Avec plus de 900 buts inscrits et plus de 400 passes décisives délivrées, il est le cinquième meilleur buteur[9] et deuxième meilleur passeur de l'histoire du football[10],[11]. Avec 60 passes décisives délivrées, il est le meilleur passeur de l'histoire en sélection[12],[13]. Il détient à la fois le record mondial du nombre de buts inscrits sur une saison et sur une année et les records de buts et de passes décisives en finales de compétitions officielles. Il est le meilleur dribbleur de la dernière décennie devant Eden Hazard et Franck Ribéry et fait partie des meilleurs dribbleurs de l'histoire du football. Il est également le meilleur buteur et meilleur passeur de l'histoire dans les 5 grands championnats européens avec 496 buts[14] et 222 passes décisives.

Messi commence le football dans sa ville natale de Rosario en Argentine. Dès son plus jeune âge, il montre un talent exceptionnel pour le football. Il a commencé à jouer dès l'âge de cinq ans dans le club local de sa ville natale. Atteint d'un problème de croissance qui nécessite un traitement hormonal, il rejoint à treize ans le FC Barcelone, en Espagne, dont il devient un joueur emblématique. Il y remporte un succès exceptionnel pendant ses dix-sept saisons en équipe première, avant de poursuivre sa carrière au Paris Saint-Germain puis à l’Inter Miami.

Il est trois fois nommé dans le classement des personnalités les plus influentes de la planète par le magazine Time et est le premier footballeur à faire la Une du magazine américain. Ambassadeur de l'UNICEF, il a créé une fondation d'aide à l'enfance à l'âge de 20 ans. Selon le magazine Forbes, il est entré dans le club très fermé des sportifs milliardaires.

    """

    summary_template = """
    Give me a short summary of the following information about the following person: {informations}

    and give 2 facts
    """

    summary_prompt_template = ChatPromptTemplate.from_template(summary_template)

    llm = ChatOpenAI(model="gpt-5", temperature=0)
    chain = summary_prompt_template | llm
    response = chain.invoke({"informations": informations})
    print(response.content)

if __name__ == "__main__":
    main()
