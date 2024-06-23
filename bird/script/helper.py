#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-28

import os
import uuid
import paramiko
from framework.helper import Log


class SSH(object):
    def __init__(self):
        self.ssh_path = os.path.expanduser('~') + '/.ssh'
        self.__SSH_CLIENT__ = {}
        self.__SFTP_CLIENT__ = {}

    def connect(self, ip, user, password, port=22, reconnect=False):
        try:
            if reconnect:
                if ip in self.__SFTP_CLIENT__:
                    try:
                        self.__SFTP_CLIENT__[ip].close()
                    except:
                        pass
                    del self.__SFTP_CLIENT__[ip]
                if ip in self.__SSH_CLIENT__:
                    try:
                        self.__SSH_CLIENT__[ip].close()
                    except:
                        pass
                    del self.__SSH_CLIENT__[ip]

            if ip not in self.__SFTP_CLIENT__:
                s = paramiko.SSHClient()

                if password and len(password) > 0:
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    s.connect(ip, port, user, password, timeout=15)
                else:
                    hpath = os.path.expanduser('~')
                    key = paramiko.RSAKey.from_private_key_file(hpath + '/.ssh/id_rsa')
                    s.load_system_host_keys()
                    s.connect(ip, port, user, pkey=key)

                self.__SSH_CLIENT__[ip] = s
                self.get_sftp(ip)

        except Exception, e:
            Log.log('SSH连接', user, '@', ip, '失败')
            raise e

    def get_ssh(self, ip):
        return self.__SSH_CLIENT__[ip]

    def get_sftp(self, ip):
        sftp = self.__SFTP_CLIENT__.get(ip, None)
        if sftp is None:
            sftp = self.__SSH_CLIENT__[ip].open_sftp()
            self.__SFTP_CLIENT__[ip] = sftp
        return sftp

    def release_all(self):
        for s in self.__SFTP_CLIENT__.values():
            try:
                s.close()
            except:
                pass
        for s in self.__SSH_CLIENT__.values():
            try:
                s.close()
            except:
                pass
        self.__SSH_CLIENT__ = {}
        self.__SFTP_CLIENT__ = {}

    def __write_remote_tmp_sh__(self, ip, lines):
        checkret = '''
REMOTE_SSH_EXEC_RESULT_=$?
if [ ${REMOTE_SSH_EXEC_RESULT_} -ne 0 ]
then
echo "REMOTE_SSH_EXEC_RESULT_=${REMOTE_SSH_EXEC_RESULT_}"
exit ${REMOTE_SSH_EXEC_RESULT_}
fi
'''
        sftp = self.get_sftp(ip)
        remote_path = '/tmp/' + str(uuid.uuid1())
        fo = sftp.open(remote_path, 'w')
        for line in lines:
            fo.write(line)
            fo.write('\n')
        fo.write('\n\n')
        fo.write(checkret)
        fo.write('\n\n')
        fo.write('rm -fr ' + remote_path)
        fo.write('\n\n')
        fo.flush()
        fo.close()
        return remote_path

    def execute_cmd(self, ip, *cmd_list):
        cmd = self.__write_remote_tmp_sh__(ip, cmd_list)
        sclient = self.get_ssh(ip)
        ret = 0
        _, stdout, stderr = sclient.exec_command('sh ' + cmd, get_pty=True)
        lines = []
        for line in stdout:
            line = line.strip()
            lines.append(line)
            if line.find('REMOTE_SSH_EXEC_RESULT_') >= 0:
                ret = int(line.split('=')[1])
        for line in stderr:
            lines.append(line.strip())
            if ret == 0:
                ret = 1
        sclient.exec_command('rm -fr ' + cmd, get_pty=True)
        return ret, '\n'.join(lines)

    def mkdirs(self, ip, mpath):
        if isinstance(mpath, (str, unicode)):
            mpath = [mpath]
        lines = []
        for p in mpath:
            p = os.path.abspath(p)
            cmd = '''if [ ! -d  '%s' ] \n then \n mkdir -p '%s' \n fi\n''' % (p, p)
            lines.append(cmd)
        ret = self.execute_cmd(ip, lines)
        return ret

    def __file_callback__(self, size, filesize):
        pass

    def put_file(self, ip, localpath, remotepath, fun_callback):
        if not fun_callback:
            fun_callback = self.__file_callback__
        sftp = self.get_sftp(ip)
        attrs = sftp.put(localpath, remotepath, callback=fun_callback)
        return attrs.st_size

    def get_file(self, ip, remotepath, localpath, fun_callback):
        if not fun_callback:
            fun_callback = self.__file_callback__
        sftp = self.get_sftp(ip)
        attrs = sftp.get(remotepath, localpath, callback=fun_callback)
        return attrs.st_size
