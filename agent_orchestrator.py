import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
# https://platform.openai.com/docs/api-reference/chat/create?lang=python
# the best way of obtaining a json output is using the tools argument within the create
# https://json-schema.org/understanding-json-schema
# https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools
# https://json-schema.org/learn/miscellaneous-examples

# high quality guide https://platform.openai.com/docs/guides/function-calling
# high quality guide https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
company_description = "startup building electric bikes in carbon fiber."
customers = "young professional that have to conmmute, young people that care about the evironment and climate change"
# the paramenters argument of the function is defined as a a json schema object
def read_file(file_name):
    return open(file_name).read()
# ideas_tools =
my_messages = [
    {
        "role": "system",
        "content": "You an honest and helpful assistant  that only outups your respose in strict JSON without any trailing or leading character. Use the functions to provide answers:",
    },
    {"role": "system", "content": "You are an expert  evaluating business ideas"},
    {
        "role": "user",
        "content": f"provide in json format for for the following business {company_description} and this type of customers {customers}",
    },
]

my_tools = (
    [
        {
            "type": "function",
            "function": {
                "name": "get_product_idea",
                "description": f"Provide an useful product ideas for a company with this description {company_description}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "best_idea": {
                            "type": "string",
                            "description": "a product idea that is good for the business to try in addition the product it already has",
                        },
                    },
                    "required": ["best_idea"],
                },
            },
        }
    ],
)
my_tools2 = [
    {
        "type": "function",
        "function": {
            "name": "get_product_idea",
            "description": f"get a list of possible product ideas that match with the business following business dedescription {company_description}",
            "parameters": {
                "type": "object",
                "properties": {
                    "ideas_list": {
                        "type": "array",
                        "description": "list of three of possible product ideas that are an incremental idea of the current products the company has.",
                        "items": {"type": "string"},
                        "prefixItems": [
                            {"type": "string"},
                            {"type": "string"},
                            {"type": "string"},
                        ],
                    }
                },
                "required": ["ideas_list"],
            },
        },
    },
]
my_tool_choice = {"type": "function", "function": {"name": "get_product_idea"}}

completion = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},  # always used in
    temperature=0.2,
    messages=my_messages,
    tools=my_tools2,
    tool_choice=my_tool_choice,
    max_tokens=3000,
)
response = completion.choices[0].message.content

tool_calls_response = completion.choices[0].message.tool_calls
function_args = json.loads(tool_calls_response[0].function.arguments)
print(function_args)
print("finale")

