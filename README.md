# FileComparison

#### Checks if two files are same or not.

#### Language: Python 2.7
#### Program Name:  file_checker.py, FileComparisonTest.py

##### How to Run:
1.	Open Terminal/Command line.
2.	Go to “Vungle Assignment” folder
3.	Go to “Test_Files” folder
4.	Run Python program by using command – python FileComparisonTest.py


##### Input:
Make sure all files are in same folder.
The code takes test files.

##### Output:
It will determine whether it has same content or not.

##### Approach:
A function is written that returns True if both files are same and returns False otherwise.

##### Algorithm:

First it will check if both file sizes are same or not. 
If file sizes are not same, it means it is different files and so it will return Boolean False. 

If both file sizes are same. 
It will compare both files’ content with a chunk of bytes at a time. 

If the chunks do not match, it will return Boolean value false and break the loop. 

At the end, if everything is same, it will return. 


##### Complexity:
 Time Complexity: O(n) if size is n bytes 
 Space Complexity: O(m) if chunk size is m 


##### Tests:
It checks for following tests: 
Both Empty Files Test 
Both Same Files Test 
Both Different Image Files Test 
Two Different Extension Files Test 
Different Files Test 
Both Different Image Files Test 
Invalid File Location Test 
One Extra Space Test 
One Letter Different Test 
Both Same Audio Files Test 
Both Same Image Files Test 
