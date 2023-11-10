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
- The maximum length of the long URL supported is 2048 characters. This is an arbitrary number chosen and there is no constraint to change this to a higher number if required.
- High level metrics to track the usage of short URLs can be accessed through the metrics API.

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
