# Data Summary

Implementation of a probabilistic agent to predict fires based on data given from https://archive.ics.uci.edu/dataset/162/forest+fires <br>

Our data maps out Montesinho park, a region in North Eastern Portugal on an X,Y spatial coordinate grid. Everyday, for each coordinate on the map, the following metrics are measured
* `Temperature`
* `Wind`
* `Rain`
* `Relative Humidity`
* `Month`
* `Day`
  UPDATE:
* Fire Weather Index Metrics
  * `FFMC` (Continuous): Measures moisture content of litter and other fine fuels, higher --> fuels ignite/burn easier
  * `DMC` (Integer): Measures moisture content of loosely compacted organic material in the forest, higher --> material ignites/burns easier
  * `DC` (Continuous): Measuress moisture content of forest fuels, higher --> dryer/more risk
  * `ISI` (Continuous): Initial Spread Index, measures how fast a fire may spread once ignited
* Total burned area


As noted on the website from which the dataset was pulled from, given that the output skews towards 0.0, a logarithmic transformation is recommended. The attached research paper applied a transformation of $f(x) = ln(x+1)$.
Summary and Goal of our proposed agent: Given that we are able to observe the state of the forest (i.e. the aforementioned metrics) for everyday recorded, our goal is to predict the area burned of the forest for the following day. That is to say that our agent aims to predict the area that will burn on a subsequent day, given the metrics currently available to it.

# Broad Details of our probabilistic model agent
What kind of probabilistic model is it? 
* The world the AI agent exists in and will be trained in will be the Northeast region of Portugal.
  * The Performance measure of our agent will be the probability at which it correctly or closely correctly determines the occurrence and spread of wildfires given the metric available to it.
  * The Environment the agent exists in will be the Montesinho park, a national park in Northeast Portugal
  * The Actuators available to this agent will be capable of output predictions of the fires. A proposed output would be something similar to the inputs given to the agent; a vector which contains a predicted coordinate for the area burnt, alongside predicted weather metrics for iterative predictions (i.e. predicting multiple days in advance)
  * The Sensors available to this agent will be the measurements provided. Our agent in practice will be able to have access to the aforementioned metrics given, such as temperature, humidity etc.

What kind of agent is it? Goal based? Utility based? etc. 
 * Given our goals and data available, we believe it is most appropriate to utilize a goal-based agent, given our emphasis on predicting future events given the partially observable knowledge of its dynamic environment.

Describe how your agent is set up and where it fits in probabilistic modeling
* Many of our variables, such as FFMC, DMC, humidity, and wind speed, are continuous, so we indexed them to make them compatible with our probabilistic model. We structured these continuous variables into predefined bins that allowed us to compute probabilities more effectively.

# Initial Belief Network
We based our conditional probability table computations and our model off of the constructed belief network. The dependencies of the nodes to one another are based off of a combination of our own intuition and how certain variables (like the weather indexes) are calculated.

<div style="text-align: center;">
  <img src="probabilistic_agent_code/data/init_bayes_model.png" alt="Initial Belief Network" width="500"/>
</div>

# Data Exploration
First we thought it would be helpful to look at the distributions of each of our index variables (different fire indexes that assess risk).
![ffmc](https://github.com/user-attachments/assets/cd09e66b-9c8a-4fc7-b921-83f4d5f82d1f)
![dmc](https://github.com/user-attachments/assets/50c8247d-e03b-4426-915a-2e8580e9330b)
![dc](https://github.com/user-attachments/assets/a0ca46a0-b14e-4776-bf53-c84ec6630faa)
![isi](https://github.com/user-attachments/assets/8de0d2f2-fe6e-4672-bc38-6d22816b032f)\
As you can see, although many of these models draw from the same metrics (wind, humidity, temperature, precipitation), they're distributed quite differently. This tells us they may each give us unique insights as to the risk of fire that day.\
From what we've researched, we know that a high FFMC means litter and other cured fine fuels are more likely to ignite, so our data heavily observes instances where risk of ignition is high. DMC assesses the dryness and risk of ignition of loosely compacted organic layers, but this index is more widely distributed. DC measures deep, compacted organic layers, again with higher values being dryer/greater risk. This has a left skew and we observed more values on the higher end of the scale. Finally, ISI (Initial Spread Index) measures how fast a fire may spread once ignited. These values are skewed right and grouped towards the lower end of the scale. Since each of these indexes measure different sources of ignition/spread that can affect the occurrrence/spread of a fire, they are all incredibly helpful when it comes to predicting a fire.
<br/><br/>
![occ](https://github.com/user-attachments/assets/c868ab8f-e0f3-4881-b3f9-c32480ada66b)
![month](https://github.com/user-attachments/assets/12b1ccf3-37e5-45ec-8de6-69f28d06e352)\
Another interesting aspect of our data is the observation frequency of fires in general and what months are more prevalent in our data. As you can see, the occurence of fire vs. no fire is about equal. Meanwhile, for the months represented, we see August and September have a much higher frequency than other months. We assume this to be because August and September are peak fire seasons, so collecting fire-related data is more crucial during these periods.
<br/><br/>
<img width="463" alt="Screenshot 2025-02-16 at 1 36 39 PM" src="https://github.com/user-attachments/assets/c9db5d29-2f12-474b-bb50-51223f32b63d" />\
Finally, for missingness we've determined that no column in our data has missing values that need to be addressed, making it easier to train our model.

# Conclusion
Our first probabilistic model effectively identifies important trends in fire occurrence depending on environmental conditions. The analysis shows that FFMC plays a significant role, and levels between 85 and 95 significantly increase the likelihood of a fire. The highest likelihood of fire occurs within the range of 90 ≤ FFMC < 95, where 74.44% of observations indicate fire presence. Similarly, DMC demonstrates a strong correlation with fire occurrence, with fire probability rising as DMC increases. The highest probability (88.89%) is observed for DMC values greater than 200. 
Our findings are further supported by seasonal trends, since fire incidents peak in August and September, which corresponds with the region's dry season. Additionally, the dataset is well-balanced between fire and no-fire cases.


TO DO:
* Train your first model
* Evaluate your model
* Create/Update your README.md to include your new work and updates you have all added. Make sure to upload all code and notebooks. 
* Provide links in your README.md
Conclusion section: What is the conclusion of your 1st model? What can be done to possibly improve it?
