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
