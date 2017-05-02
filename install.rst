How to install
==============

As root on TKLDev:
------------------

USR=/usr/local
TOOLS=$USR/src/tkldev-tools
git clone https://github.com/JedMeister/tkldev-tools.git $TOOLS
cd $TOOLS
for file in bin/*; do ln -s $SRC/$file $TOOLS/$file; done

