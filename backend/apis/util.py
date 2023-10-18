import hashlib
import uuid
import jwt
from db.models import *

SECRET_KEY = "secret%^&AMGASDAS!!@#!@#1112"

# generate a token for the given user_id and type
def generate_token(user_id, type):
    data = {
        "user_id": user_id,
        "type": type
    }

    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return token


# decode the given token and return the user object
# the user object can be either a student, supervisor or partner
def decode_token_and_get_user_object(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None

    # now use the user_id and type to obtain this user
    user_id = data["user_id"]
    type = data["type"]

    if type == "stduent":
        student = Student.query.filter_by(student_id=user_id).first()
        return student
    elif type == "supervisor":
        supervisor = Supervisor.query.filter_by(supervisor_id=user_id).first()
        return supervisor
    elif type == "partner":
        partner = Partner.query.filter_by(partner_id=user_id).first()
        return partner
    else:
        return None


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
