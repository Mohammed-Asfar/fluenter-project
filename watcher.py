import pyperclip
import keyboard
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from models import RewrittenTextModel
import time

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Pydantic parser
parser = PydanticOutputParser(pydantic_object=RewrittenTextModel)

# Prompt for Taglish conversion
taglish_prompt = PromptTemplate(
    input_variables=["input"],
    template=(
        "Convert the given English text into its Tamil Romanized (Taglish) form.\n"
        "Return the output strictly as JSON following this schema:\n{format_instructions}\n\n"
        "Text:\n{input}"
    ),
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

taglish_chain = LLMChain(llm=llm, prompt=taglish_prompt)

# Prompt for English correction
english_prompt = PromptTemplate(
    input_variables=["input"],
    template=(
        "Correct the given English text for spelling and grammar mistakes.\n"
        "Return the output strictly as JSON following this schema:\n{format_instructions}\n\n"
        "Text:\n{input}"
    ),
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

english_chain = LLMChain(llm=llm, prompt=english_prompt)


def process_clipboard(chain):
    clipboard_text = pyperclip.paste()
    if not clipboard_text:
        print("Clipboard is empty.")
        return

    # Run LLM chain
    output = chain.run(input=clipboard_text)

    # Parse structured output
    parsed: RewrittenTextModel = parser.parse(output)
    rewritten_text = parsed.rewritten_text
    print("Rewritten text:", rewritten_text)

    # Copy rewritten text to clipboard
    pyperclip.copy(rewritten_text)
    time.sleep(0.1)
    keyboard.press_and_release("ctrl+v")


# Hotkeys
keyboard.add_hotkey("ctrl+t", lambda: process_clipboard(taglish_chain))
keyboard.add_hotkey("ctrl+g", lambda: process_clipboard(english_chain))

print(
    "Press Ctrl + T to convert to Taglish, Ctrl + G to correct English. Press ctrl+shift+backspace to exit."
)
keyboard.wait("ctrl+shift+backspace")
