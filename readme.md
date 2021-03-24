# Movies
# Movies app with flask_restful api
### Get movie ratings 

This app will show you the information of movies like genre and ratings. 
This app has two level of access:
- admin - can perform crud operations(create, read, update and delete)
- user - can only read the movies information

### Prerequisites
- python3(>=3.7)
- pip3
- Mongodb(https://www.mongodb.com/try/download/community)
- 5000 port should be free for running flask server on localhost
- 27017 port should be free for running mongodb server

### Technology Stack used

- [HTML] - for user interface
- [Bootstrap] - for styling
- [python_flask] - python web framework
- [mongodb] - database 

### Installation

```sh
pip install -r requirements.txt
```


### How to Run
- set environment variables  
-- `env=local` OR `env=heroku` depending on environment you are running in  
-- `mongodb_host=mongodb://localhost:27017/+yourdbname` OR `mongodb_host=hostedmongodbaddress`

Now run main app ,run this command

```sh
python app.py
```

Type the url on your browser to run the webapp
- localhost:5000 if running locally
