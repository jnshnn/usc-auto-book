# USC automatically book appointments

This script helps the user to book automatically appointsments by urban sports club. 
It might also help iOS or web user to book classes in advance and enjoy the same adventages as the android users.

## Disclaimer
Use on own risk. The author is not responsible in for any damage made to your account or to USC. 

And of cause, do not use the script if you don't have the approval of USC to access their API.

## Installation

It is recommended to create a new `virtual environment` to run this project. 

```bash
virtualenv venv
```

Source the virtual by using the `source` command and your approtiate `active.*` file in the `./venv/bin/` directory.

Install the requirements with pip3. 

```bash
pip3 install -r requirements.txt
``` 

## Configure

Edit the `usc_api.config` file for your credentials in the `[Credentials]` section. 

```
[Credentials]
	# replace with your email
	email = usc@example.com
	# replace with your password
	password = uscpassword1
```

## Defining a cron job

To add or update a cron job tip:
```bash
crontab -e
```

This will add a new cron job as your current user. 
The following line:

```
SHELL=/bin/sh

0 0 * * TUE,FRI   source $HOME/usc-auto-book/venv/bin/activate && $HOME/usc-auto-book/uscApiTool.py

```

Will execute the script provided as the last argument every tuesday and friday at midnight.
See a explanation on the syntax [here](https://crontab.guru/#0_0_*_*_TUE,FRI). Replace the path with the path where this repo is cloned.

If you want to receive a mail with the script output create the following job and replace `you@yourmail.com` with your mail address:

```
SHELL=/bin/sh

0 0 * * TUE,FRI   source $HOME/usc-auto-book/venv/bin/activate && $HOME/usc-auto-book/uscApiTool.py 2>&1 | mail -s "usc auto book -- cron job update" you@yourmail.com
```
