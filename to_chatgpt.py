
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv


from collections import Counter
import json


def to_chat_gpt(objects):
    '''
    TODO Needs work. Don't have API tokens available to check out response.
    After receiving response, will need to arrange response into a dictionary, containing:
    {'object': 'position'}
    This will be used for LangSAM

    '''

    n = len(objects)
    object_counts = Counter(objects)

    num_objects = []
    for idx, (element, count) in enumerate(object_counts.items()):
        s = 's' if count > 1 else ''
        last_word = 'and ' if idx ==n else ''
        num_objects.append(f'{last_word}{count} {element}{s}')


    num_objects = ', '.join(num_objects)

    description = f"There are {n} items: " + num_objects + "."

    load_dotenv()

    client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Declare prompt2 as a global variable

    async def main() -> None:
        global chatgpt_response

        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{description}" + \
                        "If we use western customs, what is the correct placement of these items? Please write the placement in the form of tuples. \
                        That is, (item, location), where location is the general location inside of a 600x600 image. \n \
                        Additionally, feel free to discard any item you don't see as fitting. When we exclude an item, you could just write (item, exclude)."
                      ,
                }
            ],
            model="gpt-3.5-turbo",
        )
        
        completion_content = chat_completion.choices[0].message.content
        #print(completion_content)
        chatgpt_response = completion_content

    # Run the main function
    asyncio.run(main())

    # Now, prompt2 is accessible globally with the updated content_dict
    print(chatgpt_response)

    return chatgpt_response

to_chat_gpt(['plate', 'spoon', 'fork', 'knife'])