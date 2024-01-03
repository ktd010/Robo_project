import json

# Your ChatCompletionMessage object
chat_completion_message = ChatCompletionMessage(content='{\n  "fork": 1,\n  "plate": 1,\n  "spoon": 1}', role='assistant', function_call=None, tool_calls=None)

# Extract the content from the message
content_str = chat_completion_message.content

# Parse the content string as a Python dictionary
content_dict = json.loads(content_str)

# Now, content_dict contains the parsed content as a Python dictionary
print(content_dict)

