import hashlib
import uuid

# hash the given file, keep the original extension
# reference: https://www.programiz.com/python-programming/examples/hash-file
def get_hash_filename(file):
    # get original filename
    old_filename = file.filename

    # get the file extension
    extension = old_filename.split(".")[-1]

    # calculate the hash for the file
    filehash = hashlib.sha256()

    # read chunk by chunk, each chunk is 1024 bytes
    for chunk in iter(lambda: file.read(1024), b""):
        filehash.update(chunk)

    # reset the file pointer to the beginning
    file.seek(0)

    # get the final hash value.
    # in case the same file is uploaded multiple times, the hash value should be different
    new_filename = "{}_{}.{}".format(filehash.hexdigest(), uuid.uuid4().hex, extension)
    return new_filename
