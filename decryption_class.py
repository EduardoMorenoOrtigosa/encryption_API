from cryptography.fernet import Fernet

class Decrypted_file():

    def __init__(self, file_, key):
        self.file_ = file_
        self.key = key

    def load_key(self):
        """
        Loads the key from the current directory named `key.key`
        """
        return open("key.text", "rb").read()

    def decrypt(self):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        # key file should be the file given by the user 
        f = Fernet(self.key)

        # encrypted data should be the file given by the user 
        with open(self.file_, "rb") as file_r:
            # read the encrypted data
            encrypted_data = file_r.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        #with open(filename, "wb") as file:
        #    file.write(decrypted_data)

        return decrypted_data
