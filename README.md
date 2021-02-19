# Psu Encrypt 
##### Graduate Student Version (80bit key)
* Graham Seamans
* seamansgraham@gmail.com
### To Run
* Place the key into `./key.txt`
* Place the plaintext into `./plaintext.txt` or the ciphertext into `./ciphertext.txt`
* Run: '`python src/main.py e`' or '`python src/main.py d`' where `e` is encrypt and `d` is decrypt. If you don't provide an arumgent you will be prompted.
* Find the plaintext or cypher text in the appropriate file.
### Notes
* This runs with ASCII encode and decode so things will get weird with UTF-8 files, although the majority of the text will be just fine.

### Included Files
* `./plaintext.txt` - Put the plain text here to encrypt or find it here after decryption.
* `./ciphertext.txt` - Put the cipher text here to decrypt or find it here after encryption.
* `./key.txt` - The key goes here. No '0x' before the key. 80bit key only.
* `./src/main.py` - Takes user input about whether to encrypt and decrypt and interfaces with `cipher.py`
* `./src/cipher.py` - Largely runs the show. Reads and writes to files and calls the `festel.py` with blocks to encrypt or decrypt.
* `./src/festel.py` - The festel cipher. Gets keys from `key.py`. Has the f and g functions. 
* `./src/key.py` - Generates the keys. Makes a list of lists of all subkeys in encrytion order.
* `./src/ftable.py` - The ftable and lookup function.
* `./src/utility.py` - Functions to translate between and combine ascii, hex, binary, binary strings, and such.
