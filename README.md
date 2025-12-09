## This project is part of my Autonomous Robot Arm

This is my fist attempt at creating a distance calculator between an object and a camera.

This project attempts to detect different high contrast objects with either template matching or contour detection then creating a bounding box over it.

I've experimented with filtering objects using HSV and LAB color spaces. Through the experimentation I found values that work with specific colors, but not with others. So my pipeline limits detection through specific colors. 

Moving forward, I would reattempt this using ArUco markers instead.
