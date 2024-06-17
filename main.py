import chainlit as cl
from groq import Groq
from langdetect import detect
from deep_translator import GoogleTranslator

# Initialize the Groq client
client = Groq(api_key="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")

@cl.on_message
async def main(message: cl.Message):
    # Detect the language of the input message
    detected_language = detect(message.content)
    
    # If the detected language is not English, translate the message to English
    if detected_language != "en":
        input_text = GoogleTranslator(source=detected_language, target="en").translate(message.content)
    else:
        input_text = message.content

    # Create a chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model="llama3-8b-8192",
    )
    
    # Get the response from the model
    response_text = chat_completion.choices[0].message.content

    # If the input was translated to English, translate the response back to the detected language
    if detected_language != "en":
        response_text = GoogleTranslator(source="en", target=detected_language).translate(response_text)

    # Send the response back to the user
    await cl.Message(
        content=response_text
    ).send()
