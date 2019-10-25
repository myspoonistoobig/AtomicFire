#!/usr/bin/env python

# Only run from command CLI
if __name__ == "__main__":
	import argparse
	import json
	import os
	from Crypto.Cipher import Blowfish

	# Get command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', action='store', dest='input_file', help='Specify a FireFTP export file')
	parser.add_argument('-o', '--output', action='store', dest='output_file', help='Specify a path and file name for the FileZilla XML import')
	parser.add_argument('-k', '--key', action='store', dest='crypto_key', help='Specify the Key used to encrypt the FireFTP export')
	parser.add_argument('-w', '--overwrite', action='store_true', dest='overwrite_output', help='Overwrite any file with the same name as the specified output file')
	args = parser.parse_args()

	# Quick configuration from command line options
	if args.input_file is None:
		print('No input file specified')
		sys.exit(128)

	if not os.path.exists(os.path.expanduser(args.input_file)):
		print('Specified file does not exist')
		sys.exit(128)

	if args.output_file is None:
		args.outputfile = './FileZillasites.xml'

	if args.crypto_key is None:
		args.crypto_key = "\0"

	with open(args.input_file, 'r') as content_file:
		content = content_file.read()

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
		print(plaintext)


