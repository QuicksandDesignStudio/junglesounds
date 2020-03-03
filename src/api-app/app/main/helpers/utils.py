

def abort_if_doesnt_exist(id):
    abort(404, message="{} Doesn't exist".format(id))


def not_supported():
        abort(501, message="Not implemented yet")    