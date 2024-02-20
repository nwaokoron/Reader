#Synthesizes speech from the input string of text
from google.cloud import texttospeech
from bs4 import BeautifulSoup
import requests, logging
from newspaper import Article
import trafilatura

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# textToSpeech take an input url and converst the main content of that site converts
# it to speech and saves it as an mp3 file.
def textToSpeech(content):   

    logger.info("textToSpeech")
    logger.debug(__name__)
    
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    article_content = content
    filename = "output.mp3"
    audio_content_list = []
    for i in range(0, len(article_content), 4000): # Dealing with 5k char Limit per Google API
        synthesis_input = texttospeech.SynthesisInput(text=article_content[i:i+4000])

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        # voice = texttospeech.VoiceSelectionParams(
        #     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        # )

        voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-B", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        audio_content_list.append(response.audio_content)
    
    # take audio_content_list and turn it into one audio file
    for i in range(len(audio_content_list)):
        with open(filename, "ab") as out:
            out.write(audio_content_list[i])

    return filename
# [END tts_synthesize_text]

# [START tts_synthesize_text]


# uncomment to run function from command line
# user_input = input("web page url you want to convert to speech: ")
# textToSpeech(user_input)