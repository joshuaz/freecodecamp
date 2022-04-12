import hashlib

def crack_sha1_hash(hash, use_salts=False):
    passwords_arr = []
    read_and_add_to_array("top-10000-passwords.txt", passwords_arr)
    
    if use_salts:
        top_salts = []
        top_salts_passwords = {}
        read_and_add_to_array("known-salts.txt", top_salts)
        for bsalt in top_salts:        #bsalts and bpassword because it's in bytes
            for bpassword in passwords_arr:
                prepended = hashlib.sha1(bsalt + bpassword).hexdigest()
                appended = hashlib.sha1(bpassword + bsalt).hexdigest()
                top_salts_passwords[prepended] = bpassword.decode("utf-8")
                top_salts_passwords[appended] = bpassword.decode("utf-8")
        if hash in top_salts_passwords:
            return top_salts_passwords[hash]

    passwords_dict = {}
    for p in passwords_arr:
        hash_line = hashlib.sha1(p).hexdigest()
        passwords_dict[hash_line]= p.decode("utf-8") #bytes are encoded, so we have to decode
    
    if hash in passwords_dict:
        return passwords_dict[hash]
    return "PASSWORD NOT IN DATABASE"

def read_and_add_to_array(file_name, arr):
    with open(file_name, "rb") as f: #rb changes text to bytes
        line = f.readline().strip() #stripping because there's a \n at the end of each line
        while line:
            arr.append(line)
            line = f.readline().strip() 