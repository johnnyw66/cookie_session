# cookie_session
This utilty starts a python http session from an existing Chrome Cookies database. 

A Windows 11 Python utility which will continue an authenticated AtoZ Session initiated through a Chrome Web Browser.

It will run for 30 days, constantly checking for active VTOs and VETs. 

In the event of new opportunties being found the application will push notifications to your Alexa/Echo Dot devices.

After the 30 day session, OTP authentication has to be processed for the next 30 day session.


## Requirements

You need to run this script on a Windows 11 OS. (I do have a Mac version of this script).

You need to have Chrome Web Browser running on your Operating system.

Make sure you install Python 3.9 or greater on your Windows 11 system (along with pip3).


After completing your Python installation - install the python libraries pickle, pycryptodome and pywin32 by issusing the following commands on a command terminal -


* pip3 install pickle
* pip3 install pycryptodome
* pip3 install pywin32


Produce the source file **configure.py** (use **example_configure.py** as a template)

Fill in the AtoZ credentials 'ATOZ_USERNAME' and 'ATOZ_PASSWORD' with your own user name and password.

Fill in the 'NOTIFICATIONS_TOKEN' with your own notify-me skill token.

## Notify Me Alexa Skill

Read the document **Amazon-Alexa-Access-Code-Guide.pdf** found in the docs folder (courtesey of Protesus.com). This gives instructions on how to set up notifications on your alexa devices.

Make sure you copy your token into your configure.py file.

Run the test script **testnotify.py** from the command console. 

**python3 testnotify.py**

If you've registered your skill correctly and copied your token into configure.py - you should get a notification on your Alexa device(s).

As per instructions in the protesus documents -

**Alexa device will not announce the message aloud upon receiving the notification. It will simply make a beep and light up the ring indicating that there are new notifications available. Amazon for safety and privacy reasons controls this. When the ring lights up, you need to ask Alexa using your normal wake word,**

**“Alexa, Do I have any notifications?”, "Alexa, What are my notifications?" or “Alexa, read my notifications”.**

**To delete notifications from your Alexa device, you can say**

**“Alexa, delete my notifications”.**



## Running the AtoZ opportunity watcher.

First, use Chrome to authenticate an AtoZ session using your credentials.

When going through AtoZ's authentication (under a Chrome Web Browser) make sure you tick on the '30 Day Trusted Device Option'.
When you have gone through the One Time Password stage (with an SMS verification code sent to your registered phone) - simply quit your browser.


Second, run the python script

**python3 start_session_from_cookies_win32.py**

### It is imperative you are not running your Chrome browser in the background at the very start of running this script!

If you leave this script running - you will get instant notifications of any opportunities offered to you as soon as management place them on their staff management system, usually 20 to 30 minutes before any push/email notifications.

The Python script can be modified to also claim opportunities.

WATCH THIS SPACE.
















