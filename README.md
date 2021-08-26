# Python-Keylogger
<p>Keylogger im making to learn python</p>
<h2> <b>!! DISCLAIMER !!</b> </h2>
<h3> <b> DONT DO ANYTHING ILLEGAL WITH THIS PROGRAM. THIS IS FOR EDUCATIONAL PURPOSES ONLY. YOU ARE RESPONSIBLE FOR EVERYTHING YOU DO WITH THIS PROGRAM </b> </h3>
<h1> How to use </h1>
<p> Open receiver.py and change the PORT variable to the port you would like the program to listen to. </p>
<p> Open sender.py and change IP and PORT variables to your own ip in the local network and the port you put in the receiver.py</p>

<h2> Modules to install </h2>
<p> "pip install pynput==1.6.8" (1.6.8 because pyinstaller compiling fails with newer versions) </p>
<p> "pip install pyinstaller" (for compiling to exe) </p>

<h2> How to compile to exe? </h2>
<p> Make a folder for sender and receiver... then drag the scripts into the folders </p>
<p> Open cmd and go in the script folder and for both do "pyinstaller --onefile (script.py/pyw)". </p>
<p> Change the sender script to .pyw if you don't want the console to appear </p>
