import os
import logging
import time
import configure

import re
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
from Crypto.Cipher import AES # pip3 install pycryptodome
import win32crypt # pip3 install pywin32
import hashlib
import requests #pip3 install requests

from datetime import datetime
from requests.cookies import create_cookie

import pickle #pip3 install pickle


USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH_COOKIES = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"%(os.environ['USERPROFILE']))


def get_key():
    try:
        #(1) Get secretkey from chrome local state
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key

    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""



def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_windows_chrome_secrets( ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        return decrypted_pass.decode()
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    

# Path to the Google Chrome Cookies file
# Expand the tilde (~) in the path to the user's home directory
# chrome_cookies_path = "%s/Library/Application Support/Google/Chrome/Default/Cookies" % os.path.expanduser("~")

def populate_chrome_cookies(session, chrome_cookies_path, safeStorageKey, domain=''):
    #print(chrome_cookies_path,safeStorageKey)
	
    # Connect to the SQLite database
    conn = sqlite3.connect(chrome_cookies_path)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to select cookies
    sql_query = f"SELECT name, encrypted_value, host_key, path, expires_utc FROM cookies WHERE host_key LIKE '%{domain}'"

    # Execute the query
    cursor.execute(sql_query)

    # Fetch all the results
    cookies = cursor.fetchall()

    # Print the cookies
    for cookie in cookies:
        name, encrypted_value, host_key, path, expires_utc = cookie
        #print(f"Name: {name}")
        #print(f"Encrypted Value: {encrypted_value}")
        #print(f"Decrypted Value: {decrypt_windows_chrome_secrets(encrypted_value,safeStorageKey)}")
        #print(f"Host: {host_key}")
        #print(f"Path: {path}")
        #print("-" * 20)
        #print(f"Expires (UTC): {get_chrome_datetime(expires_utc)}")
        session.cookies.set_cookie(create_cookie(
            name= name,
            value= decrypt_windows_chrome_secrets(encrypted_value,safeStorageKey),
            domain= host_key,
            path= path,
            expires= expires_utc,
        ))
    # Close the database connection
    conn.close()

    
def complete_relay_state(session,response_text):
    logging.info("*******complete_relay_state**********")
    relay_state = findValue('RelayState',response_text)
    saml_response = findValue('SAMLResponse',response_text)

    response = session.post(url = 'https://idp.federate.amazon.com/api/v1/intermediate/saml',
        data = {
                'RelayState':relay_state,
                'SAMLResponse':saml_response
                }
            )
    csrf_token = findValue('csrf-token', response.text, valueToken="content")
    search_pattern = 'data-employee-id\s*=\s*\'([^\']+)\''
    employee_id =re.search(search_pattern, response.text).group(1)

    logging.info(f'complete_relay_state: csrf_token:{csrf_token} employee-id:{employee_id}')
    return csrf_token,employee_id

def findValue(key_value,string_value,index=0,nameToken="name",valueToken="value"):
    pattstr = f'{nameToken}'+'\s*=\s*\\"' + f'{key_value}' + '\\"\s+'+ f'{valueToken}' +'\s*=\s*\"([^"]+)\\"'
    #print(f"Pattern String = {pattstr}\n")
    find=re.search(pattstr,string_value)
    return find.group(1)

def login(session, username, password):
        global verification_code, employee_id, csrf_token, anti_csrftoken_a2z

        session.headers['User-Agent'] = USER_AGENT

        # Start off with main Web Page
        logging.info(f"0 - Start at Main Web Page")

 
        response = session.get('http://atoz.amazon.work')
        #print(f"Cookies {session.cookies}")
        if ('RelayState' in response.text):
            return complete_relay_state(session, response.text)

        request_context_key = findValue("RequestContextKey",response.text)
        authentication_step = "ENTER_PASSWORD" #findValue("AuthenticationStep",response.text)
        anti_csrftoken_a2z = findValue("anti-csrftoken-a2z",response.text)

        
        logging.info(f'1- Login RequestContextKey:{request_context_key}, AuthenticationStep:{authentication_step} anti=csrftoken-a2z: {anti_csrftoken_a2z}')


        # Deal with Amazon Login Credentials
        response = session.post(url = 'https://idp.amazon.work/idp/enter?sif_profile=amazon-passport',
            data = {
                    'login':username,
                    'password':password,
                    'RequestContextKey':request_context_key,
                    'AuthenticationStep':authentication_step,
                    'anti-csrftoken-a2z':anti_csrftoken_a2z,
                    },
                   )

        if ('RelayState' in response.text):
            return complete_relay_state(session, response.text)
            
        # If we have arrived here - OUR 30 day session has completed.
        # We don't handle this - direct user to use the Browser for 30 day authentication
        logging.info("Session has probably finished - you need to reauthenicate on your webbrowser")
 
def notify_opportunities(announcement):
    print(f"announce_opportunties: '{announcement}'")
    res = requests.post("https://api.notifymyecho.com/v1/NotifyMe",
            json = {
            'accessCode': configure.NOTIFICATIONS_TOKEN,
            'notification': announcement
            }) 
    print(res.text)

if __name__ == '__main__':

    logging.basicConfig(format='%(name)s %(levelname)s: %(asctime)s: %(message)s', level=logging.DEBUG)
    logging.info("Make sure you do not have your chrome browser already running....")
    #announce_opportunties("THESE ARE TEST's")

    session = requests.session()
    for domain in ['amazon.work']:
        logging.info(f"Looking for cookies in {domain}..")
        populate_chrome_cookies(session, CHROME_PATH_COOKIES, get_key(), domain=domain)

    logging.info(f"{session.cookies}")


    pickle_name = 'lastopps.pickle'

    last_hashes = {"last_vto_hash": '',
                    "last_hash":'',
                    "last_accepted_vto_hash": '',
                    "last_active_vto_hash": '',
                    "last_barred_vto_hash":'',

                    "last_vet_hash":'',
                    "last_accepted_vet_hash": '',
                    "last_active_vet_hash": '',
                    "last_update" : ''}


    try:
        last_hashes = pickle.load( open( pickle_name, "rb" ) )
    except:
        pickle.dump( last_hashes, open( pickle_name, "wb" ) )

    time_started = datetime.now()

    last_hash = last_hashes['last_hash']
    print(f"Last hash = {last_hashes['last_hash']}")

    while True:

        csrf_token,employee_id = login(session,configure.ATOZ_USERNAME, configure.ATOZ_PASSWORD)

        logging.info(employee_id)

        while True:    

            response = session.get(url=f'https://atoz.amazon.work/api/v1/opportunities/get_opportunities?employee_id={employee_id}')
            if (response.status_code != 200):
                break

            jResp = response.json()

            sorted_vto = sorted(jResp['vtoOpportunities'], key = lambda i: i['opportunity_id'])
            sorted_vet = sorted(jResp['vetOpportunities'], key = lambda i: i['opportunity_id'])

            num_VETs = len(sorted_vet)
            num_VTOs = len(sorted_vto)

            if ((num_VETs + num_VTOs) == 0):
                logging.info('Zero Sized Opportunities Skipping Checks')
                logging.info(jResp)
                continue

            active_vet = list(filter(lambda _ :  _['active'], sorted_vet))
            active_vto = list(filter(lambda _ :  _['active'], sorted_vto))
            num_active_VETs = len(active_vet) 
            num_active_VTOs = len(active_vto) 

            logging.info(f"#VETS {num_VETs} #VTOS {num_VTOs} #ACTIVE VTOS: {len(active_vto)} #ACTIVE VETS: {len(active_vet)} Employee ID: {employee_id} running {(datetime.now() - time_started)}")
            sorted_opportunities = {'vtoOpportunities':sorted_vto, 'vetOpportunities': sorted_vet}
            opportunities_hash = hashlib.md5(str(sorted_opportunities).encode()).hexdigest()
            if (opportunities_hash != last_hash):
                logging.info("<<<<<<<<There has been a change in opportunties - publish>>>>>>>>>")

                # Note: The if statement below will initiate a Alexa notification on Zero VTOs/VETs
                # Change '>=' for a '>' to only notify on actual active opportunities.
                # You'll also need to keep track of active numbers and send
                # notifications when those numbers increase and not decrease.
               
                if (num_active_VETs + num_active_VTOs >= 0):
                    notify_opportunities(f'There are {num_active_VETs} active VETs and {num_active_VTOs} active VTOs')

                last_hash = opportunities_hash
                last_hashes['last_hash'] = last_hash
                pickle.dump( last_hashes, open( pickle_name, "wb" ) )
 
            time.sleep(5)
