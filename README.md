---
cs140adagide: A super simple IDE for intro C++ classes.
---

The CS140 Adaguide project aims to build a super simple C++ editor for Western Washington University's (WWU) Computer Science Department's "Intro to C++ Programming" course (Course number CSCI140, often called CS140). The editor is meant to be a no frills, simple and intuitive editor, with all of the basic functionality expected.

---
Basic Design
---

We use QT for our window manager, and to help manage processes we execute. We use Scintilla (Of notepad++ fame) for our code editor. Our project uses an MVC design. ProjectModel.py contains the code for managing files. MainWindow.py sets up the main window, Scintilla, other widgets, and the toolbars. Controller.py brings it all togeather. We have two widgets, BuildWidget.py manages compilation and ConsoleWidget.py manages interfacing with the console applications this editor is meant to build.