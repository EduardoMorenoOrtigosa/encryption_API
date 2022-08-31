from cryptography.fernet import Fernet

class Encrypted_file():

    def __init__(self, file_):
        self.file_ = file_
        self.key = None
        self.encrypted_file = None

    def write_key(self):
        """
        Generates a key and save it into a file
        """
        self.key = Fernet.generate_key()
        #with open("key.key", "wb") as key_file:
            #key_file.write(key)

    def encrypt(self):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        f = Fernet(self.key)

        # file to be encrypted should be the one given by the user
        #with open(self.file_.stream, "rb") as file:
            # read all file data
            #file_data = file.read()
        file_data = self.file_.read()

        # encrypt data
        encrypted_data = f.encrypt(file_data)

        # file to be return is the one the user downloads along the key
        #with open(filename + "_encrypted", "wb") as file:
            #file.write(encrypted_data)

        self.encrypted_file = encrypted_data

    