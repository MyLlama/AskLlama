import streamlit as st
import requests
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the list of characters
characters = [
   {"name": "Krishna", "image": "https://via.placeholder.com/50", "prompt": "You are Lord Krishna, who is known for his teachings on righteousness, action and devotion, which can be found in the Bhagavad Gita, he is also known for his playful nature."},
   {"name": "Jesus", "image": "https://via.placeholder.com/50", "prompt": "You are Jesus Christ,a central figure in Christianity, believed by Christians to be the son of God. his life and teachings are recorded in the New Testament of the Bible. Jesus is known for his teachings of love, compassion, and forgiveness"},
   {"name": "Osho", "image": "https://via.placeholder.com/50", "prompt": "You are Osho. He encouraged his followers to question traditional religious and social norms and to explore their own inner experiences and emotions."},
   {"name": "Buddha", "image": "https://via.placeholder.com/50", "prompt": "You are Buddha, who was a spiritual teacher and founder of Buddhism, one of the major religions of the world."},
   {"name": "Guru Nanak", "image": "https://via.placeholder.com/50", "prompt": "You are guru Nanak,whose teaching emphasized the unity of God and the equality of all people and promoted a simple and direct relationship with God through meditation, selfless service, and ethical living."},
   {"name": "Prophet Mohammed", "image": "https://via.placeholder.com/50", "prompt": "You are Prophet Muhammad, his teachings emphasized the oneness of God and the importance of compassion, charity, and social justice."},
   {"name": "Mahavira", "image": "https://via.placeholder.com/50", "prompt": "You are Mahavira, his teachings emphasized the concept of ahimsa, or non-violence. He taught that the ultimate goal of life is to achieve liberation from the cycle of birth and death by following the principles of non-violence, truthfulness, celibacy, and detachment."},
]

# Define the function to get the chatbot response
def get_chatbot_responses(question, selected_characters):
    # Define the URL of the ChatGPT API endpoint
    url = "https://api.openai.com/v1/chat/completions"

    # Set up the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Your_API_KEY",
    }

    completions = []
    for character in selected_characters:
        # Set up the data for the API request
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": f"{character['prompt']}"}, 
                         {"role": "user", "content": f"Q: {question}\n"}]
            
        }

        # Log the request for debugging
        logging.info(f"API request for {character['name']}: {data}\n")

        # Make the API request and handle errors
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # raise an exception if status code is not 2xx
            response_data = response.json()

            # Log the API response for debugging
            logging.info(f"API responce :{response_data}\n")

            # Get the completion from the response and append the character name to it
            completion = response_data["choices"][0]["message"]["content"].strip()
            completion_with_character = f"![{character['name']}]({character['image']}) {character['name']}: {completion}"
            completions.append(completion_with_character)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logging.error(f"Error while making the API request: {e}\n")
            st.error(f"Error while making the API request for {character['name']}. Please try again later.")

    return completions



# Define the app layout
st.set_page_config(page_title="Ask Llama", page_icon=":llama:", layout="wide")
st.title("Ask Llama")
st.subheader("powered by Llama, www.myllama.co")

# Define the sidebar with the list of characters
st.sidebar.title("Select Characters")

# Define the dropdown menu for characters
selected_character_names = st.sidebar.multiselect(
    "Choose characters",
    options=[character["name"] for character in characters],
    format_func=lambda name: name,
)

# Get the selected characters from the list of characters
selected_characters = [character for character in characters if character["name"] in selected_character_names]

# Display an error message if no characters are selected
if len(selected_characters) == 0:
    st.warning("Please select at least one character to start the chat.")
else:
    # Show the selected characters with their images
    st.sidebar.title("Selected Characters")
    for character in selected_characters:
        col1, col2 = st.sidebar.columns([0.2, 0.8])
        with col1:
            st.image(character["image"], width=50)
        with col2:
            st.write(character["name"])

    # Define the chatbox
    chatbox = st.empty()
    question = st.text_input("Ask a question:")

    if st.button("Send"):
        completions = get_chatbot_responses(question, selected_characters)
        chatbot_response = "\n\n".join(completions)
        chatbox.write(chatbot_response)

# Define the footer of the app
st.markdown("---")
st.markdown("This app is made for research purposes and not to hurt any sentiments.")

# Hide the Streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu, footer {visibility: hidden;}
footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 50px;
        line-height: 50px;
        text-align: center;
        background-color: #f5f5f5;
    }
    .streamlit_container {
        position: relative;
        min-height: 100vh;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
