[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

[image4]: ./output/sand_colour_spaces.png
[image5]: ./output/rock_colour_spaces.png
[image6]: ./output/ball_colour_spaces.png
[image7]: ./output/combined.png
[image8]: ./output/sim.png

## Search and Sample Return Project

![alt text][image1]

This project is modeled after the [NASA sample return challenge](https://www.nasa.gov/directorates/spacetech/centennial_challenges/sample_return_robot/index.html)

## The Simulator
The first step is to download the simulator build that's appropriate for your operating system.  Here are the links for [Linux](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Linux_Roversim.zip), [Mac](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Mac_Roversim.zip), or [Windows](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Windows_Roversim.zip).  


## Dependencies
Python 3 + OpenCV, and Jupyter Notebooks

---

### Computer Vision Analysis
#### Identifying Sand, Obstacles and Rocks
 To identify the Obstacle in the field of view we looked at different colour space segment them for the the range of colour we are looking for, for example when looking for the the rock walls we are generlly looking for a blackish brown colour. 
These actions are preformed in the `Diferent Colour Spaces Thresholds`, `Sand Threshold`, `Rock Threshold` and `Ball Threshold` sections of the Jupyter Notebook.


![alt text][image4]
![alt text][image5]
![alt text][image6]
![alt text][image7]


#### Processing of Images
The first step to processing an incoming is to apply a perspective transform on it to get a bird's eye view of the environment. Next we apply our three threshold functions to identify the the sand, walls and the rock samples that are inview.
 
After finding each of these we then convert the pixel locations to a position in the local rover coordinate system then to our global world coordinate system.
 
Finally we update our map, marking it with our findindings.
 
Here is a video of our pipeline on the sample [video](./output/test_mapping2.mp4)






### Autonomous Navigation and Mapping

In the `perception_step()` we look for each of the sand, walls and rock samples pixels and then translate them to our world coordinate system to be used in the `decision_step()` of our pipeline.
 
Also we try to correct for the roll of the rover,  as well as making note if we have either an extreme value of pitch or roll.
 
 
In the `decision_step()` we build a [DFA](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) which make choices to transition from state to state primarily based on the size of the sand area and rock wall area in front of the rover.
The possible state are 

| Possible State |
|:--------------:|
|Forward|
|Stuck|
|Rock Ahead|
|Move To Ball|
|Can Pick Up|
|Picking Up|
|Turn Around|
|Open Area|
|Corridor|
|Left Wall|
|Right Wall|
|Front Wall|
|Left Corner|
|Right Corner|    
|Full Corner|
|Return Home|
|Completed Challenge|

#### Autonomous Mode
To lunch in autonomous mode open a terminal and run the `drive_rover.py` file. Call it at the command line like this: 

```sh
python drive_rover.py
```  
Then launch the simulator and choose "Autonomous Mode".  The rover should drive itself now! 

#### Results
![alt text][image8]

When launching in autonomous mode the rover is able to navigate the environment and map 
95+% with a fidelity of about 65%. It is able to  find all of the rock samples, pick them up, and return home.

The simulator was run at 1024x768 on Good quality with about 26-28 fps.
**Note: running the simulator with different choices of resolution and graphics quality may produce different results!


#### Issues and Improvements
The pipeline can fail when it gets really stuck in a Wall/Rock sometimes, it can get unstuck if you give it enough time. This is due to the edge detection/collision of the simulator.

The pipline could be improved by doing some path planing and moving in the direction of unexplored area.
