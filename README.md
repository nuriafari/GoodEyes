# GoodEyes


## Inspiration
Really easily, you start getting too close to the screen without even realising. In this new century, where we are always in front of a computer, it is more important than ever to make sure we keep at a safe distance from the screen. We thought it would be very useful for adults and kids alike to be able to have a background app that could warn you every time you got too close to the screen. 

## What it does
GoodEyes tracks the distance between your face and the screen, and pops up a message when you are more than 5 seconds too close to the screen.

To track the distance, it measures the distance between the two eyes: the bigger the distance, the closer the user is to the screen.

To use it, enter into GoodEyes.py, and install the corresponding modules. After executing the .py file, You will see an introduction screen with an ON-OFF button, that starts the distance tracking when it is pressed, and ends it when it is pressed a second time. You can also close the program by pressing the close button on the Pygame screen.

After finishing, the program saves the percentage of time the user has been too close to the screen, and the average number of warnings it recieves by minute, and also the date in which the program was run (in this version, the date is saved in hours and minutes. Eventually, we would change this into weeks and days). When the program is run again, it displays which shows the user how the program has been able to improve its average distance to the screen over time.

## How we built it
The program has been coded using python. As the visual interface, we used the module pygame. We used cv2 and argparse to use the camera to track the distance to the screen. Datetime and time were used to keep track of the average time the user is too close to the screen, and also to control the pop-up only appearing when the user has been close to the screen for more than 5 seconds. Json was used to save a dictionary to keep track of the progress, and os to be able to get to the files. 

The three members of the team had some coding experience on Python. Nuria had used pygame to make an app before, and Lambo had used threading and cv2 to use the camera to track the distance. Finally, Ridwan had video-editing experience. After brainstorming and deciding which project to develop, we were able to split our tasks so that each member could contribute equally to the final project.

## Challenges we ran into
The most difficult part was to put pygame and the camera tracking together: We struggled on makin them work on the same time. Finally, we could solve it by using the thread library, in which the code can run with more than 1 process at once.

Another challenge was for the pop-up message to pop up, even though the Pygame screen or camera were minimized or not in the front. We solved that when we found a new library, ctypes, which had a feature that allowed it to move to the front of the screen.

## Accomplishments that we're proud of

## What we learned

## What's next for GoodEyes

owners: Núria, Lambo, Radwin
