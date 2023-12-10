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
    "type": "service_account",
    "project_id": "cheatfsusersdb",
    "private_key_id": "c936f544f0aa2ba2881703dee0b251103f8f0168",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJqx/mOObeVW4i\njzcwVg5aGNK92B5XY5S9HUbJkuEAY5ej/Sruyx3iFyu/Jcabtp7+31QPT+YzlF3w\naVHEfnyowBAd85pbp+NteLyZ4FBfKeM7yleyc/Y0QPvs5550K5YtOkDB7ZeqYyTQ\nIUry8HnY7aenGyZFiGNu2GO4JdlC7p3OoiKoAbFfP4kLDzrOzcS5fae/1UNElkV0\nrHpJbBTHsSTJ4Q086XdOE/ef0vnKuezUBVco5xBDCMyQ2SBDaXeWvYSS2JxgYChN\nWcr7eVgwt5XFaaY8ce+xfnz60PUIWtF3jSUxYD5cveV37ALxtCUMPSXUEmPitEZW\n7dqqyK2PAgMBAAECggEAAoMzyAoAcletIhgXr237CstRYNUe96bBdSO2vI8sZ3VW\nL9BZJxV3v1fbjyuY0FrTm0hMA07TBuR70SF2x9RtmCqgaMcerrKmRjhhXSdqyOy8\nLIQGWK5SLG981AREuJzMZ67YnLHpmFFY5ZDsnp85XWcEljPj46zh1EE06Nfr34YU\n3tGgghIEpaQcyjDb7ByWCUg3jd2nKRJCOSAIX1HqKrwCjP8TpmBRh8cEFZKmRqNc\ns9smhc/CLsKWl6mf/Q9PoO7gn/MZh8uC8WB0o6ckL62/Bfntfyr+yXGpK4QU/rb8\nr7pd6FskpwI9bbnKvw9uUlRjtq0BYienXfIJDRpUpQKBgQDkpJ2MP6KQNckUd8n6\nb1d1bTc+NFJdGPMtiEpLSsepcpaxX4EzISr8GKw0vzbCR8BoJtwb2ZWE5aqYRyAu\nuhMuaL+oTGhn6de6WSqsvQn867IDZDuWoNHp5H9aHgDQ4xnaam9r3HdZzyQs3K03\nclcB49wPy/jnvaP9xmdnqB7ZZQKBgQDhzEWzMN4y+8MizgLnVq46pWVYvrWGyTaE\nwYGJputwTV3FZwrWrJs88TKBAe2gTGBoO7VDKPqyjPCrqmEbVdLbNavacrudr71X\nkjyYVMO/V9reL1ftFtihLPRIloCoNO+iVG2h51BbLYlHvsMdYES4AR8S4DZPusOe\nIMf6kfw14wKBgGabpYSCLk8vhAzmcUMtYn91QvxseKYFA2TkrAq8BXx6yzvQk2fB\ns8usuuN1CHsJvkQ/ZDovXFVmyDdMfBncMa17Hr/FgnlXzRN43pjkwS27DIlPGxrP\nE0U24RwtKMqVkE2fxF8QcpNgTWjApA+lBXz4qBKCxDIjvguuVUuEfEutAoGBAMIO\nUQjDwvOGNBrBevVfJbX5V7SBknkYjOZjd/TZpBaMJz70Y/hDt9cUZBdDlPnjKifq\nyMnDelHhlyWx9GsNw33qDpxbZqsK0mtknvc8Qk88Ljot7h8xN1St0fRghIoLlLeq\nX955cjIqXIVwiTfB+M07CX2rfIHhPSW1fqj2tg+JAoGAW58a0kPC9h6/Jwlcf3AF\nq8WVS+H5pGkO4sQ4Rhjl/gB1/Bj9DINoV6y6epWkdbTkCP2abqOwev979H4gcb5K\nlnG8ZGqyeWDurnRLCHtqCYEllnc6qc49F6KKNe2D+hWZmZwXTC+0SvNbnvmLvToC\nGhpBeD60+Md7nDrGZDVZW6s=\n-----END PRIVATE KEY-----\n",
    "client_email": "usercheat@cheatfsusersdb.iam.gserviceaccount.com",
    "client_id": "116682715270260941337",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/usercheat%40cheatfsusersdb.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
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

'''
input_login = 'admin'
input_password = 'admin'
input_id = ''.join(subprocess.check_output('wmic diskdrive get model, SerialNumber').decode().split())

out, lf = loging_in(input_login, input_password, input_id)
print(out)
'''