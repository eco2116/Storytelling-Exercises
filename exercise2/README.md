# Storytelling-Exercises

**Steps to run:**

1. Ensure proper python dependencies are installed (redis, requests, tweepy).
2. Begin redis server by running ```redis-server``` in one terminal.
2. In another terminal, run the pipeline ```python process_data.py | python avg.py | python alert_system.py | python twitter_bot.py```
