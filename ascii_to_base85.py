#!/usr/bin/env python3
"""
ascii_to_base85.py

Converts ASCII text to Base85 encoding.

Usage:
    python ascii_to_base85.py "Hello, World!"
    python ascii_to_base85.py -f input.txt
    echo "Hello, World!" | python ascii_to_base85.py
"""

import argparse
import base64
import sys


def ascii_to_base85(text: str, encoding: str = "ascii") -> str:
    """
    Convert an ASCII string to its Base85-encoded representation.

    Args:
        text: The input string to encode.
        encoding: Text encoding to use before Base85 encoding (default: ascii).

    Returns:
        The Base85-encoded string.

    Raises:
        UnicodeEncodeError: If text contains characters outside the given encoding.
    """
    raw_bytes = text.encode(encoding)
    encoded_bytes = base64.b85encode(raw_bytes)
    return encoded_bytes.decode("ascii")


def base85_to_ascii(encoded_text: str, encoding: str = "ascii") -> str:
    """
    Decode a Base85-encoded string back to its original text.

    Args:
        encoded_text: The Base85-encoded string.
        encoding: Text encoding to use when decoding bytes back to text.

    Returns:
        The decoded original string.
    """
    raw_bytes = base64.b85decode(encoded_text)
    return raw_bytes.decode(encoding)


def main():
    parser = argparse.ArgumentParser(
        description="Convert ASCII text to Base85 encoding (and back)."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to encode. If omitted, reads from --file or stdin.",
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to a file containing text to encode.",
    )
    parser.add_argument(
        "-d", "--decode",
        action="store_true",
        help="Decode a Base85 string back to ASCII instead of encoding.",
    )
    args = parser.parse_args()

    # Determine input source: positional arg > file > stdin
    if args.text is not None:
        input_text = args.text
    elif args.file:
        with open(args.file, "r", encoding="ascii") as f:
            input_text = f.read().rstrip("\n")
    else:
        input_text = sys.stdin.read().rstrip("\n")

    try:
        if args.decode:
            result = base85_to_ascii(input_text)
        else:
            result = ascii_to_base85(input_text)
    except UnicodeDecodeError:
        print("Error: input is not valid Base85-decodable ASCII data.", file=sys.stderr)
        sys.exit(1)
    except UnicodeEncodeError:
        print("Error: input text contains non-ASCII characters.", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
