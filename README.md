weibo
=====

weibo is a twitter-like simple weibo demo system. It supports the miminum functionalities of a twitter-like clone.  

## Architecture

* Framework  
[Flask](http://dormousehole.readthedocs.org/en/latest/)
* Database   
[sqlite3](http://www.sqlite.org/)
* DB API for Sqlite3    
[Python sqlite3 module](https://docs.python.org/2/library/sqlite3.html)

## Setup

This code has passed test on OS X with Python 2.7.6. Consequently it should conform with Ubuntu system or other Linux distributions.

### Steps
1. Install Python 2.7.6 (If not install).
2. Install Flask framework(sudo pip install -U flask).
3. Install sqlite3 library(On ubuntu: sudo apt-get install libsqlite3-dev).
4. Clone source code to local system.

### Run
1. Execute bin/init\_db.py to initialize data base.
2. python ann/app.py to run flask embedded web server.
3. Send request with curl or other http clients.

## Test Client
* curl
* POST Man plugin for Chrome

### curl usage

curl -X \[Method\] -H "header: value" http://127.0.0.1:5000/weibo/uri  -d '{json object}' -vv

**Example**  
curl -X POST -H "X-User: test" -H "X-pass: test123" http://127.0.0.1:5000/weibo/signup -vv  

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/weibo/follower -d '{ \  
"user": "test",\  
"follower": "Obama"\  
}' -vv


## REST APIs

### signup

#### Request

* URI  

URI           | Method | Parameters|
--------------| ------ | -----------
/weibo/singup | POST   | None      |

* Headers  

Name          | Value    | Required/Optioanl|
--------------|----------| ------------------
X-User        | name     | Required         |  
X-Pass        | password | Required         |

* body  
None(*Will Change*)

#### Response

* status  
  * 200 OK: Request is handled successfully
  * 400 Bad Request: Request does not conform with restrictions
  * 403 Forbidden: Can not signup
  
* Headers  

Name                 | Value                | Required/Optioanl|
---------------------|----------------------| ------------------
Contenty-Type        | application/json     | Required         |  

* Body  

```
{   
    "uuid": uuid string, 
    "name": user name,
    "follower": follower list,
    "following": following list
}
```

### signin

#### Request

* URI  

URI           | Method | Parameters|
--------------| ------ | -----------
/weibo/singin | POST   | None      |

* Headers  

Name          | Value    | Required/Optioanl|
--------------|----------| ------------------
X-User        | name     | Required         |  
X-Pass        | password | Required         |

* body  
None(*Will Change*)

#### Response

* status  
  * 200 OK: Request is handled successfully
  * 400 Bad Request: Request does not conform with restrictions
  * 403 Forbidden: Authentication failed
  * 404 Not Found: The user is invalid
  
* Headers  

Name                 | Value                | Required/Optioanl|
---------------------|----------------------| ------------------
Contenty-Type        | application/json     | Required         |  

* Body  

```
{   
    "uuid": uuid string, 
    "token": token string
}
```

###  add follower

#### Request

* URI  


URI                      | Method | Parameters|
-------------------------| ------ | -----------
/weibo/\<uuid\>/follower | POST   | None      |

* Headers  

Name                | Value                | Required/Optioanl|
--------------------|----------------------| ------------------
Content-Type        | application/json     | Required         |    

* body  

```
{
    "follower": the follower name to be added
}
```

#### Response

* status  
  * 200 OK: Request is handled successfully
  * 400 Bad Request: Request does not conform with restrictions
  * 403 Forbidden: Authentication failed
  * 404 Not Found: The user or follower is invalid
  
* Headers  

Name                 | Value                | Required/Optioanl|
---------------------|----------------------| ------------------
Contenty-Type        | application/json     | Required         |  

* Body  

```
{   
    "name": user name, 
    "follower": follower list of user,
    "following": following list of user
}
```
