#!/usr/bin/env python3

from useful.cli import CLI, command, NoMatch
from useful.mlockall import mlockall
from useful.mypipe import MyPipe
from useful.log import Log

from collections import OrderedDict
from subprocess import check_output, Popen, PIPE, CalledProcessError
from getpass import getpass
import socket
import pickle
import atexit
import sys
import os

ENCRYPT = "openssl enc -e -aes-256-cbc -salt -pass fd:{fd} -out {path}"
DECRYPT = "openssl enc -d -aes-256-cbc -salt -pass fd:{fd} -in  {path}"


class Passwords:
  def __init__(self, path, secret):
    assert secret, "password cannot be empty"
    self.log = Log("passwords")
    self.secret = secret.encode()+ b'\n'
    self.passwords = OrderedDict()
    self.path = os.path.expanduser(path)
    if not os.path.exists(self.path):
      return print("No passwords stored yet.\n"
                   "%s will be created on first save" % self.path)

    with MyPipe() as (r,w):
      os.write(w, self.secret)
      try:
        p = Popen(DECRYPT.format(fd=r, path=self.path),
                           shell=True, stdout=PIPE, close_fds=False)
        try:
          self.passwords = pickle.load(p.stdout)
        except EOFError:
          self.log.critical("cannot load db: it is truncated or corrupted")

      except CalledProcessError as err:
        self.log.critical("Can't load DB. Wrong password? %s" % err)
        raise

  def delkey(self, key):
    if key in self.passwords:
      del self.passwords[key]
    self.sync()

  def add(self, key, text):
    if key in self.passwords:
      return print("I will not overwrite key %s" % key)
    self.passwords[key] = text
    self.sync()

  def sync(self):
    with MyPipe() as (r,w):
      os.write(w, self.secret)
      p = Popen(ENCRYPT.format(fd=r, path=self.path),
                shell=True, close_fds=False, stdin=PIPE)
      pickle.dump(self.passwords, file=p.stdin)
      p.stdin.close()


class CLI(CLI):
  def __init__(self, pw):
    super().__init__()
    self.pw = pw

  @command("exit")
  @command("quit")
  def exit(self):
    sys.exit("bye")

  @command("show")
  @command("show all")
  @command("show [key]")
  def show(self, key=''):
    if key == 'all':
      key = ''  # this will match everything
    matched = 0
    for k, v in self.pw.passwords.items():
      if k.find(key) != -1:
        print(k,':', v)
        matched += 1
    if not matched:
      print("<no entries>")

  @command("store [key]")
  def store(self, key):
    if key in self.pw.passwords:
      return print("this key is already in DB\n"
                   "use 'del %s' to delete it." % key)
    print("Press Ctrl+D to finish")
    text = []
    try:
      while True:
        text += [input()]
    except EOFError:
      pass
    print("saving...", end=' ')
    self.pw.add(key, "\n".join(text))
    print("saved")

  @command("del [key]")
  def del_key(self, key):
    self.pw.delkey(key)

  @command("save")
  @command("sync", help="sync changes (mainly for debugging purposes")
  def sync(self):
    self.pw.sync()

  @command("clear", help="clear screen (watch for console history!")
  def clear(self):
    print(chr(27) + "[2J")


if __name__ == '__main__':
  mlockall()  # prevent program from swapping out
  secret = getpass()
  secret = "test"
  if not secret:
    sys.exit("password cannot be empty")
  pw = Passwords(path="~/.passwords", secret=secret)
  cli = CLI(pw)
  atexit.register(cli.clear)
  while True:
    try:
      inpt = input("pwshow> ")
      if inpt:
        cli.run_cmd(inpt)
    except EOFError:
      sys.exit("bye")
    except NoMatch:
      print("unknown command, bro :(")
