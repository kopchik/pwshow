pwshow
======

Yet another CLI password manager with interactive interface.
Example:

~~~
ux32vd@pwshow$ ./pwshow.py
No passowords stored yet.
~/.passwords will be created on first save
pwshow> show all
<no entries>
pwshow> store test1
Press Ctrl+D to finish
asdfasdf
pwshow> store test2
Press Ctrl+D to finish
privet, isden
pwshow> store multiline
Press Ctrl+D to finish
this is line one
this is line two
pwshow> show test
test1 : asdfasdf
test2 : privet, isden
pwshow> show all
test1 : asdfasdf
test2 : privet, isden
multiline : this is line onethis is line two
pwshow> quit
bye
~~~

As you see, in this revision multi-line output was broken :)