# Data Summary

Implementation of a probabilistic agent to predict fires based on data given from https://archive.ics.uci.edu/dataset/162/forest+fires <br>

Our data maps out Montesinho park, a region in North Eastern Portugal on an X,Y spatial coordinate grid. Everyday, for each coordinate on the map, the following metrics are measured
* `Temperature`
* `Wind`
* `Rain`
* `Relative Humidity`
* `Month`
* `Day`
* Fire Weather Index Metrics
  * `FFMC` (Continuous)
  * `DMC` (Integer)
  * `DC` (Continuous)
  * `ISI` (Continuous)
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

# Initial Belief Network
We based our conditional probability table computations and our model off of the constructed belief network. The dependencies of the nodes to one another are based off of a combination of our own intuition and how certain variables (like the weather indexes) are calculated.

<div style="text-align: center;">
  <img src="probabilistic_agent_code/data/init_bayes_model.png" alt="Initial Belief Network" width="500"/>
</div>

TO DO:
* Train your first model
* Evaluate your model
* Create/Update your README.md to include your new work and updates you have all added. Make sure to upload all code and notebooks. 
* Provide links in your README.md
Conclusion section: What is the conclusion of your 1st model? What can be done to possibly improve it?
