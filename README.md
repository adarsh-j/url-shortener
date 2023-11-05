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
	> docker-compose up
 - The URL Shortener service can be accessed on port 80, as follows
	> curl http://172.0.0.1
	
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


## Tests
