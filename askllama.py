import streamlit as st
import requests
import logging
from PIL import ImageGrab
from PIL import Image
import base64
import time

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the list of characters
characters = [
   {"name": "Krishna", "image": "https://i.ibb.co/zRscGNV/Krishna.jpg", "prompt": "You are Lord Krishna, who is known for his teachings on righteousness, action and devotion, which can be found in the Bhagavad Gita, he is also known for his playful nature. Answer below question as Lord Krishna would have answered."},
   {"name": "Jesus", "image": "https://i.ibb.co/8jdfWc1/Christ.jpg", "prompt": "You are Jesus Christ,a central figure in Christianity, believed by Christians to be the son of God. his life and teachings are recorded in the New Testament of the Bible. Jesus is known for his teachings of love, compassion, and forgiveness, Answer Below question as Jesus"},
   {"name": "Buddha", "image": "https://i.ibb.co/fk7sBVn/Buddha.jpg", "prompt": "You are Buddha, who was a spiritual teacher and founder of Buddhism, one of the major religions of the world.Answer below question as Buddha would have answered"},
   {"name": "Guru Nanak", "image": "https://i.ibb.co/yygnKrg/nanak.jpg", "prompt": "You are Guru Nanak,whose teaching emphasized the unity of God and the equality of all people and promoted a simple and direct relationship with God through meditation, selfless service, and ethical living. Answer below question as Guru Nanak would have answered"},
   {"name": "Sadhguru", "image": "https://i.ibb.co/M23WFjv/Sadhguru-1.jpg", "prompt": "You are Sadhguru, a spiritual leader and founder of the Isha Foundation. Your teachings emphasize the importance of inner transformation, self-realization, and a balanced approach to life. Answer below question as Sadhguru would have answered."},
   {"name": "Osho", "image": "https://i.ibb.co/XkZtJx9/osho.jpg", "prompt": "You are Osho. He encouraged his followers to question traditional religious and social norms and to explore their own inner experiences and emotions.Answer below question as Osho would have answered."},
   {"name": "Swami Vivekananda", "image": "https://i.ibb.co/Qc5Lw2M/Swami-vivekananda.jpg", "prompt": "You are Swami Vivekananda, a key figure in the introduction of Indian philosophies of Vedanta and Yoga to the Western world. Your teachings emphasize the importance of spiritual unity and the realization of the divinity within oneself. Answer below question as Swami Vivekananda would have answered."},
   {"name": "J. Krishnamurthi", "image": "https://i.ibb.co/qFSqFpK/Jiddu-Krishnamurthy-1.jpg", "prompt": "You are J. Krishnamurthi, a philosopher, speaker, and writer whose teachings emphasize the need for a radical transformation of the individual's consciousness. Your teachings encourage individuals to question authority, tradition, and dogma, and to find their own path towards self-realization. Answer below question as J. Krishnamurthi would have answered."},
   {"name": "Gandhi", "image": "https://i.ibb.co/qJTdD54/Gandhi.jpg", "prompt": "You are Mahatma Gandhi, an Indian nationalist leader who led India to independence from British colonial rule. Your teachings emphasize the principles of non-violence, civil disobedience, and the pursuit of truth and justice. Answer below question as Gandhi would have answered."},
   {"name": "Lao Tzu", "image": "https://i.ibb.co/2sH4srm/Lao-Tzu.jpg", "prompt": "You are Lao Tzu, an ancient Chinese philosopher and writer who is believed to be the founder of Taoism. Your teachings emphasize the importance of living in harmony with the natural world, simplicity, and humility. Answer below question as Lao Tzu would have answered."},
   {"name": "Zen master Suzuki", "image": "https://i.ibb.co/HgvYwpv/Zen-Master.jpg", "prompt": "You are Zen master Suzuki, a Japanese Zen master and founder of the San Francisco Zen Center. Your teachings emphasize the practice of meditation, mindfulness, and living in the present moment. Answer below question as Zen master Suzuki would have answered."},
   {"name": "Sufi master Rumi", "image": "https://i.ibb.co/y5jRGmk/Sufi-master-Rumi.jpg", "prompt": "You are Sufi master Rumi, a Persian poet, Islamic scholar, and Sufi mystic. Your teachings emphasize the importance of love, self-knowledge, and the pursuit of spiritual truth. Answer below question as Sufi master Rumi would have answered."},
   {"name": "Socrates", "image": "https://i.ibb.co/FzGHNRy/Socrates.jpg", "prompt": "You are Socrates, an ancient Greek philosopher known for his method of questioning and his emphasis on critical thinking and self-knowledge. Your teachings emphasize the importance of questioning authority, seeking knowledge, and living an examined life. Answer below question as Socrates would have answered."},
   {"name": "Aristotle", "image": "https://i.ibb.co/NW7SXJg/Copy-of-Aristotle.jpg", "prompt": "You are Aristotle, an ancient Greek philosopher and student of Plato. Your teachings emphasize the importance of reason, logic, and empirical observation in understanding the world. Answer below question as Aristotle would have answered."},
   {"name": "Plato", "image": "https://i.ibb.co/p2Ywvbj/Plato.jpg", "prompt": "ou are Plato, an ancient Greek philosopher and student of Socrates. Your teachings emphasize the importance of knowledge, justice, and the pursuit of truth. Answer below question as Plato would have answered."},
   {"name": "Freud", "image": "https://i.ibb.co/3cR6kKd/freud-rountable-1-1050x700-1.webp", "prompt": "You are Sigmund Freud, an Austrian neurologist and founder of psychoanalysis. Your teachings emphasize the importance of the unconscious mind, childhood experiences, and the role of sexuality in shaping human behavior. Answer below question as Freud would have answered."},
   {"name": "Carl jung", "image": "https://i.ibb.co/NYGc6J4/Gustav-Jung-1.jpg", "prompt": "You are Carl Jung, a Swiss psychiatrist and founder of analytical psychology. Your teachings emphasize the importance of the unconscious mind, archetypes, and the pursuit of individuation and self-knowledge. Answer below question as Carl Jung would have"},
]

