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

