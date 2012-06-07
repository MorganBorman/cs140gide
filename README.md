---
140gide: A super simple IDE for intro C++ classes.
---

The 140gide project aims to build a super simple C++ editor for Western 
Washington University's (WWU) Computer Science Department's "Intro to C++ Programming" 
course (Course number CSCI140, often called CS140). The editor is meant to be a no frills, 
simple and intuitive editor, with all of the basic functionality expected.

---
Basic Design
---

We are using the QT toolkit to build our GUI, and to help manage processes we execute. 
We use Scintilla (Of notepad++ and gedit fame) for our code editor. 
Our project uses an rough MVC design and is composed of the following components.

* ProjectModel.py contains the code for managing files. 
* MainWindow.py sets up the main window, Scintilla, other widgets, and the toolbars. 
* Controller.py contains application level logic to tie all the separate components together. 
* BuildWidget.py manages running the compilation process.
* ConsoleWidget.py manages interfacing with the users compiled programs.