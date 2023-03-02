import streamlit as st
import requests
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the list of characters
characters = [
    {"name": "Krishna", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Lord Krishna would have answered."},
    {"name": "Jesus", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Jesus Christ would have answered."},
    {"name": "Osho", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Osho would have answered."},
    {"name": "Buddha", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Buddha would have answered."},
    {"name": "Guru Nanak", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Guru Nanak would have answered."},
    {"name": "Prophet Mohammed", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Prophet Mohammed would have answered."},
    {"name": "Mahavira", "image": "https://via.placeholder.com/150", "prompt": "Q: Answer this question as  Mahavira would have answered."},
]

# Define the function to get the chatbot response
def get_chatbot_responses(question, selected_characters):
    # Define the URL of the ChatGPT API endpoint
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"

    # Set up the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY_HERE",
    }

    completions = []
    for character in selected_characters:
        # Set up the data for the API request
        data = {
            "prompt": f"{character['prompt']} \nQ: {question}\nA:",
            "temperature": 0.7,
            "max_tokens": 256,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": "\n",
            "n": 1,
            "user": character["name"]
        }

        # Log the request for debugging
        logging.info(f"API request for {character['name']}: {data}")

        # Make the API request and handle errors
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # raise an exception if status code is not 2xx
            response_data = response.json()

            # Log the API response for debugging
            logging.info(response_data)

            # Get the completion from the response and append the character name to it
            completion = response_data["choices"][0]["text"].strip()
            completion_with_character = character["name"] + ": " + completion
            completions.append(completion_with_character)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logging.error(f"Error while making the API request: {e}")
            st.error(f"Error while making the API request for {character['name']}. Please try again later.")

    return completions



# Define the app layout
st.set_page_config(page_title="Ask Llama", page_icon=":llama:", layout="wide")
st.title("Ask Llama")
st.subheader("powered by Llama, www.myllama.co")

# Define the sidebar with the list of characters
st.sidebar.title("Select Characters")
selected_characters = []
for character in characters:
    if st.sidebar.checkbox(character["name"], key=character["name"]):
        selected_characters.append(character)

# Display an error message if no characters are selected
if len(selected_characters) == 0:
    st.warning("Please select at least one character to start the chat.")
else:
    # Define the chatbox
    st.title("Chatbox")
    chatbox = st.empty()

    # Define the input field for the user's question
    question = st.text_input("Ask a question:")

    # Process the user's question and display the chatbot response
    if st.button("Send"):
        completions = get_chatbot_responses(question, selected_characters)
        chatbot_response = "\n\n".join(completions)
        chatbox.write(chatbot_response)
        
# Define the footer of the app
st.markdown("---")
st.markdown("This app is made for research purposes and not to hurt any sentiments.")
