# Storytelling and Streaming Data - Assignment 1

### General implementation details ###

**Python library dependencies**

1. twitter
2. json
3. time

**API Keys**

* It is unfortunate and dangerous that I had to hardcode my keys and secrets into GitHub. I believe that we will be learning how to fix this using Redis in class on 2/10.

**Port**

* Port 8000 must be used here because it is hardcoded into the `index.html` file. Hopefully in a later implementation, I can allow the user to choose their own port.

**Encoding**

* I would have liked to pretty print the Tweet data on the webpage similar to how it works with stdout. However, I was running into unicode encoding issues when rendering the page. Hopefully, I can learn to solve this in a future implementation.

### Part 1 ###

* The stream that I have chosen to use comes from Tweets. I specifically used the twitter python library to track the key word water for tweets that were written near Flint, Michigan. The reason I chose this stream and filter was because there is quite a buzz going around about the atrocities of the contaminated water situation in Flint. While other environmental data streams may provide information on the level of damage to health, Twitter is useful for capturing reactions and emotions around an issue. By filtering on the word water, I attempted to hone in on those conversations that surround this global health issue. By using a location filter, I could capture the reactions of those people who actually live near the afflicted city.
* I tried prepending the word 'water' with various adjectives ('dirty', 'bad', etc.) but the stream was too slow to submit in my assignment. However, it did teach me the power of catering a stream to produce a desired output. Filtering using adjectives seems like a dangerous tactic that could be used by the media to sway mass opinions.
* Unforunately, I noticed that many of the Tweets were unrelated to the water contamination ciris. This was a clear reminder to me that Twitter users are not representative of any population. Twitter users comprise a small subset of a total population. Their ages and other classifying qualities are not distributed evenly. I am interested in spending more time exploring the demographics of Twitter users and trying to understand what we can learn from reading a filtered Twitter stream.

### Part 2 ###

**How to run**

1. Simply open a terminal window and run `python flint_tweets_stdout.py`
2. Tweet data will be pretty printed into stdout.

### Part 3 ###

**How to run**

1. In one terminal window execute `python -m SimpleHTTPServer 8000`
2. Then, in another window execute `websocketd --port 8000 python flint_tweets_webpage.py`
3. Navigate in Chrome to `http://0.0.0.0:8000/`
4. Tweet text will show up periodically in the browser.
