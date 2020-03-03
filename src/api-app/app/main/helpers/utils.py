import hashlib
import os
from flask_restful import abort


def abort_if_doesnt_exist(id):
    abort(404, message="{} Doesn't exist".format(id))


def not_supported():
    abort(501, message="Not implemented yet")    

def resource_exists():
    abort(409, message="Resource already exists")    

def validation_error(message):
    abort(500, message=message)    


def getHashOfFile(filename):
	return hashlib.md5(open(filename,'rb').read()).hexdigest()

def deleteFile(filename):
	os.remove(filename)