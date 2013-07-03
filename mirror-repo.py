#!/usr/bin/env python

import psutil
import subprocess
import os
import sys


class MakeRepo():
    def __init__(self):
        self.path = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        self.cmd = "rsync"
        self.repository_url = "rsync://mirror.yandex.ru/centos"
        self.repository_path = "centos"
        self.dry_run = True
        self.delete = False
        self.excludes_file = 'centos_filter.conf'
        self.basic_opts = ['--recursive', '--verbose']
        self.delete_opts = ['--delete', '--delete-during', '--delete-excluded']
        self.dry_run_opts = ['--dry-run']

        if not self.repository_url.endswith('/'):
            self.repository_url += '/'
        if not self.repository_path.endswith('/'):
            self.repository_path += '/'

    def rsync_is_running(self):
        process_list = psutil.get_process_list()

        for process in process_list:
            if process.name == self.cmd:
                if self.repository_url in process.cmdline:
                    if self.repository_path in process.cmdline:
                        # found rsync with same arguments running
                        return True
        # did not find rsync with same arguments
        return False

    def make_command_line(self):
        command_list = [self.cmd]
        command_list.extend(self.basic_opts)
        if self.dry_run:
            command_list.extend(self.dry_run_opts)
        if self.delete:
            command_list.extend(self.delete_opts)
        if self.excludes_file and os.path.isfile(self.excludes_file):
            command_list.append("--exclude-from=" + self.excludes_file)

        command_list.append(self.repository_url)
        command_list.append(self.repository_path)

        return command_list

    def run_rsync(self):
        if not self.rsync_is_running():
            command_list = self.make_command_line()
            print command_list
            subprocess.call(command_list, env={"PATH": self.path})
        else:
            print "Already running!"
            sys.exit(1)


if __name__ == "__main__":
    MR = MakeRepo()
    MR.run_rsync()