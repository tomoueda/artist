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

@bot.command(
    name="anime",
    description="I'll turn a photo you drop into an anime picture",
    options=[interactions.Option(name='photo', description="your photo here", type=interactions.OptionType.ATTACHMENT)],
)
async def anime(ctx: interactions.CommandContext, photo):
    await ctx.defer()
    if photo.url:
        image_url = photo.url 
        model = 'gpt-4-vision-preview'
        prompt = """
        Give me a prompt for DALL-E to use to reproduce this image. Describe the image in great detail, as DALL-E will not be able to see the original image. 
        Describe the image as if the subject(s) in it are anime characters in style of Yusuke Kozaki. Ensure you include pertinent details like what direction the subject is facing, 
        what kinds of clothing or jewelry they're wearing, if they're wearing glasses (and what those look like), what their facial expressions are,
        how they're posing, and what their background is. If the subject appears to be human, be sure to include their gender and skin color as well. 
        Only return the DALL-E prompt, and nothing else.
        """
        messages = [{'role': 'user', 'content': [{'type': 'text', 'text': prompt}, {'type': 'image_url', 'image_url': {'url': image_url}}]}]
        response = client.chat.completions.create(model=model, messages=messages, max_tokens=1024)
        message = response.choices[0].message
        response = client.images.generate(model='dall-e-3', prompt=message.content, quality='hd', n=1, response_format='b64_json')
        image1 = base64.b64decode(response.data[0].b64_json)
        response = client.images.generate(model='dall-e-3', prompt=message.content, quality='hd', n=1, response_format='b64_json')
        image2 = base64.b64decode(response.data[0].b64_json)
        stream1 = io.BytesIO(image1)
        stream2 = io.BytesIO(image2)
        file1 = interactions.File('image1.png', fp=stream1)
        file2 = interactions.File('image2.png', fp=stream2)


        prompt = """
        Give me a prompt for DALL-E to use to reproduce this image. Describe the image in great detail, as DALL-E will not be able to see the original image. 
        Describe the image as if the subject(s) in it are anime characters in style of Yusuke Kozaki. Ensure you include pertinent details like what direction the subject is facing, 
        what kinds of clothing or jewelry they're wearing, if they're wearing glasses (and what those look like), what their facial expressions are,
        how they're posing, and what their background is. If the subject appears to be human, be sure to swap their gender but keep the same skin color. 
        Only return the DALL-E prompt, and nothing else.
        """
        messages = [{'role': 'user', 'content': [{'type': 'text', 'text': prompt}, {'type': 'image_url', 'image_url': {'url': image_url}}]}]
        response = client.chat.completions.create(model=model, messages=messages, max_tokens=1024)
        message = response.choices[0].message
        response = client.images.generate(model='dall-e-3', prompt=message.content, quality='hd', n=1, response_format='b64_json')
        image3 = base64.b64decode(response.data[0].b64_json)
        stream3 = io.BytesIO(image3)
        file3 = interactions.File('image3.png', fp=stream3)

        await ctx.send(f'<@{ctx.author.id}> what do you think?', files=[file1, file2, file3])

bot.start(bot_token)
