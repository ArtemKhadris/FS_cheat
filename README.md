# Automatic keystrokes for the game FreeStreet

The work is based on OpenCV. The code looks for these pictures (arrows) in the window and clicks them in the correct order. Various filters are used to improve image search, and limiting the search area to speed up the work. The waiting time before pressing a key is set so that the program's operation is not noticed. Created UI for login and login confirmation.

JPG files - images for searching. Text files - the same pictures, but in a different format. They are all in the pictures.py file. Separately for clarity.

User data was stored in a Google spreadsheet in an encrypted format. No one, not even the administrator, could obtain this data (hard drive number). It was needed for the “one user - one computer” format. The encryption key is stored with the user; if lost, the user must register again.

The login and password were issued by the administrator and entered into a Google spreadsheet; the remaining fields (date of first login, encrypted hard drive number, etc.) were filled in when the user logged in for the first time. Then the user himself came up with his own encryption code.

# ATTENTION
The author of this script DOES NOT RECOMMEND downloading and playing this game (FREESTREET), since this game is pirated content. Original licensed games [PARA-PA City of Dance](https://parapa.ru/) and 5Street. The script does not work with them.
