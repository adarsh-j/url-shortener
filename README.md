**Table of content:**
- [URL Shortener](#url-shortener)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Functional Requirements](#functional-requirements)
- [Architecture](#architecture)
- [Scalability](#scalability)
- [Shortening Algorithm](#shortening-algorithm)
- [Metrics](#metrics)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)

# URL Shortener!

The URL Shortener service creates a short URL to be used as an alias for a long URL. This short URL will redirect the user to the long URL when accessed. This is similar to the service provided by Bitly or Tinyurl.

## Features
- Every short URL is case sensitive, unique and will point and resolve to only one long URL. A long URL can have multiple short URLs pointing to it.
- The size of all short URL is always 6 characters long and consists of characters [a-zA-Z0-9].
- The URL mapping will remain in the system forever and can be deleted through an API.
- Metrics to track the usage of short URLs can be accessed through the metrics API.

## Requirements
- This service was developed and tested on a Linux host (Ubuntu 20.04) with Docker v20.10.5 running.
- CURL v7.47 was used to access the endpoints. Any other similar utility should suffice. 

## Installation
- Download the repository and run
	> docker-compose up

## Usage
-  Once the docker containers are up and running, identify the IP of the web server through the following commands
```
$ docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS          PORTS                    NAMES
7159d5711693   nginx:alpine                        "/docker-entrypoint.…"   9 seconds ago    Up 8 seconds    0.0.0.0:80->80/tcp       webserver
```
 - The URL Shortener service can be accessed on port 80, as follows
	> curl http://0.0.0.0
	
## Functional Requirements
- User should be able to create a unique shortened URL for any specific long URL.
- The short URL should redirect the user to the long URL on access.
- The short URL can be deleted on request.
- User should be able to retrieve following metrics for a short URL.
	- Number of times accessed in the last 24 hours.
	- Number of times accessed in the past week.
	- Total number of times accessed in the life time.

## Architecture



### Scalability

### Shortening Algorithm

### Metrics

### Database Schema

## API Documentation

Functions
---------

    
`createUrl()`
:   This endpoint is used to create a short URL from a real URL.
    The short URL returned is unique and points to this original URL only.
    Accepts the `url` in JSON format.
    Example Input:
    ```
    {
        "url" : "www.google.com"
    }
    ```
    Example Output:
    ```
    {
        "longurl" : "www.google.com",
        "shorturl" : "X8uE9s"
    }
    ```

    
`deleteUrl()`
:   This endpoint is used to delete an existing short URL and all its associated metrics.
    A HTTP code 404 is returned if the short URL does not exist.
    Example Input:
    ```
    {
        "url" : "x8uE9s"
    }
    ```
    Example Output:
    ```
    {
        "message" : "success",
        "shorturl" : "X8uE9s"
    }
    ```

    
`getMetrics(shorturl, hour)`
:   This endpoint is used to get the number of times a specific short URL was accessed,
    in the number of hours specified.
    hour is an integer between 0 and 168 (which is the number of hours in a week).
    If the hour is 0, all time access count is returned. Otherwise, access time is the past
    <hour> hours is returned.
    
    A HTTP code 404 is returned if
        - The short URL does not exist.
        - Hour is not an integer between 0 and 168.
    Success return is a JSON which contains
        - short URL
        - count, in int
        - start_time, which is (current time) - (number of hours) in epoch seconds OR
            0 if hour is 0
        - end_time, which is (current time) in epoch seconds
    
    Example Input:
    ```
    /api/v1/metrics/x8uE9s/24
    ```
    Example Output:
    ```
    {
        "shorturl" : "X8uE9s"
        "count" : 128,
        "start_time" : "1699422878",
        "end_time" : "1699426478"
    }
    ```

    
`index()`
:   This endpoint serves the home page

    
`readUrl(shortUrl)`
:   This endpoint is used to redirect (HTTP code 302) the short URL to the actual long URL.
    If the short URL does not exist, a HTTP code 404 is returned.
    All short URLs are 6 character length and contain [a-zA-Z0-9] characters only.
=======
------------------------------------------------------------------------------------------

#### Home page and accessing short URLs

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(get home page)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         |  `application/json`               | Welcome to URL Shortener service                                    |

##### Example cURL

> ```javascript
>  curl GET http://localhost/
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/{short_url}</b></code> <code>(accessing short URLs)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                  |
> |-------------------|-----------|----------------|------------------------------|
> | `short_url`       |  required | string         | The unique short URL         |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `302`         |                                   | Redirected to the original long URL                                 |
> | `400`         | `application/json`                | `{"code":"404","message":"Page does not exist"}`                    |

##### Example cURL

> ```javascript
>  curl GET http://localhost/u6Ht3e
> ```

</details>

------------------------------------------------------------------------------------------

#### Creating new short URL

<details>
 <summary><code>POST</code> <code><b>/api/v1/create</b></code> <code>(create new short URL against a real, possibly longer URL)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                                                       |
> |-------------------|-----------|----------------|-------------------------------------------------------------------|
> | `url`             |  required | string         | The long URL against which a short URL needs to be created        |


##### Responses

> | http code     | content-type                      | response                                                                   |
> |---------------|-----------------------------------|----------------------------------------------------------------------------|
> | `200`         | `application/json`                | `{"longurl":"<original_longurl>","shorturl":"<created_short_url>"}`        |
> | `404`         | `application/json`                | `{"message":"A URL is required to create a shortened alias to it"}`        |
> | `500`         | `application/json`                | `{"longurl":"<original_longurl>","message":"Failed to create short url"}`  |

##### Example cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data '{"url" : "www.google.com"}' http://localhost/
> ```

</details>

------------------------------------------------------------------------------------------

#### Deleting existing short URL

<details>
  <summary><code>DELETE</code> <code><b>/api/v1/delete</b></code> <code>(delete existing short URL)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                                   |
> |-------------------|-----------|----------------|-----------------------------------------------|
> | `url`             |  required | string         | The short URL that needs to be deleted        |

##### Responses

> | http code     | content-type              | response                                          |
> |---------------|---------------------------|---------------------------------------------------|
> | `200`         | `application/json`        | `{"shorturl":"<shorturl>","message":"success"}`   |

##### Example cURL

> ```javascript
>  curl -X DELETE -H "Content-Type: application/json" --data '{"url" : "X8uE9s"}' http://localhost/
> ```

</details>

------------------------------------------------------------------------------------------

#### Metrics

<details>
 <summary><code>GET</code> <code><b>/api/v1/metrics/{shorturl}/{hour}</b></code> <code>(get metrics)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                                     |
> |-------------------|-----------|----------------|-------------------------------------------------|
> | `short_url`       |  required | string         | The unique short URL                            |
> | `hour`            |  required | int            | Number of hours between 0 and 168, inclusive    |

##### Responses

> | http code     | content-type                      | response                                                                                      |
> |---------------|-----------------------------------|-----------------------------------------------------------------------------------------------|
> | `200`         |  `application/json`               | `{"shorturl":"<shorturl>","count":<int>, "start_time": <long int>, "end_time": <long int>}`   |
> | `404`         |  `application/json`               | `{"shorturl":"<shorturl>","message":<string>"}`                                               |


##### Example cURL

> ```javascript
>  curl GET http://localhost/api/v1/metrics/u6Ht3e/0	
> ```

</details>

------------------------------------------------------------------------------------------

## Tests
