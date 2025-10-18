import pyperclip
import keyboard
import time
import os
import traceback
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from models import RewrittenTextModel


# ----------------------------- #
# 🧩 INITIAL SETUP
# ----------------------------- #

load_dotenv()

LOG_FILE = "fluenter_log.log"


def log_message(msg: str, is_error: bool = False):
    """Write messages or errors to log file with timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        level = "ERROR" if is_error else "INFO"
        f.write(f"[{timestamp}] [{level}] {msg}\n")
    if is_error:
        print(f"⚠️ {msg}")
    else:
        print(f"✅ {msg}")


# ----------------------------- #
# ⚙️ INITIALIZE LLM + PROMPTS
# ----------------------------- #

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = PydanticOutputParser(pydantic_object=RewrittenTextModel)

    taglish_prompt = PromptTemplate(
        input_variables=["input"],
        template=(
            "Convert the given English text into its Tamil Romanized (Taglish) form.\n"
            "Return the output strictly as JSON following this schema:\n{format_instructions}\n\n"
            "Text:\n{input}"
        ),
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    english_prompt = PromptTemplate(
        input_variables=["input"],
        template=(
            "Correct the given English text for spelling and grammar mistakes.\n"
            "Return the output strictly as JSON following this schema:\n{format_instructions}\n\n"
            "Text:\n{input}"
        ),
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    taglish_chain = LLMChain(llm=llm, prompt=taglish_prompt)
    english_chain = LLMChain(llm=llm, prompt=english_prompt)

    log_message("LLM initialized successfully.")
except Exception as e:
    log_message(f"Failed to initialize LLM: {e}\n{traceback.format_exc()}", is_error=True)
    raise SystemExit("❌ Failed to initialize LLM. Check your .env or internet connection.")


# ----------------------------- #
# 🧾 PROCESSING FUNCTION
# ----------------------------- #

def process_clipboard(chain, mode_name: str):
    """Process clipboard text through the given LangChain."""
    try:
        clipboard_text = pyperclip.paste().strip()
        if not clipboard_text:
            log_message("Clipboard is empty, skipping.", is_error=True)
            return

        log_message(f"Processing {mode_name} for text: {clipboard_text[:50]}...")

        # Run the model
        output = chain.run(input=clipboard_text)

        # Parse structured output
        parsed = parser.parse(output)
        rewritten_text = parsed.rewritten_text.strip()

        if not rewritten_text:
            raise ValueError("Model returned empty text.")

        # Copy rewritten text back to clipboard and paste
        pyperclip.copy(rewritten_text)
        time.sleep(0.15)
        keyboard.press_and_release("ctrl+v")

        log_message(f"{mode_name} complete. Result: {rewritten_text[:80]}")

    except KeyboardInterrupt:
        log_message("Keyboard interrupt detected, exiting gracefully.")
        raise

    except Exception as e:
        log_message(f"Error during {mode_name}: {e}\n{traceback.format_exc()}", is_error=True)


# ----------------------------- #
# 🎧 HOTKEY SETUP
# ----------------------------- #

def main():
    print("=" * 60)
    print("🪄 Fluenter Assistant is running")
    print("Press Ctrl+T → Convert to Tamil (Taglish)")
    print("Press Ctrl+G → Correct English")
    print("Press Ctrl+Shift+Backspace → Exit")
    print("=" * 60)

    log_message("Service started. Waiting for hotkeys...")

    # Add hotkeys
    keyboard.add_hotkey("ctrl+t", lambda: process_clipboard(taglish_chain, "Taglish Conversion"))
    keyboard.add_hotkey("ctrl+g", lambda: process_clipboard(english_chain, "English Correction"))

    try:
        keyboard.wait("ctrl+shift+backspace")
    except KeyboardInterrupt:
        pass
    finally:
        log_message("Service stopped by user.")
        print("\n🛑 Exiting Fluenter Assistant.")


# ----------------------------- #
# 🚀 ENTRY POINT
# ----------------------------- #

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"Fatal error: {e}\n{traceback.format_exc()}", is_error=True)
        print("❌ Fatal error. Check fluenter_log.log for details.")
