# Techgig Data Science Edition 3 Final solution
The approach is very simple if you figure out the data carefully. If you take a look at the target column in train.csv, you’ll find that most entries in target are just the initial part of the urls present in each row of the description. So we need to extract the url and then take the initial part. Regarding this I asked a question on [stackoverflow](https://stackoverflow.com/questions/46610149/extract-the-initial-part-of-a-url-if-it-ends-with-com-or-net). I needed a regular expression to accomplish the task because I’m not good at regular expression. 
	Now I had the regular expression to extract the url. Before I apply this re to test dataset, I found the unique values in target column in train.csv. Now let’s move to test data. I applied re to each row of test data. While iterating over each row, I was checking few conditions 
1.	Pick the url if the extracted url appears in the unique values taken from train data.
2.	If there were two match found then according to train data I need to pick either the first one or last one. So this condition also worked.
3.	There were some values like “_will_”, ”_service_” in target column of train data. After analysing the train data I found that these values were picked only when there was no match.
4.	There were two three cases which I handled manually by returning specific values.

I've used **nltk** but there is no use of it if you define words like _'will'_, _'service'_ manually.
