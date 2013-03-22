#!/usr/bin/env python3

from useful.cli import CLI, command, NoMatch
from collections import OrderedDict
import pickle
import sys
import os


class Passwords:
  def __init__(self, path="~/.passwords"):
    self.passwords = OrderedDict()
    self.path = os.path.expanduser(path)
    try:
      with open(self.path, 'rb+') as fd:
        raw = b""
        chunk = True
        while chunk:
          chunk = fd.read()
          raw += chunk
      # TODO: here some crypto routines
      if raw:
        self.passwords = pickle.loads(raw)
    except FileNotFoundError:
      print("No passowords stored yet.\n"
            "%s will be created on first save" % path)

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
    to_encrypt = pickle.dumps(self.passwords)
    # TODO: here is strong encryption
    raw = to_encrypt
    with open(self.path, 'wb') as fd:
      written = fd.write(raw)
      assert written == len(raw)
      os.fdatasync(fd.fileno())


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
      if k.startswith(key): 
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
    self.pw.add(key, "\n".join(text))

  @command("del [key]")
  def del_key(self, key):
    self.pw.delkey(key)


if __name__ == '__main__':
  pw = Passwords()
  cli = CLI(pw)
  while True:
    try:
      inpt = input("pwshow> ")
      cli.run_cmd(inpt)
    except EOFError:
      sys.exit("bye")
    except NoMatch:
      print("unknown command, bro :(")