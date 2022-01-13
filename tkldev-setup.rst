Setup a new TKLDev
==================

This is my (Jeremy's) personal workflow when I initially set up a new TKLDev.
I think it's a pretty sane path to get things set up ready to go, but YMMV.

Within this doc I will use variables for name and email. To make things super
easy, if you set these variable first, then you can copy paste the commands
that are in this doc::

    export NAME="Your Name"
    export EMAIL="you@example.com"

Be sure to replace "Your Name" & "you@example.com" with your actual name (or
nickname) and email respectively. These will be displayed within GitHub.

generate new ssh keypair
------------------------

I highly recommend generating an RSA ed25519 keypair::

    ssh-keygen -t ed25519 -C "$EMAIL"

register your key with GitHub
-----------------------------

Assuming that you wish to push code back to GitHub, if you don't already have
an account, `sign up`_. Otherwise log in and browse to:

    https://github.com/settings/keys 

Then click the "New SSH key" button. Enter a title for your key and in the
'Key' box, paste the contents of the relevant public key file. E.g. if you
followed my advice above, paste the output of::

    cat ~/.ssh/id_ed25519.pub

If you generated a "standard" RSA keypair, then this will give you the
relevant text to paste::

    cat ~/.ssh/id_rsa.pub

install these tools
-------------------

Please see https://github.com/JedMeister/tkldev-tools/blob/master/install.rst

git config
----------

::

    git config --global user.email "$EMAIL"
    git config --global user.name "$NAME"

install additional useful packages
----------------------------------

I use these lots, so always install them (note all TurnKey apps include
'vim-tiny', this will install full vim::

    apt update -qq
    apt install -y tree vim


.. _sign up: https://github.com/signup
