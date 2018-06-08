# Motion-Tracking-with-OpenCV

Uses only OpenCV and no fancy tools for (multiple) Motion Tracking, nice performance.

In this program, I first turn the previous and current frames into gray scale, and apply Gaussian blurring. Then I get the difference between these two frames, and defines threshold so it doesn’t respond to any trivia change between frames, and apply many iterations of dilations to magnify the change in motions. 

Then I use the findContours() function to obtain the points of contour by the movements between frames, and iterates through the contours to find the center of mass for each consecutive frames. What I notice from the previous attempt is that since we are only comparing between the difference from frame to frame, the pixel shifts may not represent a coherent movement - when my hand moves, the area that are outlined may not cover some part of my fingers, and the areas that do outline the movements, may be a few discrete area. Thus, I may have three or four boxes on my hand. Using the center of mass, and add some padding around the center to fill the thresh layer that we later use to find the vertices for the bounding boxes, thus gives us a much nicer bounding area along a single object.

The program tracks an object that moves steadily across the field of view pretty well. It won’t maintain an understanding of where it is if it stops moving temporarily, and continue tracking it if it starts moving again since I did not use any color tracking technique like camshift - it only stay for an extra frame, but it will pick up the object once it starts moving again. Although the having the box sticking with the object even when it stops could be implemented with some logical tricks, I decide not to, since as there are many moving objects accumulating, eventually the screen will just be full of bounding boxes..

After adding the padding I got from the mass of center, the program is actually very successful at tracking a moving object without being distracted by other moving objects. My program can also track multiple objects, and track them individually pretty well as long as their bounding boxes don’t cross line - otherwise the program would think they are the same object moving. 


