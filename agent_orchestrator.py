import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

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