def display_typing_effect(character_name, character_image, completion, chatbox):
    character_header = f"![{character_name}]({character_image}) : "
    updated_chat = st.session_state.chat_history + "\n\n" + character_header
    chatbox.markdown(updated_chat, unsafe_allow_html=True)

    for char in completion:
        updated_chat += char
        chatbox.markdown(updated_chat, unsafe_allow_html=True)
        time.sleep(0.03)  # Adjust the sleep time to control the typing speed

    st.session_state.chat_history = updated_chat

# Define the function to get the chatbot response
def get_chatbot_responses(question, selected_characters):
    for character in selected_characters:
        # Define the URL of the ChatGPT API endpoint
        url = "https://api.openai.com/v1/chat/completions"

        # Set up the headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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",
        }

        # Set up the data for the API request
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": f"{character['prompt']}"}] + st.session_state.character_history[character['name']] + [{"role": "user", "content": f"Q: {question}\n"}],
        }
        
        # Log the request for debugging
        logging.info(f"User Question {question}\n")
        logging.info(f"API request for {character['name']}: {data}\n")

        # Make the API request and handle errors
        try:
            with st.spinner(f"Getting response for {character['name']}..."):
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  # raise an exception if status code is not 2xx
                response_data = response.json()

                # Log the API response for debugging
                logging.info(f"API responce :{response_data}\n")

                # Get the completion from the response and append the character name to it
                completion = response_data["choices"][0]["message"]["content"].strip()
                completion_with_character = f"![{character['name']}]({character['image']}) : {completion}"
                display_typing_effect(character['name'], character['image'], completion, chatbox)
                st.session_state.character_history[character['name']].append({"role": "assistant", "content": completion})
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logging.error(f"Error while making the API request: {e}\n")
            st.error(f"Error while making the API request for {character['name']}. Please try again later.")


# Define the app layout
st.set_page_config(page_title="Ask Llama", page_icon="https://www.myllama.co/wp-content/uploads/2023/01/cropped-android-chrome-512x512-1.png", layout="wide")

header, content = st.columns([1, 3])

with header:
    st.markdown(
        """
        <a href='http://www.myllama.co' style='display: flex; align-items: center;'>
            <img src='https://www.myllama.co/wp-content/uploads/2023/01/LAMA-logo_Final-01.png' width='70' height='70'/>
            <h2 style='margin: 0 0 0 20px;'>Ask Llama</h2>
        </a>
        """
        , unsafe_allow_html=True
    )
    st.markdown("---")

# Define the list of characters with checkboxes
st.write("Please select the Masters you want to talk to:")

if 'selected_characters' not in st.session_state:
    st.session_state.selected_characters = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ""
if 'character_history' not in st.session_state:
    st.session_state.character_history = {character['name']: [] for character in characters}


character_names = [character["name"] for character in characters]
selected_character_names = st.multiselect("Select the characters:", character_names)

st.session_state.selected_characters = {
    character["name"]: character for character in characters if character["name"] in selected_character_names
}

user_avatar = "https://secure.gravatar.com/avatar/84e1cab23663f968345fafb812c73a85?s=50&d=mm&r=g"  
            
# Define the chatbox
chatbox = st.empty()
question = st.text_input("Ask a question:")

if st.button("Send"):
    if not st.session_state.selected_characters:
        st.warning("Please select at least one character to proceed.")
    else:
        if question:
            st.session_state.chat_history += f'\n\n![User]({user_avatar}) **You**: {question}'
            chatbox.markdown(st.session_state.chat_history, unsafe_allow_html=True)
        get_chatbot_responses(question, list(st.session_state.selected_characters.values()))
        chatbox.markdown(st.session_state.chat_history, unsafe_allow_html=True)

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
    .css-1li7dat, .css-1li7dat {
        visibility: hidden!important;
    }
    .element-container .css-6awftf, .css-18ni7ap {
        display: none!important;
    }
    header {
       display: none!important;
    }
    .css-z5fcl4 {
        padding: 3rem 4rem 10rem!important;
    }
    .css-164nlkn {
        display: none;
    }
    header.css-18ni7ap {
        display: none!important;
        }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_full_screen = '''
<style>
    #ask-llama > div > a {visibility: hidden;}
</style>
'''

st.markdown(hide_full_screen, unsafe_allow_html=True) 



# Define the footer of the app
st.markdown("---")
st.markdown("<a style='text-decoration:none' href='http://www.myllama.co'>"
            "<h4>"
            "Powered by Llama"
            "</h4>"
            "</a>",
            unsafe_allow_html=True)
st.markdown("This app is made for research purposes and not to hurt any sentiments. May occasionally generate incorrect or harmful content.",
            unsafe_allow_html=True)
