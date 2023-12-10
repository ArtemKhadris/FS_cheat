import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import subprocess
from urllib.request import urlopen
from datetime import datetime, timedelta
import cryptocode

def loging_in(input_login, input_password, input_id, key1, key2):
    input_login = str(input_login)
    input_password = str(input_password)
    input_id = str(input_id)
    credentials = {
        # INFORMATION FOR SYNCHRONIZING USER DATA FROM GOOGLE TABLES
    "type": "---",
    "project_id": "---",
    "private_key_id": "---",
    "private_key": "-----BEGIN PRIVATE KEY-----\---\n-----END PRIVATE KEY-----\n",
    "client_email": "---",
    "client_id": "---",
    "auth_uri": "---",
    "token_uri": "---",
    "auth_provider_x509_cert_url": "---",
    "client_x509_cert_url": "---",
    "universe_domain": "---"
    }
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(credentials)
    sheet = client.open("UsersFS").sheet1
    df = pd.DataFrame(sheet.get_all_records())

    output = ''

    cur_date = urlopen('http://just-the-time.appspot.com/')
    cur_date = cur_date.read().strip()
    cur_date = cur_date.decode('utf-8')
    cur_date = datetime.strptime(cur_date, '%Y-%m-%d %H:%M:%S')
    cur_date = cur_date.date()
    
    log_flag = False
    # Check if login exists in the DataFrame
    if input_login not in df['login'].values:
        output = 'Wrong login'
    else:
        # Filter the DataFrame based on the login
        filtered_df = df[df['login'] == input_login]

        # Check if the password is correct
        if input_password != str(filtered_df['password'].iloc[0]):
            output = 'Wrong password'
        else:
            if key1 != key2:
                output = 'Your keys are different'
            else:
                # Check if the user is banned
                if str(filtered_df['ban'].iloc[0]) == str(1):
                    output = 'You are banned, contact the administration if you do not agree'
                else:
                    # Check if the ID matches
                    if input_id != cryptocode.decrypt(str(filtered_df['id'].iloc[0]),key1) and str(filtered_df['id'].iloc[0]) != str(0):
                        # Set the banned status to 1
                        df.loc[df['login'] == input_login, 'ban'] = str(1)
                        df.loc[df['login'] == input_login, 'id_ban'] = cryptocode.encrypt(input_id,key1)
                        df.loc[df['login'] == input_login, 'date_ban'] = str(cur_date)
                        df.loc[df['login'] == input_login, 'key'] = key1
                        output = 'Your ID does not match. \nYou are now banned. \nСontact the administration if you do not agree'
                    elif input_id != cryptocode.decrypt(str(filtered_df['id'].iloc[0]),key1) and str(filtered_df['id'].iloc[0]) == str(0):
                        df.loc[df['login'] == input_login, 'id'] = cryptocode.encrypt(input_id,key1)
                        output = 'Your ID has been updated.'
                        # Check if the subscription has expired
                        if cur_date > datetime.strptime(str(filtered_df['date_sub'].iloc[0]), '%Y-%m-%d').date() and datetime.strptime(str(filtered_df['date_sub'].iloc[0]), '%Y-%m-%d').date() != datetime.strptime('2000-01-01', '%Y-%m-%d').date():
                            output += '\nYour subscription is over'
                        elif datetime.strptime(str(filtered_df['date_sub'].iloc[0]), '%Y-%m-%d').date() == datetime.strptime('2000-01-01', '%Y-%m-%d').date():
                            df.loc[df['login'] == input_login, 'date_sub'] = str(cur_date + timedelta(days=30))
                            output += '\nLogin successful\nWelcome, Newcomer!'
                            log_flag = True
                    else:
                        # Check if the subscription has expired
                        if cur_date > datetime.strptime(str(filtered_df['date_sub'].iloc[0]), '%Y-%m-%d').date() and datetime.strptime(str(filtered_df['date_sub'].iloc[0]), '%Y-%m-%d').date() != datetime.strptime('2000-01-01', '%Y-%m-%d').date():
                            output = 'Your subscription is over'
                        else:
                            output = 'Login successful\nWelcome back!'
                            log_flag = True

    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    return output, log_flag
