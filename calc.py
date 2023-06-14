import binascii
import text_to_image
def encoder(file:str,filepath:str):
    print("file recieved")
    print(file)
    filename =file
    extension=filename.rsplit(".")
    finalpath=filepath
    print(finalpath)
    try:
        with open(filename, "rb") as f:
            content=f.read()
            hex_Data=binascii.hexlify(content)
        with open("encryptionfile.txt", 'wb') as f:
            f.write(hex_Data)
        encoded_image_path = text_to_image.encode_file("encryptionfile.txt",finalpath +"/tmp_encrypted."+extension[-1]+".png")    
    except:
        FileNotFoundError

#decoder
def decoder(file:str,filepath:str):
    filetype=file.split(".")
    finalpath=filepath
    decoded_file_path = text_to_image.decode_to_file(file,"decrypted.txt")
    import binascii
    with open("decrypted.txt") as f,open(finalpath +"/decrypted_file"+"."+filetype[1], 'wb') as out:
        for line in f:
            out.write(binascii.unhexlify(''.join(line.split())))