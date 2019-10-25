#!/usr/bin/env python
import argparse
import json
from Crypto.Cipher import Blowfish

# Get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', action='store', dest='input_file', help='Specify an input file with full file path')
parser.add_argument('-o', '--output-directory', action='store', dest='output_directory', help='The directory to output the result')
parser.add_argument('-k', '--key', action='store', dest='crypto_key', help='Key')
args = parser.parse_args()

if __name__ == "__main__":
	with open(args.input_file, 'r') as content_file:
		content = content_file.read()

	if args.crypto_key is None:
		args.crypto_key = "\0"

	json_content = json.loads(content)

	for entry in json_content:
		bs = Blowfish.block_size
		key = args.crypto_key.encode()
		ciphertext = bytearray()

		for c in entry['password']:
			ciphertext.append(ord(c))

		iv = b"\0\0\0\0\0\0\0\0"
		cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
		msg = cipher.decrypt(bytes(ciphertext))
		plaintext = msg.decode('utf-8')


