# USC automatically book appointments

This script helps the user to book automatically appointsments by urban sports club. 

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
0 0 * * TUE,FRI   $HOME/usc-auto-book/uscApiTool.py
```

Will execute the script provided as the last argument every tuesday and friday at midnight.
See a explanation on the syntax [here](https://crontab.guru/#0_0_*_*_TUE,FRI).