#Synthesizes speech from the input string of text
from google.cloud import texttospeech
from bs4 import BeautifulSoup
import requests
from newspaper import Article
import trafilatura



def textToSpeech(input_url):        
 
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    article_content = ""
    # Set the text input to be synthesized
    article = Article(url=input_url)
    try:
        article.download() # try downloading with newpaper library
        article_content = article.text
        article.parse()
    except Exception as e:
        print("download failed via newspaper library")
        HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        response = requests.get(input_url, headers=HEADERS)

# Check for successful response (status code 200)
        html_content = ""
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            article_content = soup.find("article") or soup.find("div", class_="article-body") or soup.find("div", class_="content") or soup.find("main")
            if article_content is None:
                print("Error: Unable to retrieve HTML content.")
                return
            article_content = article_content.text
        else:
            print("Error: Unable to retrieve HTML content via BeautifulSoup.")
            print("HTTP Status code:", response.status_code)
            #return
            downloaded = trafilatura.fetch_url(input_url)
            try:
                article_content = trafilatura.extract_text(downloaded,include_comments=False)
            except Exception as e:
                print("download failed via trafilatura library")
                return

    print("downloaded") #TODO: Since download fails for some urls. let's wrap it with an exception and use and
    # another library to get the main content.

    synthesis_input = texttospeech.SynthesisInput(text=article_content[:4000])

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
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


user_input = input("web page url you want to convert to speech: ")
textToSpeech(user_input)