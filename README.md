# Facebook Election Forecasting Tools
Project Overview:

This project entails the development of tools by Facebook for forecasting the results of US presidential elections based on sentiment analysis and network relationships among voters.

Tool 1: Forecasting with Enmity Levels

The first tool utilizes enmity levels among friends on Facebook to categorize voters into Democrats and Republicans. The goal is to minimize enmity within each group while maximizing enmity between the two groups.

Functionality:

The function facebook_enmy(V, E) takes two inputs:

A Python set V representing voters.
A Python dictionary E where keys denote pairs of voters who are friends on Facebook, and values represent the enmity level assigned by Facebook.
Outcome:

The function returns two Python sets, D and R, representing voters for Democrats and Republicans, respectively. The tool aims to optimize both the running time and the enmity level between Democrats and Republicans.

Tool 2: Forecasting with Friendship Levels

The second tool adapts to changes in sentiment analysis, focusing on friendship levels rather than enmity. It groups voters to maximize friendship within each group and minimize friendship between Democrats and Republicans.

Functionality:

The function facebook_friend(V, E) requires two inputs:

A Python dictionary V where keys represent voters and values are tuples containing likelihoods for Democrats and Republicans.
A Python dictionary E where keys represent pairs of voters who are friends on Facebook, and values represent the friendship level assigned by Facebook.
Outcome:

Similar to Tool 1, this function returns two Python sets, D and R, representing voters for Democrats and Republicans, respectively. The tool aims to optimize the running time while maximizing the likelihood of voter grouping.

Note: The README provides an overview of the project and its components. For detailed implementation and usage instructions, please refer to the code documentation.
