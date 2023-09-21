import json

import click
import subprocess
from os import walk
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import isfile
from os.path import relpath
import os

IDA_PATH = "D:\Application\IDA_Pro_7.7\idat64.exe"
IDA_SCRIPT_PATH = './gen_cfg_json.py'
LOG_PATH = "./gen_cfg_log.txt"
JSON_FOLDER_PATH = './JSON/'
idbs_folder = './idbs'


def main():
    try:
        print("[D] IDBs folder: {}".format(idbs_folder))
        success_cnt, error_cnt = 0, 0
        for root, _, files in walk(idbs_folder):
            for f_name in files:
                if (not f_name.endswith(".i64")) and (not f_name.endswith(".idb")):
                    continue

                idb_path = join(root, f_name)
                print("\n[D] Processing: {}".format(idb_path))

                if not isfile(idb_path):
                    print("[!] Error: {} not exists".format(idb_path))
                    continue

                cmd = [IDA_PATH,
                       '-A',
                       '-L{}'.format(LOG_PATH),
                       '-S{}'.format(IDA_SCRIPT_PATH),
                       '-Ojson:{}'.format(JSON_FOLDER_PATH),
                       idb_path]

                print("[D] cmd: {}".format(cmd))

                # get idapython plugin
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()

                if proc.returncode == 0:
                    print("[D] {}: success".format(idb_path))
                    success_cnt += 1
                else:
                    print("[!] Error in {} (returncode={})".format(
                        idb_path, proc.returncode))
                    error_cnt += 1

        print("\n# IDBs correctly processed: {}".format(success_cnt))
        print("# IDBs error: {}".format(error_cnt))

    except Exception as e:
        print("[!] Exception\n{}".format(e))


if __name__ == '__main__':
    main()
