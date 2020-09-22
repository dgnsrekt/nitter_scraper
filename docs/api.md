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

A modified version of the get_profile function.

This version automatically uses the address of the docker to container as the primary
address to scrape profile data from.

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

Schema something

<a name="schema.Entries"></a>
## `Entries`

Contains metadata parsed from the text contents of the tweet.

This object is a subclass of the pydantic BaseModel which makes it easy to serialize
the object with the .dict() and json() methods.

**Attributes**:

- `hashtags` - Contains all hashtags parsed from the tweet. Example `Bitcoin`.
- `cashtags` - Contains all cashtags parsed from the tweet. Example $BTC
- `urls` - Contains all URLs parsed from the tweet excluding photo/video media links.
- `photos` - Contains all URLs that link to photo media.
- `videos` - Contains all URLs that link to video media.

<a name="schema.Tweet"></a>
## `Tweet`

Represents a status update from a twitter user.

This object is a subclass of the pydantic BaseModel which makes it easy to serialize
the object with the .dict() and json() methods.

**Attributes**:

- `tweet_id` - Twitter assigned id associated with the tweet.
- `tweet_url` - Twitter assigned url that links to the tweet.
- `is_retweet` - Represents if the tweet is a retweet.
- `is_pinned` - Represents if the user has pinned the tweet.
- `time` - Time the user sent the tweet.
- `text` - Text contents of the tweet.
- `replies` - A count of the replies to the tweet.
- `retweets` - A count of the times the tweet was retweeted.
- `likes` - A count of the times the tweet was liked.
- `entries` - Contains the entries object which holds metadata
  on the tweets text contents.

<a name="schema.Tweet.from_dict"></a>
#### `Tweet.from_dict`

```python
 | def from_dict(cls, elements: Dict[str, Any]) -> "Tweet"
```

Creates Tweet object from a dictionary of processed text elements.

**Arguments**:

- `elements` - Preprocessed attributes of a tweet object.
  

**Returns**:

  Tweet object.

<a name="schema.Profile"></a>
## `Profile`

The profile object contains Twitter User account metadata.

This object is a subclass of the pydantic BaseModel which makes it easy to serialize
the object with the .dict() and json() methods.

**Attributes**:

- `username` - The users screen_name, handle or alias. '@dgnsrekt'
- `name` - The users name as they've defined it.
- `profile_photo` - URL reference to the profiles photo.
- `tweets_count` - The number of Tweets (including retweets) issued by the user.
- `following_count` - The number of accounts the user is following.
- `followers_count` - The number of followers this account has.
- `likes_count` - Number of likes the follower has received.
- `is_verified` - Indicates if the user has been verified.
- `banner_photo` - URL reference to the profiles banner.
- `biography` - The users autobiography.
- `user_id` - User identification number generated by twitter.
- `location` - A user defined location.
- `website` - A user defined website.

<a name="schema.Profile.from_dict"></a>
#### `Profile.from_dict`

```python
 | def from_dict(cls, elements: Dict[str, Any]) -> "Profile"
```

Creates Profile object from a dictionary of processed text elements.

**Arguments**:

- `elements` - Preprocessed attributes of a profile object.
  

**Returns**:

  Profile object.

<a name="profile.username_cleaner"></a>
#### `username_cleaner`

```python
def username_cleaner(username: str) -> str
```

Strips @ symbol from a username.

**Example**:

  @dgnsrekt -> dgnsrekt
  

**Arguments**:

- `username` - username with @ symbol to remove.
  

**Returns**:

  Username with @ symbol stripped.

<a name="profile.link_parser"></a>
#### `link_parser`

```python
def link_parser(element: HTML) -> str
```

Gets the first link from an html element

Used for the profiles website, photo and banner links.

**Arguments**:

- `element` - HTML element with a link to parse.
  

**Returns**:

  First link from a collection of links.

<a name="profile.parse_user_id_from_banner"></a>
#### `parse_user_id_from_banner`

```python
def parse_user_id_from_banner(banner_url: str) -> str
```

Parses the users id from the users banner photo url.

The user id can only be parsed from the banner photos url.

**Example**:

```
    /pic/profile_banners%2F2474416796%2F1600567028%2F1500x500 -> 2474416796
                           ^        ^
                           |        |
                           ----------
                           user id section in banner link
```
  

**Arguments**:

- `banner_url` - URL of the profiles banner photo.
  

**Returns**:

  The target profiles user id.

<a name="profile.stat_cleaner"></a>
#### `stat_cleaner`

```python
def stat_cleaner(stat: str) -> int
```

Cleans and converts single stat.

Used for the tweets, followers, following, and likes count sections.

**Arguments**:

- `stat` - Stat to be cleaned.
  

**Returns**:

  A stat with commas removed and converted to int.

<a name="profile.profile_parser"></a>
#### `profile_parser`

```python
def profile_parser(elements: Dict) -> Dict
```

Converts parsed sections to text.

Cleans and processes a dictionary of gathered html elements.

**Arguments**:

- `elements` - Elements prepared to clean and convert.
  

**Returns**:

  A dictionary of element sections cleaned and converted to their finalized types.

<a name="profile.html_parser"></a>
#### `html_parser`

```python
def html_parser(html: HTML) -> Dict
```

Parses HTML element into individual sections

Given an html element the html_parser will search for each profile section using
CSS selectors. All parsed html elements are gathered into a dictionary and returned.

**Arguments**:

- `html` - HTML element from a successful nitter profile scraped response.
  

**Returns**:

  A dictionary of found elements from the parsed sections.

<a name="profile.get_profile"></a>
#### `get_profile`

```python
def get_profile(username: str, not_found_ok: bool = False, address: str = "https://nitter.net") -> Optional[Profile]
```

Scrapes nitter for the target users profile information.

**Arguments**:

- `username` - The target profiles username.
- `not_found_ok` - If not_found_ok is false (the default), a ValueError is raised if the target
  profile doesn't exist. If not_found_ok is true, None will be returned instead.
- `address` - The address to scrape profile data from. The default scrape location is
  'https://nitter.net' which should be used as a backup. This value will normally be
  replaced by the address of a local docker container instance of nitter.
  

**Returns**:

  Profile object if successfully scraped, otherwise None.
  

**Raises**:

- `ValueError` - If the target profile does not exist and the not_found_ok argument is false.

