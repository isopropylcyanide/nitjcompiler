import sftp
import paramiko
import os
# Copyright (c) 2016 Aman Garg All Rights Reserved.

def_host = "127.0.0.1"
def_username = "new1"
def_pass = "12"


class FileExplorer:
    """
    Python class that handles listing, renaming, viewing,
    deleting, adding of files in user's remote directory through ssh\sftp
    """

    def __init__(self, user, passwd, host_id):
        """Create and return a FileExplorer object"""
        try:
            self.sftp_server = sftp.Server(user, passwd, host_id)
            self.ssh_server = paramiko.SSHClient()
            self.ssh_server.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh_server.connect(host_id, username=user,
                                    password=passwd)
        except Exception as e:
            raise e

    def close(self):
        """Close the connection if it's active"""
        self.sftp_server.close()
        self.ssh_server.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def upload(self, local, remote):
        """sftp: Upload a file to remote directory"""
        self.sftp_server.put(local, remote)

    def download(self, remote, local):
        """sftp: download a file from remote"""
        self.sftp_server.get(remote, local)

    def listfiles(self, root='.'):
        """Recursively list all files and return their tree representation
            which is a hierarchial element
        """
        # Prepare the python module for server upload
        moveFile = 'fileLister.py'
        self.sftp_server.upload('editor/scripts/%s' %
                                (moveFile), "./%s" % (moveFile))

        stdin, stdout, stderr = self.ssh_server.exec_command(
            'python ' + moveFile, bufsize=-1)

        # if stderr is empty, then success
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            raise Exception(error)
        output = ''
        for line in stdout.readlines():
            output += line
        return output
