#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main() {

 string input = "";

 // How to get a string/sentence with spaces
 cout << "Please enter a valid sentence (with spaces):\n>";
 getline(cin, input);
 cout << "You entered: " << input << endl << endl;

 // How to get a number.
 int myNumber = 0;

 while (true) {
   cout << "Please enter a valid number: ";
   getline(cin, input);

   // This code converts from string to number safely.
   stringstream myStream(input);
   if (myStream >> myNumber)
     break;
   cout << "Invalid number, please try again" << endl;
 }
 cout << "You entered: " << myNumber << endl << endl;

 // How to get a single char.
 char myChar  = {0};

 while (true) {
   cout << "Please enter 1 char: ";
   getline(cin, input);

   if (input.length() == 1) {
     myChar = input[0];
     break;
   }

   cout << "Invalid character, please try again" << endl;
 }
 cout << "You entered: " << myChar << endl << endl;

 cout << "All done. And without using the >> operator" << endl;

 return 0;
}