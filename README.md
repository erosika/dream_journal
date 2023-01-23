# dream_journal

  bot records dream entries to a txt file

  - first thing in the morning:
  bot texts the 'dreamer' to ask if they had a dream last night
  'dreamer' replies with a record of their dream (via text // voice to text)

  - sometime in the day:
  script will be scheduled to check for a message/entry
  entry is appended to a text file



# Steps:

* create a dedicated Gmail account for the bot

* find your SMS gateway address which varies depending on cell provider (i.e. 'your9digit#'@txt.att.net)


* login to gmail and generate an app password

* create secret info to a dictionary called secrets.json as:
  - {
  "user" : "XXXXXXXXXX@gmail.com",          --| dream journal bot's dedicated gmail
  "password" : "XXXXXXXXXX",              --| bot's gmail password
  "app_pw_gmail" : "XXXXXXXXXX",               --| bot's gmail app password
  "dreamer_contact" :  "XXXXXXXXX@yourSMSgateway.net"    --| this is your phone number
  }


* enable Gmail API
  - create credentials--> OAuth client ID --> desktop app
  - download .json file with client ID and secret
  - rename as credentials.json and save to directory


* from here, the program is divided into two seperate commands to be sceduled by cron

* the two commands for the shell script are:

  - 'alert'  --- schedule for a time in the early morning when you wake up
  - 'write'  --- will check for a text response and append it to dream_journal.txt with the date

