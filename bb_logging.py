

def write_log(logfile, msg):
    with open(logfile, "a") as f:
        # print(msg)
        f.write(str(msg))


def write_error_log(logfile, msg):
    with open(logfile, "a") as f:
        # print(msg)
        f.write(str(msg))
