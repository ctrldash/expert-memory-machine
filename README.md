### Repo with homework for data streams topics

A simple kafka streaming application

Dataset: a history from your favorite browser to a CSV file

Prepare a kafka environment.

Implement a “generator” microservice that splits the dataset to messages, sends them to kafka as a message. 

Implement a kafka streaming application that calculates a visiting statistic - a number of visits for each root domain (com, ua, org, edu, etc) from your browser history and prints top five root domains

Results: 
Top 5: 
 | suffix	| count
0	| com	| 24568
1	| com.ua	| 6805
2	| ua	| 3064
3	| in.ua	| 858
4	| org	| 572