# GoodEyes

## Inspiration
Without thinking, you start getting too close to the screen without even realising. In this new century, where we are always in front of a computer, it is more important than ever to make sure we keep at a safe distance from the screen. We thought it would be very useful for adults and kids alike to be able to have a background app that could warn them every time they got too close to the screen. 

## What it does
GoodEyes tracks the distance between your face and the screen, and pops up a message when you are more than 5 seconds too close to the screen.

To track the distance, it measures the distance between the two eyes: the bigger the distance, the closer the user is to the screen.

To use the app, enter into GoodEyes.py code, and install the corresponding modules. After executing the .py file, You will see an introduction screen with an ON-OFF button, that starts the distance tracking when it is pressed, and ends it when it is pressed a second time. You can also close the program by pressing the close button on the Pygame screen.

After finishing, the program saves the percentage of time the user has been too close to the screen, and the average number of warnings it recieves by minute, and also the date in which the program was run (in this version, the date is saved in hours and minutes. Eventually, we would change this into weeks and days). When the program is run again, it displays which shows the user how the program has been able to improve its average distance to the screen over time.

## How we built it
The program has been coded using python. As the visual interface, we used the module pygame. We used cv2 and argparse to use the camera to track the distance to the screen. Datetime and time were used to keep track of the average time the user is too close to the screen, and also to control the pop-up only appearing when the user has been close to the screen for more than 5 seconds. Json was used to save a dictionary to keep track of the progress, and os to be able to get to the files. 


## Challenges we ran into
The most difficult part was to put pygame and the camera tracking together: We struggled on make them work on the same time. Finally, we could solve it by using the thread library, in which the code can run with more than 1 process at once.

Another challenge was for the pop-up message to pop up, even though the Pygame screen or camera were minimized or not in the front. We solved that when we found a new library, ctypes, which had a feature that allowed it to move to the front of the screen.

## Accomplishments that we're proud of
We were three strangers that teamed up and created a working computer application demo. In the beginning, we brainstormed different ideas and came up with an APP that helps children and adults keep a healthy distance from their screens. Then, we split tasks according to what we are good at. Ridwan is good at making videos and voicing, so he is responsible for the video making and documentary of our project. Nuria is good with GUIs, so she is responsible for making the user interface of our APP. Lambo has experience with machine vision, so he was responsible for implementing face detection and distance measurement algorithms. By working together, we learned more about collaboration and accomplished something that we could not have done by ourselves.

## What we learned
Teamwork helps to generate better ideas. Because everybody is working on what they are good at and focusing more on their part of the project, work is more efficient. Also, we learned that if we believe we can make something and try, we can succeed even if it is very hard.

## What's next for GoodEyes
With more time and some investments, we can develop GoodEyes as professional standard computer software. We can also develop Andriod and IOS versions so more people can use GoodEyes to protect their eyes. More compelling functions can be developed, like parenting notification, parent lock, or distance calibration. To save battery power, the camera will be programmed to take photos every period of time. The screen use behavior log will be more detailed, reflecting the user's daily screen use. 

We have to research how to run the software in the background on different devices. Our software may encounter problems running in the background of mobile devices because they have harsher security limitations. We can study how existing APPs run in the background of phones. Another big issue is camera access. No one wants their camera to always be watching them, we need to convince the user their camera is only used for detecting distance of their face, and no personal data will be collected for any use.

We hope you enjoy the program!

## owners
Núria, Lambo, Radwin
