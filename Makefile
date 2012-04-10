PROJECTDIR = ~/sources/cs140adagide

colorful:
	rm -f $(PROJECTDIR)/resources/icons/theme
	ln -s $(PROJECTDIR)/resources/icons/colorful $(PROJECTDIR)/resources/icons/theme
	pyrcc4 cs140adagide.qrc -o cs140adagide_qrc.py

symbolic:
	rm -f $(PROJECTDIR)/resources/icons/theme
	ln -s $(PROJECTDIR)/resources/icons/symbolic $(PROJECTDIR)/resources/icons/theme
	pyrcc4 cs140adagide.qrc -o cs140adagide_qrc.py
