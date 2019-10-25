# AtomicFire
This script is designed to help you convert [FireFTP](http://fireftp.net/) export files into [FileZilla](https://filezilla-project.org/) Site Manager import files.

### A Note on Passwords and Security

The script decrypts the Blowfish encrypted passwords to plaintext and then base64 encodes them for the FileZilla import format. base64 is not a suitable format for securely encrypting passwords. Online tools and functions built into nearly every programming language make decoding base64 a trivial task. Therefore, it is not recommended that you store the FileZilla import file for any extended period of time. It is also recommended that you exclude the resulting export file from any source repositories. This tool should be used to convert your data and then the intermediate files should be discarded.

### Prerequisites
1. Python 3+. The actual use and scope of this tool is not exhaustive enough for it to be worthwhile to support older versions.
2. A FireFTP export file. The default name for this is usually fireFTPsites.dat. See Additional Considerations below if you were unable to export a file in advance of the Firefox upgrade and need pointers on how to get to a point where you can export from FireFTP.
3. This script.
4. Basic command line knowledge.

### Python Dependencies
- [PyCryptodome](https://github.com/Legrandin/pycryptodome)

All requirements can be installed using the command below if I did not package the dependencies correctly.

```
$ pip install -r requirements.txt
```

### Exporting Your Sites from FireFTP
1. Open a browser that is still capable of running the legacy FireFTP.
2. Open a new instance of FireFTP.
3. Click the Tools menu item (it is usually located at the far right).
4. Choose Export... from the Tools menu.
5. Save your FireFTP export .dat file in a location you will remember.
6. You may optionally encrypt the passwords in your .dat file with a password. Leave this field blank or choose a password. The conversion script has support for either option.

### Usage
1. Download or clone this project to your local computer.

From the command line:
```
$ git clone https://github.com/myspoonistoobig/AtomicFire.git
```

2. Unzip and/or change into the directory.

From the command line:
```
$ cd AtomicFire/python/
```

3. Run this script.

From the command line:
```
$ python convert.py
```

Use the command line arguments below.

`-i [path to your fireFTPsites.dat file]` or `--input [path to your fireFTPsites.dat file]`

Include the full path to your FireFTP export file. If you do not supply the i argument, the script assumes there is a file named fireFTPsites.dat in the same directory as index.js.

`-o [path and file name where you want your FileZilla import file to save]` or '`--output [path and file name where you want your FileZilla import file to save]`

Include the full path and desired file name where your FileZilla import XML file will be written. If you do not supply the o argument, the script will write FileZillasites.xml to the same directory as index.js.

If you do not supply the w argument below and the output file already exists, the script will exit instead of overwriting the existing file.

`-w` or `--overwrite`

This option allows the script to overwrite any existing output files that may have the same name and location as the one specified in the arguments.

`-k [your password]` or `--key [your password]`

If you used a password/key to protect your export from FireFTP you need to specify the k argument with the password used during export. No password is the default, just like the FireFTP export. Any special characters you have used in your password may need escaped on the command line. Use quotes around your password if you have special characters or spaces.

**Usage Example:**
```
$ python convert.py -i ~/Desktop/fireFTPsites.dat -o ~/Desktop/FileZillasites.xml -w -k "supersecretpassword1 @!"
```

The resulting output file should be ready for import into FileZilla via the File -> Import... menu.

### Additional Considerations

This tool has potential uses outside my personal reason for creating it. For instance, it would also be useful for any decision to migrate to FileZilla from FireFTP independent of the Firefox updgrade. The tool should work with exports generated from FireFTP installed on Firefox, Waterfox, or any other Firefox derivative that supports legacy Firefox extensions.

This script was written for FireFTP version 2.031 and FileZilla version 3.29.0. Brief research into import and export methods for both tools reveals past differences from current functionality. This script may or may not work with past or future versions of either solution.

Other tools may be capable of importing FileZilla import files in FileZilla's XML format. The output of this script should work for any app or script that accepts these XML files.

In the process of digging through FireFTP export and import source code I saw that it specifies arc4 (RC4) encryption routines in some places. I don't think these are generally used in the current export. It may be legacy code. Thus, there is no support in my script for the arc4 methods.

**If you did not backup your FireFTP sites before Firefox automatically installed version 57:**
Your profile and legacy extensions may still be intact. You may be able to install a Firefox fork such as [Waterfox](https://www.waterfoxproject.org/), as recommended by FireFTP's developer. Waterfox has the ability to import data from your Firefox profile. This is how I recovered my site data. Waterfox pulled in my old profile and all of my saved FireFTP sites. From Waterfox I was able to export my FireFTP sites for conversion. See the FireFTP export instructions above if you are unfamiliar with the process.

If Waterfox or another Firefox derivative is unable to load your profile and legacy extensions, a partial file containing your site data may still be available in your old profile directory. More information for finding your profile location can be found at [https://support.mozilla.org/kb/profiles-where-firefox-stores-user-data#w_how-do-i-find-my-profile](https://support.mozilla.org/kb/profiles-where-firefox-stores-user-data#w_how-do-i-find-my-profile). In your profile folder there may be a file named fireFTPsites.dat. This file does not contain any stored password information but it may hold your other site data and credentials still.
