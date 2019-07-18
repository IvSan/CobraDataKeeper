# Blockchain data keeper  
**MVP 1.0 Prototype**  
**Project for Vilnius school of AI**  

Software that allows you to store data with proof it will never be changed. Based on Proof-of-Work concept. Blockchain architecture SPA *(single peer application)*.  
All data stored in a single text file next to the script itself. if there is no one new file will be created automatically. If file exists it will be validated and complemented each script run.  

## How to run  

As first step fire `pip install -r requirements.txt`  

To get help `python3 chainer.py -h`  

CLI structure: `python3 chainer.py [-h] [-v] [-n n] [-f filename] [data]`

 - `-h, --help` - argument to get help
 - `-v, --verbose` - use it to get all service information
 - `-n n, --number n` - number of blocks you want to close *(to mine)* for securing the data, higher the number, harder to change data, more secure, optional, default is 1
 - `-f filename, --file filename` - specify the file to read data from and write data to, optional, default filename is `chain`

To read the data file just open it as text with utf-8 encoding.

### Examples
To store two lines `Alice gives Bob exactly 1.238075135 buck` and `Bob confirms` using file `credits.txt` and securing the record with `5` closed blocks the command should be:  
`python3 chainer.py -f credits.txt -n 5 "Alice gives Bob exactly 1.238075135 buck" "Bob confirms"`
