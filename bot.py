import interactions
import base64
import io
from openai import OpenAI


import os

"""
Instantiation
"""
bot_token = os.environ.get('DISCORD_TOKEN')
client = OpenAI()
bot = interactions.Client()


"""
Def
"""

def gen_file(prompt, image_url):
    model = 'gpt-4-vision-preview'
    messages = [{'role': 'user', 'content': [{'type': 'text', 'text': prompt}, {'type': 'image_url', 'image_url': {'url': image_url}}]}]
    response = client.chat.completions.create(model='gpt-4-vision-preview', messages=messages, max_tokens=1024)
    message = response.choices[0].message
    response = client.images.generate(model='dall-e-3', prompt=message.content, quality='hd', n=1, response_format='b64_json')
    image = base64.b64decode(response.data[0].b64_json)
    stream = io.BytesIO(image)
    file = interactions.File('image.png', fp=stream)
    return file

@bot.command(
    name="anime",
    description="I'll turn a photo you drop into an anime picture",
    options=[interactions.Option(name='photo', description="your photo here", type=interactions.OptionType.ATTACHMENT)],
)
async def anime(ctx: interactions.CommandContext, photo):
    await ctx.defer()
    if photo.url:
        prompt = """
        Give me a prompt for DALL-E to use to reproduce this image. Describe the image in great detail, as DALL-E will not be able to see the original image. 
        Describe the image as if the subject(s) in it are anime characters. Ensure you include pertinent details like what direction the subject is facing, 
        what kinds of clothing or jewelry they're wearing, if they're wearing glasses (and what those look like), what their facial expressions are,
        how they're posing, and what their background is. If the subject appears to be human, be sure to include their gender and skin color as well. 
        Pay particular attention to their hair detail. Go for likeness rather than being a generic anime character. If someone doesn't have bangs don't add bangs for example.
        Pay particular attention to their facial features as well. Go for likeness rather than being a generic anime character. If someone has a beard be sure to include the beard.
        If there's multiple people focus on getting the number and descriptions right.
        Only return the DALL-E prompt, and nothing else.
        """
        realistic = gen_file(prompt, photo.url)

        prompt = """
        Give me a prompt for DALL-E to use to reproduce this image. Describe the image in great detail, as DALL-E will not be able to see the original image. 
        Describe the image as if the subject(s) in it are anime characters with the likeness of hayao miyazaki art style. Ensure you include pertinent details like what direction the subject is facing, 
        what kinds of clothing or jewelry they're wearing, if they're wearing glasses (and what those look like), what their facial expressions are,
        how they're posing, and what their background is. If the subject appears to be human, be sure to include their gender and skin color as well. 
        Pay particular attention to their hair detail. Go for likeness rather than being a generic anime character. If someone doesn't have bangs don't add bangs for example.
        Pay particular attention to their facial features as well. Go for likeness rather than being a generic anime character. If someone has a beard be sure to include the beard.
        If there's multiple people focus on getting the number and descriptions right.
        Only return the DALL-E prompt, and nothing else.
        """
        miyazaki = gen_file(prompt, photo.url)

        prompt = """
        Give me a prompt for DALL-E to use to reproduce this image. Describe the image in great detail, as DALL-E will not be able to see the original image. 
        Describe the image as if the subject(s) in it are anime characters in style of Yusuke Kozaki. Ensure you include pertinent details like what direction the subject is facing, 
        what kinds of clothing or jewelry they're wearing, if they're wearing glasses (and what those look like), what their facial expressions are,
        how they're posing, and what their background is. If the subject appears to be human, be sure to swap their gender but keep the same skin color. 
        Only return the DALL-E prompt, and nothing else.
        """
        gender_bent = gen_file(prompt, photo.url)

        await ctx.send(f'<@{ctx.author.id}> what do you think?', files=[realistic, miyazaki, gender_bent])

bot.start(bot_token)
