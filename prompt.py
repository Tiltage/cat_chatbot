import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI()

def generate_text(prompt):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a chatbot, known as Chatty Cat,+\
       that takes on the personality of a cat to cheer up and motivate employees.+\
       Place heavier emphasis on the use of cat emojis in your responses.+\
       Be as encouraging as possible.+\
       Refer to professional help where signs of self-harm behavior surface."},
      {"role": "user", "content": f"{prompt}"}]
    )
  return response.choices[0].message.content

def generate_dalle_prompt(prompt):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a chatbot, known as Chatty Cat,+\
       that takes on the personality of a cat to cheer up and motivate employees.+\
       Generate an appropriate description that would suit the needs of the user in encouraging them.+\
       If provided a description of a cat, elaborate on the description of the cat as well.+\
       Be as positive as possible"},
      {"role": "user", "content": f"{prompt}"}]
    )
  return response.choices[0].message.content

def reply(prompt, message_history):

  #Append prompt to message history
  message_history.append({"sender": "You", "content": f"{prompt}"})

  #Generate a chat response using the OpenAI API
  reply_text = generate_text(prompt)

  #Append the generated response to the message history
  message_history.append({"sender": "Chatty Cat", "content": f"{reply_text}"})

  #Return the generated response and the updated message history
  return message_history

def generate_image(user_prompt=None):

  def call_dalle(prompt="A cute-looking orange cat waving hi"):
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size='1024x1024',
      quality="standard",
      n=1,)
    image_url = response.data[0].url
    return image_url

  if user_prompt is None:
    reply_image_url = call_dalle()

  prompt = generate_dalle_prompt(user_prompt)
  reply_image_url = call_dalle(prompt)
  return reply_image_url