# OBFUS-69 EN & DECODER

**Encode and decode messages using the OBFUS-69 and OBFUS-6969 obfuscation schemes, with AI-assisted decoding powered by your local LLaMA model via Ollama.**

---

## Features

- Encode plaintext into OBFUS-69 or OBFUS-6969 obfuscated messages
- Decode obfuscated messages automatically detecting the mode
- Generate all possible decodings and let your local LLaMA AI pick the most likely meaning
- Configurable to select LLaMA model automatically or manually
- GPU saver modes to skip AI calls when unnecessary
- Fully offline decoding using locally hosted Ollama API

---

## Installation

1. **Install Ollama**

   Download and install Ollama from https://ollama.ai. Ollama is required to run the local LLaMA models for AI decoding.

2. **Download LLaMA model(s)**

   After installing Ollama, open a terminal and run:

   ollama pull llama3.2

   You can choose any model from `llama1` to `llama4` depending on your disk space and performance needs.

3. **Run the script**

   Clone or download this repository and run:

   python obfus69_decoder.py

---

## Usage

- Choose to encode or decode messages.
- When decoding, the script auto-detects whether the message is OBFUS-69 or OBFUS-6969.
- The script generates all possible plaintext combinations and uses LLaMA to pick the best guess.
- Access settings to select the LLaMA model, and enable GPU saver modes to optimize performance.

---

## Configuration

Settings are saved in `~/.obfus69_config.json` in your home directory. You can set:

- **LLaMA model**: Automatically pick the latest model or specify one manually.
- **GPU Saver**: Skip AI calls if only one decoding exists.
- **GPU Saver+**: Always skip AI calls and pick the first decoding.

---

## License & Copyright

© 2025 MrCookie & ChatGPT

This project is licensed under the GNU General Public License v3.0 (GPLv3).

See LICENSE file for details.

---

## Disclaimer

This tool is intended for fun and educational purposes. Use responsibly.
