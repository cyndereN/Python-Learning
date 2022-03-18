import bcrypt
passwd = "testpassword"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
print(salt)
print(hashed)
if bcrypt.checkpw(passwd, hashed):
    print("Successfully match!")
else:
    print("No match")