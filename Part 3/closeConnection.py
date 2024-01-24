import os

connection = "pipe"

if (os.path.isdir(connection)):
    os.rmdir(connection)