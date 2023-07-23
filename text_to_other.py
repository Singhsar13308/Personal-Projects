import pyttsx3#text to speech
import PyPDF2#reading pdfs
import requests#for bionic reading api
from bs4 import BeautifulSoup


import openai



url = "https://bionic-reading1.p.rapidapi.com/convert"#bionic api link



user_inp = input("Would you like to convert the pdf to audio, convert to a bionic reading format, or have a summary of the pdf: ")

open_pdf = PyPDF2.PdfReader(open('Sarthak Singh Resume.pdf', 'rb'))#open pdf

bionic_text = " "

for page in (open_pdf.pages):
    text = page.extract_text()

    bionic_text += text

    cleaned_text = text.strip().replace('\n', ' ')



#-------------------------
def audio_convert(cleaned_text):

  #  open_pdf = PyPDF2.PdfReader(open('The Little Prince.pdf', 'rb'))

    speaker = pyttsx3.init()

    # for page in (open_pdf.pages):
    #     text = page.extract_text()

    #     cleaned_text = text.strip().replace('\n', ' ')
    #     #print(cleaned_text)
    
    speaker.save_to_file(cleaned_text, 'audio.mp3')

    speaker.runAndWait()

    speaker.stop()
#-----------------------------


if user_inp == 'audio':
    audio_convert('The Little Prince.pdf')


def summarize(text):

    chat_log = []

    openai.api_key = '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'
    #giving summary
    prompt = "Briefly summarize the following text:\n\n" + text

    chat_log.append({"role": "user", "content": prompt})

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.3,
        n=1,
        stop=None,

    )
    th3_summary = response.choices[0].text.strip()

    chat_log.append({"role": "assistant", "content": th3_summary})

    print(th3_summary)

    #post summary questions

    

    print("You may ask further questions about the text.\nSay \"Done!\" when finished with questions: \n")
    
    

    while input != "quit()":

        message = input()#take input from user
        
        chat_log.append({"role": "user", "content": message})#add user input to chat log
        
        response = openai.ChatCompletion.create(#telling gpt what the user asked, answer will be stored in response
            model="gpt-3.5-turbo",
            messages=chat_log)
        
        gpt_reply = response["choices"][0]["message"]["content"]#basically gets the message instead of the whole json output

        chat_log.append({"role": "assistant", "content": gpt_reply})

        print("\n" + gpt_reply + "\n")

    


if user_inp == 'summary':
    (summarize(cleaned_text))



def bionic_reading(bionic_text):

    #bionic reading stuff
    payload = {
        "content": "{}".format(bionic_text),
        "response_type": "html",
        "request_type": "html",
        "fixation": "1",
        "saccade": "10"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "4fa1e20f7bmsha3298d2081dd68ep142cccjsn399d548298a8",
        "X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    with open('file.html', 'w') as file:
        file.write(str(response.text))

if user_inp == 'bionic':
    (bionic_reading(bionic_text))






#bionic_response_get = BeautifulSoup(response.text, 'html.parser')

#bionic_response_stripped = bionic_response_get.find('div', class_='bionic-reader-container').text.strip()



