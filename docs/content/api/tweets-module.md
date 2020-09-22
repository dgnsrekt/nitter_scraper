Module for scraping tweets

<a name="tweets.get_tweets"></a>
#### `get_tweets`

```python
def get_tweets(username: str, pages: int = 25, break_on_tweet_id: Optional[int] = None, address="https://nitter.net") -> Tweet
```

Gets the target users tweets

**Arguments**:

- `username` - Targeted users username.
- `pages` - Max number of pages to lookback starting from the latest tweet.
- `break_on_tweet_id` - Gives the ability to break out of a loop if a tweets id is found.
- `address` - The address to scrape from. The default is https://nitter.net which should
  be used as a fallback address.
  

**Yields**:

  Tweet Objects

