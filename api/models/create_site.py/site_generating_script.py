import secrets
import re 
# import qr_img from file_with_qr
adress = secrets.token_hex(9)
with open('script_html.html', 'r') as f:
    s = f.read()
string = '<img'+s
with open('{adress}', 'w') as site_html:
    re.sub(r'(<img*?)>', '{string}', s)
    #(.*?)досюда