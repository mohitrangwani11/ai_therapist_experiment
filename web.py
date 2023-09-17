import gradio as gr
import openai, config,subprocess
import os
import pyttsx3


openai.api_key = config.OPENAI_API_KEY
messages = [{"role": "system", "content": 'You are a therapist. Respond to all input in 50 words or less. Please do not prescribe medication of any sort since you are not licensed to prescribe medication. In case a person is talking about harmful actions including self-harm, please request them to reach out to a licensed medical professional.'}]

def transcribe(audio):
    global messages

    audio_filename_with_extension = audio + '.wav'
    os.rename(audio, audio_filename_with_extension)
    print(audio)
    audio_file = open(audio_filename_with_extension,"rb")
    transcript = openai.Audio.transcribe("whisper-1",audio_file)

    messages.append({"role":"user","content":transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    engine = pyttsx3.init()
    #engine.say('Hello, world!')
    

    engine.say(system_message['content'])
    engine.runAndWait()

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    
    

    return chat_transcript

#demo = gr.Interface(fn=image_classifier, inputs="image", outputs="label")
ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"),outputs="text")
ui.launch(share=True)