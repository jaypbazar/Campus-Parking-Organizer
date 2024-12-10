import mysql.connector, hashlib

def connectSQL():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "se_database"
    )

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()
