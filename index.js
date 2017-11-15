function isEmpty(obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            return false;
    }

    return JSON.stringify(obj) === JSON.stringify({});
}

const commandLineArgs = require('command-line-args');
const optionDefinitions = [
	{ name: 'infile', alias: 'i', type: String, defaultValue: './fireFTPsites.dat' },
	{ name: 'outfile', alias: 'o', type: String, defaultValue: './FileZillasites.xml' },
	{ name: 'password', alias: 'p', type: String, defaultValue: '' },
	{ name: 'overwrite', alias: 'w', type: Boolean, defaultValue: false }
];
const options = commandLineArgs(optionDefinitions, { partial: true });

var eOL = require('os').EOL;
var kryptos = require('./lib/kryptos/kryptos.js');
var fs = require('fs');

if(!fs.existsSync(options['infile'])) {
	console.log('Input file does not exist');
	process.exit(-1);
}

if(fs.existsSync(options['outfile']) && !options['overwrite']) {
	console.log('Output file already exists');
	process.exit(-1);
}

var obj = JSON.parse(fs.readFileSync(options['infile'], 'utf8'));
var fzxml = '';

if(!isEmpty(obj)) {
	fzxml += '<?xml version="1.0" encoding="UTF-8"?>' + eOL;
	fzxml += '<FileZilla3 version="3.29.0" platform="all">' + eOL;
	fzxml += '    <Servers>' + eOL;

	obj.forEach(function(site) {
		var key = options['password'];
		var cipher = new kryptos.cipher.Blowfish(key, 2, "");
		site['password'] = cipher.decrypt(site['password']);

		if(site['protocol'] === "ftp") {
			site['protocol'] = "0";
		} if(site['protocol'] === "ssh2") {
			site['protocol'] = "1";
		} else {

		}

		if(site['anonymous']) {
			site['anonymous'] = "0";
		} else {
			site['anonymous'] = "1";
		}

		if(site['pasvmode']) {
			site['pasvmode'] = "MODE_PASSIVE";
		} else {
			site['pasvmode'] = "MODE_ACTIVE";
		}

		if(site['treesync']) {
			site['treesync'] = "1";
		} else {
			site['treesync'] = "0";
		}

		fzxml += '        <Server>' + eOL;
		fzxml += '            <Host>' + site['host'] + '</Host>' + eOL;
		fzxml += '            <Port>' + site['port'] + '</Port>' + eOL;
		fzxml += '            <Protocol>' + site['protocol'] + '</Protocol>' + eOL;
		fzxml += '            <Type>0</Type>' + eOL;
		fzxml += '            <User>' + site['login'] + '</User>' + eOL;
		fzxml += '            <Pass encoding="base64">' + new Buffer(site['password']).toString('base64') + '</Pass>' + eOL;
		fzxml += '            <Logontype>' + site['anonymous'] + '</Logontype>' + eOL;
		fzxml += '            <TimezoneOffset>' + site['timezone'] + '</TimezoneOffset>' + eOL;
		fzxml += '            <PasvMode>' + site['pasvmode'] + '</PasvMode>' + eOL;
		fzxml += '            <MaximumMultipleConnections>5</MaximumMultipleConnections>' + eOL;
		fzxml += '            <EncodingType>' + site['encoding'] + '</EncodingType>' + eOL;
		fzxml += '            <BypassProxy>0</BypassProxy>' + eOL;
		fzxml += '            <Name>' + site['account'] + '</Name>' + eOL;
		fzxml += '            <Comments />' + eOL;
		fzxml += '            <Colour>0</Colour>' + eOL;
		fzxml += '            <LocalDir>' + site['localdir'] + '</LocalDir>' + eOL;
		fzxml += '            <RemoteDir>' + site['remotedir'] + '</RemoteDir>' + eOL;
		fzxml += '            <SyncBrowsing>0</SyncBrowsing>' + eOL;
		fzxml += '            <DirectoryComparison>' + site['treesync'] + '</DirectoryComparison>' + eOL;
		fzxml += '        </Server>' + eOL;
	});

	fzxml += '    </Servers>' + eOL;
	fzxml += '</FileZilla3>';
}

fs.writeFile(options['outfile'], fzxml, function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("FireFTP export converted to FileZilla import");
});