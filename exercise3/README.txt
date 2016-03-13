Evan O'Connor
README

I used Mike Dewar's Real Time Storytelling exercise 3 example to guide my project.

Part 1:
The stream that I chose to track are tweets containing either the text good morning or
good night. If a tweet says good morning, I increment a count held in redis and if it says
good night, I decrement the count. I am track this distribution across all languages.
Overall, I am trying to make a tracking mechanism to observe the likelihood that people
in a certain area who speak a given language may be waking up or going to sleep.

First, make sure redis' cache is clear. We do this, while redis is running (using redis-server) by running redis-cli flushdb. To start the tracking of the distribution, we
run the following two pipelines (preferrably in separate terminals to track outputs):

python morning.py | python count.py
python night.py | python count.py

This will begin tracking the counts of morning or night related messages. 

Part 2:
To load up the API, we run:

python api.py

Then, the various endpoints can be requested for example using curl, as follows:
curl localhost:5000/entropy

The /distribution endpoint returns data representing the ratio of the counts for each
language compared to the entire total.

The /rate endpoint tracks the overall rate of the stream totalled across all languages.

The /entropy endpoing returns the entropy of the distribution.

The /probability endpoint returns the likelihood of receiving a day or night message
for a given language. The user must provide a requested language as follows:
curl localhost:5000/probability?lang=en

Part 3:
To start the alerting system, we run:
python twitter_bot.py <lang>

ie: python twitter_bot.py en

This system will tweet messages to my account if the entropy is unusually high
or the provided language has a high probability of receiving a day or night message.

Part 4:
To start up the website that will make an API call and return the current distribution
to the user, run (while the API is running) in the directory containing index.html:

python -m SimpleHTTPServer 8001

Navigate in the browser to 0.0.0.0:8001 and you will see the current distribution
returned on the webpage.

