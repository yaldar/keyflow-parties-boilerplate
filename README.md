# keyflow-parties-boilerplate
Boilerplate with basic models for Keyflow tech task


## Dependencies

We use `python 3.7.5` for development. Make sure you have this installed on
your machine, or use `pyenv` as described later in this documentation. You would also
need mongodb server running locally 


## Steps for local development

1. [Mac](#mac-installation)

<h4 id="mac-installation">Instructions for Mac</h4>

1. Install pyenv and its virtualenv manager using
  ```
   $ brew install pyenv
   $ brew install pyenv-virtualenv
   $ pyenv install 3.7.5
   $ eval "$(pyenv init -)"
   keyflow-parties-boilerplate/$ pyenv virtualenv 3.7.5 env-3.7.5
   ```

   This will create a pyenv-virtualenv for you and probably place it on your
   `~/home/<username>/.pyenv/versions/`. You can activate that manually using
   ```
   keyflow-parties-boilerplate /$ source ~/.pyenv/versions/env-3.7.5/bin/activate
   ```

   or even better:

   ```
   keyflow-parties-boilerplate /$ pyenv activate env-3.7.5
   ```
   or, there are better ways to do this if you follow [Pyenv:Docs](https://github.com/pyenv/pyenv-virtualenv)

 2. Now you are in the right environment, install dependencies using:
   ```
   (env-3.7.5) keyflow-parties-boilerplate/$ pip install -r requirements.txt 
   ``` 
   Remember to connect this as the interpreter for PyCharm. 
   
 3. Install `mongodb-server` and copy the right configuration parameters to `keyflow/main.py`. For the most 
    basic cases, you might not want to change anything. 
 4. Try running some of the tests using Pycharm test runners. 

## Loading sample data 
For the context of the technical test, you have to create the following: 
```
Use a factory approach to create around 10 GuestAccounts.  
Use a factory approach to create a Party. 
1 of the 10 GuestAccounts is the owner of the party. 
8 others can be confirmed guests to the Party.  
```
This can be achieved using our sample data loader script. You can load the
 data by: 
```
keyflow-parties-boilerplate $ cd..
$ PYTHONPATH=keyflow-parties-boilerplate python3.7 keyflow-parties-boilerplate
/keyflow/sample_data/load_data.py 
``` 
Check your mongodb database with the name `keflow-parties` in your local
 environment to see the loaded sample data. 

## Destroying sample data
You can destroy data from all collections by running: 
```
keyflow-parties-boilerplate $ cd..
$ PYTHONPATH=keyflow-parties-boilerplate python3.7 keyflow-parties
-boilerplate/keyflow/sample_data/destroy_all_data.py 
``` 


## APIs to play around with 
@TODO: This needs to be done in some proper OPENAPI forms. 

Once you load the sample data, you can use POST on 
```
http://127.0.0.1:8080/v1/parties/1/chats/
```
with headers 
```
Authorization: 1
```
and body 
```
{
	
	"message": "First test message"
}
```
to create and store a test party room chat message into the database. 
