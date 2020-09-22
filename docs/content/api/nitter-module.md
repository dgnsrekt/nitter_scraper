<a name="nitter.DockerBase"></a>
## `DockerBase`

Provides helper methods for connecting to the docker client.

<a name="nitter.Nitter"></a>
## `Nitter`

Nitter Docker container object

**Arguments**:

- `host` _IPv4Address_ - The host address the docker container will bind too.
- `port` _int_ - The port the docker container will listen to.
  

**Attributes**:

- `tempfile` _TemporaryFile_ - A TemporaryFile file generated from a template.
- `container` _Container_ - Local representation of a container object.
  Holds the started instance of a docker container.
- `address` _str_ - The full address of the docker container.
- `ports` _dict[int, int]_ - Binds the listening port to the nitter docker container's
  internal port 8080.
- `config_filepath` _str_ - Path name to the generated tempfile.
- `volumes` _dict[str, dict[str, str]]_ - used to configure a bind volume.

<a name="nitter.Nitter.get_profile"></a>
#### `Nitter.get_profile`

```python
 | def get_profile(username: str, not_found_ok: bool = False)
```

Scrapes nitter for the target users profile information.

This is a modified version of nitter_scraper.profile.get_profile().
This version automatically uses the address of the docker container as the primary
address to scrape profile data.

**Arguments**:

- `username` - The target profiles username.
- `not_found_ok` - If not_found_ok is false (the default), a ValueError is raised if
  the target profile doesn't exist. If not_found_ok is true, None will be returned
  instead.
  

**Returns**:

  Profile object if successfully scraped, otherwise None.
  

**Raises**:

- `ValueError` - If the target profile does not exist and the not_found_ok argument is
  false.

<a name="nitter.Nitter.get_tweets"></a>
#### `Nitter.get_tweets`

```python
 | def get_tweets(username: str, pages: int = 25, break_on_tweet_id: Optional[int] = None)
```

Gets the target users tweets

This is a modified version of nitter_scraper.tweets.get_tweets().
This version automatically uses the address of the docker container as the primary
address to scrape profile data.

**Arguments**:

- `username` - Targeted users username.
- `pages` - Max number of pages to lookback starting from the latest tweet.
- `break_on_tweet_id` - Gives the ability to break out of a loop if a tweets id is found.
- `address` - The address to scrape from. The default is https://nitter.net which should
  be used as a fallback address.
  

**Yields**:

  Tweet Objects

<a name="nitter.Nitter.start"></a>
#### `Nitter.start`

```python
 | def start()
```

Starts the docker the container

<a name="nitter.Nitter.stop"></a>
#### `Nitter.stop`

```python
 | def stop()
```

Stops the docker the container

<a name="nitter.NitterScraper"></a>
#### `NitterScraper`

```python
def NitterScraper(host: str = "0.0.0.0", port: int = 8080)
```

The NitterScraper context manager.

Takes care of configuring, starting, and stopping a docker instance of nitter.

**Arguments**:

- `host` - The host address the docker container will bind too.
- `port` - The port the docker container will listen to.
  

**Yields**:

- `Nitter` - An object representing a started nitter docker container.

