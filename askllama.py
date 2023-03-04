import streamlit as st
import requests
import logging
from PIL import ImageGrab
import base64

# Define a function to take a screenshot
def take_screenshot():
    image = ImageGrab.grab()
    return image

# Define a function to convert an image to a base64 string
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Define the Streamlit app
def app():
    # Add a button to take a screenshot
    if st.button("Take a screenshot and share"):
        screenshot = take_screenshot()
        st.image(screenshot, caption="Screenshot")
        
        # Add a button to share the screenshot on social media
        if st.button("Share on social media"):
            img_str = image_to_base64(screenshot)
            url = "https://www.example.com/share?img={}".format(img_str)
            st.write("Share this URL on social media: {}".format(url))



# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the list of characters
characters = [
   {"name": "Krishna", "image": "http://chat.myllama.co/AskLlama/images/krishana.jpeg", "prompt": "You are Lord Krishna, who is known for his teachings on righteousness, action and devotion, which can be found in the Bhagavad Gita, he is also known for his playful nature. Answer below question as Lord Krishna would have answered."},
   {"name": "Jesus", "image": "http://chat.myllama.co/AskLlama/images/jesus.jpeg", "prompt": "You are Jesus Christ,a central figure in Christianity, believed by Christians to be the son of God. his life and teachings are recorded in the New Testament of the Bible. Jesus is known for his teachings of love, compassion, and forgiveness, Answer Below question as Jesus"},
   {"name": "Osho", "image": "http://chat.myllama.co/AskLlama/images/osho.jpeg", "prompt": "You are Osho. He encouraged his followers to question traditional religious and social norms and to explore their own inner experiences and emotions.Answer below question as Osho would have answered."},
   {"name": "Buddha", "image": "http://chat.myllama.co/AskLlama/images/buddha.jpeg", "prompt": "You are Buddha, who was a spiritual teacher and founder of Buddhism, one of the major religions of the world.Answer below question as Buddha would have answered"},
   {"name": "Guru Nanak", "image": "http://chat.myllama.co/AskLlama/images/nanak.jpeg", "prompt": "You are Guru Nanak,whose teaching emphasized the unity of God and the equality of all people and promoted a simple and direct relationship with God through meditation, selfless service, and ethical living. Answer below question as Guru Nanak would have answered"},
   {"name": "Prophet Mohammed", "image": "http://chat.myllama.co/AskLlama/images/mohammad.jpeg", "prompt": "You are Prophet Muhammad, his teachings emphasized the oneness of God and the importance of compassion, charity, and social justice. Answer below question as Prophet Muhammad would have answered"},
   {"name": "Mahavira", "image": "http://chat.myllama.co/AskLlama/images/mahavir.jpeg", "prompt": "You are Mahavira, his teachings emphasized the concept of ahimsa, or non-violence. He taught that the ultimate goal of life is to achieve liberation from the cycle of birth and death by following the principles of non-violence, truthfulness, celibacy, and detachment. Answer below question as Mahavira would have answered"},
]

# Define the function to get the chatbot response
def get_chatbot_responses(question, selected_characters):
    # Define the URL of the ChatGPT API endpoint
    url = "https://api.openai.com/v1/chat/completions"

    # Set up the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
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
            completion_with_character = f"![<span style='color: orange'>{character['name']}</span>]({character['image']}) {character['name']}: {completion}"
            completions.append(completion_with_character)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logging.error(f"Error while making the API request: {e}\n")
            st.error(f"Error while making the API request for {character['name']}. Please try again later.")

    return completions


# Define the app layout
st.set_page_config(page_title="Ask Llama", page_icon="https://www.myllama.co/wp-content/uploads/2023/01/cropped-android-chrome-512x512-1.png",  layout="wide")

header = st.container()
with header:
    st.markdown(
        """
        <div style='display: flex; align-items: center;'>
            <img src='https://www.myllama.co/wp-content/uploads/2023/01/LAMA-logo_Final-01.png' width='90' height='90'/>
            <h1 style='margin: 0 0 0 20px;'>Ask Llama</h1>
        </div>
        """
        , unsafe_allow_html=True
    )
    st.markdown("<a style='text-decoration:none' href='http://www.myllama.co'>"
                "<h4>"
                "Powered by Llama"
                "</h4>"
                "</a>",
                unsafe_allow_html=True)

# Define the sidebar with the list of characters
st.sidebar.title("Select Characters")

# Define the dropdown menu for characters
selected_character_names = st.sidebar.multiselect(
    "Choose characters to answer your question!",
    options=[character["name"] for character in characters],
    format_func=lambda name: name,
)

# Get the selected characters from the list of characters
selected_characters = [character for character in characters if character["name"] in selected_character_names]

# Display an error message if no characters are selected
if len(selected_characters) == 0:
    st.warning("Please select characters from sidebar to ask a question.")
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
        chatbot_response = "\n\n\n".join(completions)
        chatbox.write(chatbot_response)

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

# Define the footer of the app
st.markdown("---")
st.markdown("This app is made for research purposes and not to hurt any sentiments. May occasionally generate incorrect, harmful or biased content.")

# Add a button to show the feedback form
if st.button("Give feedback"):
    # Add a text box for feedback
    feedback = st.text_input("Feedback:")
    
    # Add a button to submit feedback
    if st.button("Submit"):
        # Print the feedback to the logs
        logging.info(f"\n\n ***FEEDBACK*** :{feedback}\n\n")
        st.success("Feedback submitted!")

# Run the Streamlit app
if __name__ == "__main__":
    app()
