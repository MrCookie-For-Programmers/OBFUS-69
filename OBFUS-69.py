import requests
import itertools
import re
import os
import json
import random

CONFIG_PATH = os.path.expanduser("~/.obfus69_config.json")

default_config = {
    "llama_model": "auto",  # 'auto' = pick latest
    "gpu_saver": False,
    "gpu_saver_plus": False
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(default_config)
        return default_config
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        print("⚠️ Error reading config. Resetting to default.")
        save_config(default_config)
        return default_config

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

config = load_config()

# === OLD OBFUS-69 MAPPING ===
obfus69_symbol_to_letters = {
    '-': ['a'],
    '?': ['b', 'f', 't'],
    ',': ['c', 'v', 'y'],
    ':': ['d'],
    '2': ['e', 'u'],
    ';': ['g'],
    ')': ['h'],
    '7': ['i'],
    '.': ['j', 'w'],
    '&': ['k'],
    '@': ['l'],
    '‚': ['m'],
    '!': ['n'],
    '9': ['o'],
    '1': ['p'],
    '4': ['q'],
    '/': ['r'],
    '6': ['s'],
    '5': ['x', 'z'],
    ' ': [' ']
}

# === OBFUS-6969 MAPPING ===
obfus6969_symbol_to_letters = {
    '_': ['a'],
    '!': ['b', 'f', 't'],
    ',': ['c', 'v', 'y'],
    '|': ['d'],
    '{': ['e', 'u'],
    '~': ['g'],
    '(': ['h'],
    ')': ['i'],
    '7': ['j', 'w'],
    '.': ['k'],
    '€': ['l'],
    '@': ['m'],
    '‚': ['n'],
    '8': ['o'],
    '9': ['p'],
    '1': ['q'],
    '4': ['r'],
    '/': ['s'],
    '5': ['x', 'z'],
    '6': ['t'],
    '?': [' ']
}

def create_letter_to_symbol_map(symbol_to_letters):
    letter_to_symbol = {}
    for symbol, letters in symbol_to_letters.items():
        for letter in letters:
            if letter not in letter_to_symbol:
                letter_to_symbol[letter] = symbol
    return letter_to_symbol

obfus69_letter_to_symbol = create_letter_to_symbol_map(obfus69_symbol_to_letters)
obfus6969_letter_to_symbol = create_letter_to_symbol_map(obfus6969_symbol_to_letters)

def detect_mode(encoded_message):
    score_69 = sum(1 for ch in encoded_message if ch in obfus69_symbol_to_letters)
    score_6969 = sum(1 for ch in encoded_message if ch in obfus6969_symbol_to_letters)
    return "obfus_6969" if score_6969 > score_69 else "obfus_69"

def encode_message(message, mode="obfus_69"):
    letter_to_symbol = obfus69_letter_to_symbol if mode == "obfus_69" else obfus6969_letter_to_symbol
    encoded = ''
    for char in message.lower():
        encoded += letter_to_symbol.get(char, '?')
    return encoded

def generate_possible_decodings(encoded_message, mode="obfus_69"):
    symbol_to_letters = obfus69_symbol_to_letters if mode == "obfus_69" else obfus6969_symbol_to_letters
    options = []
    for symbol in encoded_message:
        if symbol in symbol_to_letters:
            options.append(symbol_to_letters[symbol])
        else:
            options.append(['?'])
    return [''.join(p) for p in itertools.product(*options)]

def ask_ollama_to_pick_best(possibilities, charset_name="OBFUS-69"):
    slangs = [
        "lol", "brb", "idk", "imo", "wtf", "smh", "tbh",
        "lmao", "rofl", "btw", "omg", "fomo", "ikr", "nvm"
    ]
    
    if config.get("gpu_saver_plus"):
        print("🔋 GPU Saver+ enabled: skipping LLaMA, using first guess.")
        return possibilities[0]

    if config.get("gpu_saver") and len(possibilities) == 1:
        print("♻️ GPU Saver enabled: only one combination, skipping LLaMA.")
        return possibilities[0]

    model_name = get_latest_llama_model()

    prompt = (
        f"I have multiple possible decodings of a message encoded with the {charset_name} character set. "
        "Pick the most likely real English sentence or phrase, considering slang words.\n"
        "Possible slang or informal words include: " + ", ".join(slangs) + ".\n"
        "ONLY respond with the corrected sentence — no explanation.\n\n"
        "Options:\n"
    )
    for i, possibility in enumerate(possibilities[:20], 1):
        prompt += f"{i}. {possibility}\n"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        best_guess = response.json().get('response', '').strip()
        if best_guess:
            return best_guess
        else:
            print("⚠️ LLaMA unclear. Picking random guess.")
            return random.choice(possibilities)
    except Exception as e:
        print("❌ Error talking to Ollama:", e)
        return random.choice(possibilities)

def main_menu():
    while True:
        print("\n=== OBFUS-69 EN & DECODER ===")
        print("1. Encode message")
        print("2. Decode message (auto detect mode)")
        print("3. Exit")
        print("4. Settings")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            print("Choose mode:\n 1 - OBFUS-69\n 2 - OBFUS-6969")
            mode_choice = input("Mode (1 or 2): ").strip()
            mode = "obfus_6969" if mode_choice == '2' else "obfus_69"
            msg = input("Enter text to encode: ")
            result = encode_message(msg, mode=mode)
            print("🔐 Encoded message:\n" + result)

        elif choice == '2':
            encoded = input("Enter encoded message: ").strip()
            mode = detect_mode(encoded)
            possibilities = generate_possible_decodings(encoded, mode)
            print(f"\nDetected mode: {mode.upper()}")
            print(f"Generated {len(possibilities)} combinations. Asking LLaMA...")

            best = ask_ollama_to_pick_best(possibilities, charset_name=mode.upper())
            print("\n🧠 Most likely meaning:")
            print(best)

        elif choice == '3':
            print("Goodbye!")
            break

        elif choice == '4':
            settings_menu()

        else:
            print("Invalid option. Try again.")

def get_latest_llama_model():
    if config["llama_model"] != "auto":
        return config["llama_model"]

    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get('models', [])
        llama_versions = []

        for model in models:
            name = model['name']
            match = re.match(r'(llama)(\d+)', name)
            if match:
                version = int(match.group(2))
                llama_versions.append((version, name))

        if llama_versions:
            latest = max(llama_versions, key=lambda x: x[0])
            print(f"✅ Auto-selected model: {latest[1]}")
            return latest[1]

    except Exception as e:
        print("❌ Could not fetch available models:", e)

    return "llama3"

def settings_menu():
    while True:
        print("\n=== Settings ===")
        print(f"1. LLaMA model (current: {config['llama_model']})")
        print(f"2. GPU Saver (skip LLaMA if only 1 combo): {config['gpu_saver']}")
        print(f"3. GPU Saver+ (always skip LLaMA): {config['gpu_saver_plus']}")
        print("4. Back to main menu")

        choice = input("Choose option to change: ").strip()

        if choice == '1':
            try:
                response = requests.get("http://localhost:11434/api/tags")
                models = response.json().get('models', [])
                print("Available models:")
                for model in models:
                    print(f"- {model['name']}")
                selected = input("Type exact model name (or 'auto'): ").strip()
                config["llama_model"] = selected
                save_config(config)
            except:
                print("❌ Failed to list models.")
        elif choice == '2':
            config["gpu_saver"] = not config["gpu_saver"]
            save_config(config)
        elif choice == '3':
            config["gpu_saver_plus"] = not config["gpu_saver_plus"]
            save_config(config)
        elif choice == '4':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()

