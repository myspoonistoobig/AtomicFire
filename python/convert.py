#!/usr/bin/env python

# Only run from command CLI
if __name__ == "__main__":
	import argparse
	import base64
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

	if os.path.isdir(args.output_file):
		args.output_file = os.path.join(args.output_file, 'FileZillasites.xml')

	if args.crypto_key is None:
		args.crypto_key = "\0"

	with open(args.input_file, 'r') as content_file:
		content = content_file.read()

	json_content = json.loads(content)
	fzxml = '';

	if json_content is not None:
		fzxml += '<?xml version="1.0" encoding="UTF-8"?>' + os.linesep;
		fzxml += '<FileZilla3 version="3.29.0" platform="all">' + os.linesep;
		fzxml += '    <Servers>' + os.linesep;

		for entry in json_content:
			bs = Blowfish.block_size
			key = args.crypto_key.encode()
			ciphertext = bytearray()

			for c in entry['password']:
				ciphertext.append(ord(c))

			iv = b"\0\0\0\0\0\0\0\0"
			cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
			msg = cipher.decrypt(bytes(ciphertext))
			# Make sure we remove null padding that was put in for blowfish
			plaintext = msg.decode('utf-8').replace('\x00', '')
			encoded_bytes = base64.b64encode(plaintext.encode("utf-8"))
			plaintext_encoded = str(encoded_bytes, "utf-8")

			try:
				if entry['protocol'] == "ftp":
					entry['protocol'] = "0"
				elif entry['protocol'] == "ssh2":
					entry['protocol'] = "1"
			except KeyError:
				continue

			try:
				if entry['anonymous']:
					entry['anonymous'] = "0"
				else:
					entry['anonymous'] = "1"
			except KeyError:
				continue

			try:
				if entry['pasvmode']:
					entry['pasvmode'] = "MODE_PASSIVE"
				else:
					entry['pasvmode'] = "MODE_ACTIVE"
			except KeyError:
				continue

			try:
				if entry['treesync']:
					entry['treesync'] = "1"
				else:
					entry['treesync'] = "0"
			except KeyError:
				continue

			fzxml += '        <Server>' + os.linesep
			fzxml += '            <Host>' + entry['host'] + '</Host>' + os.linesep
			fzxml += '            <Port>' + entry['port'] + '</Port>' + os.linesep
			fzxml += '            <Protocol>' + entry['protocol'] + '</Protocol>' + os.linesep
			fzxml += '            <Type>0</Type>' + os.linesep
			fzxml += '            <User>' + entry['login'] + '</User>' + os.linesep
			fzxml += '            <Pass encoding="base64">' + plaintext_encoded + '</Pass>' +os.linesep
			fzxml += '            <Logontype>' + entry['anonymous'] + '</Logontype>' + os.linesep
			fzxml += '            <TimezoneOffset>' + str(entry['timezone']) + '</TimezoneOffset>' + os.linesep
			fzxml += '            <PasvMode>' + entry['pasvmode'] + '</PasvMode>' + os.linesep
			fzxml += '            <MaximumMultipleConnections>5</MaximumMultipleConnections>' + os.linesep
			fzxml += '            <EncodingType>' + entry['encoding'] + '</EncodingType>' + os.linesep
			fzxml += '            <BypassProxy>0</BypassProxy>' + os.linesep
			fzxml += '            <Name>' + entry['account'] + '</Name>' + os.linesep
			fzxml += '            <Comments />' + os.linesep
			fzxml += '            <Colour>0</Colour>' + os.linesep
			fzxml += '            <LocalDir>' + entry['localdir'] + '</LocalDir>' + os.linesep
			fzxml += '            <RemoteDir>' + entry['remotedir'] + '</RemoteDir>' + os.linesep
			fzxml += '            <SyncBrowsing>0</SyncBrowsing>' + os.linesep
			fzxml += '            <DirectoryComparison>' + entry['treesync'] + '</DirectoryComparison>' + os.linesep
			fzxml += '        </Server>' + os.linesep

		fzxml += '    </Servers>' + os.linesep
		fzxml += '</FileZilla3>'

	if (not os.path.exists(os.path.expanduser(args.output_file))) or (os.path.exists(os.path.expanduser(args.output_file)) and args.overwrite_output):
		with open(args.output_file, 'w') as f:
			f.write(fzxml)