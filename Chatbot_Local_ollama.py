import streamlit as st
import requests
import json

# Définir l'URL du serveur Ollama
OLLAMA_SERVER_URL = "http://127.0.0.1:11434/api/chat"

# Définir le modèle utilisé
model_name = "mistrallite"  # Remplacez par le nom de votre modèle

# Configurer Streamlit
st.set_page_config(page_title="Chatbot avec Ollama", layout="wide")
st.title("💬 Chatbot Ollama - Assistant Culinaire")
st.markdown("### Posez une question, et obtenez des suggestions de recettes marocaines !")

# Historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Zone de chat
with st.container():
    st.write("### Discussion")
    for message in st.session_state["messages"]:
        role = message["role"]
        content = message["content"]
        if role == "user":
            st.markdown(f"**🧑‍💻 Vous :** {content}")
        else:
            st.markdown(f"**🤖 Chatbot :** {content}")

# Saisie utilisateur
user_input = st.text_input("Écrivez votre message ici :", placeholder="Quels ingrédients avez-vous ?")

# Fonction pour envoyer le message à Ollama
def send_message(prompt):
    # Préparer la requête
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are Youssef, a virtual culinary assistant specializing in moroccan recipe recommendations. Your mission is to help users find recipes based on the ingredients they have available. When a user provides a list of ingredients, analyze them and suggest up to three recipes that match, considering possible ingredient combinations. For each recipe, provide: the recipe name, a brief description, and a short list of preparation steps. If no exact match is found, offer creative ideas using similar or complementary ingredients. Always respond in a friendly and engaging manner. Your goal is to make the user experience simple, helpful, and enjoyable."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Envoyer la requête POST au serveur
        response = requests.post(OLLAMA_SERVER_URL, json=payload, stream=True)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Lire le flux JSON ligne par ligne
        full_response = ""
        for line in response.iter_lines():
            if line:  # Ignorer les lignes vides
                data = json.loads(line.decode("utf-8"))  # Charger chaque ligne comme JSON
                content = data.get("message", {}).get("content", "")
                full_response += content

        return full_response
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête : {e}"
    except json.JSONDecodeError as je:
        return f"Erreur de décodage JSON : {je}"

# Si l'utilisateur soumet un message
if user_input:
    # Ajouter le message utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Obtenir la réponse du serveur Ollama
    bot_response = send_message(user_input)

    # Ajouter la réponse du bot à l'historique
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})

# Pas besoin de st.experimental_rerun(), Streamlit met à jour l'interface automatiquement
