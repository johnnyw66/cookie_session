## AtoZ cookie session - starting a python http session from an existing Chrome cookies database. 

A Windows 11 and Linux Python utility which will continue an authenticated AtoZ Session initiated through a Chrome Web Browser, it can run for 30 days, constantly checking for active VTOs and VETs. 

In the event of new opportunties being found the application will push notifications to your Alexa/Echo Dot devices.

After the month long session, One Time Password (OTP) authentication has to be completed on your Chrome browser for a new 30 day session.

Currently - I have only included the Windows 11 source on this repository.

**NOTE: THIS PYTHON APP DOES NOT NEED OR USE AN MQTT SMS GATEWAY**
[https://github.com/johnnyw66/MQTT-SMS-Gateway]



## Requirements

You need to run this script on a Windows 11 OS.

You need to have Chrome Web Browser running on your Operating system.

Make sure you install Python 3.9 or greater on your Windows 11 system (along with pip3).


After completing your Python installation - install the python libraries pickle, pycryptodome and pywin32 by issusing the following commands on a command terminal -


* pip3 install pickle
* pip3 install pycryptodome
* pip3 install pywin32
* pip3 install requests



Produce the source file **configure.py**. Use **example_configure.py** as a template, copying this to make **configure.py**.

Open your new **configure.py** source file in your favourite text editor.

Fill in the AtoZ credentials **ATOZ_USERNAME** and **ATOZ_PASSWORD** with your own user name and password.

Fill in the **NOTIFICATIONS_TOKEN** with your own notify-me skill token. See details below on what this token is used for.


## Notify Me Alexa Skill

Read the document **Amazon-Alexa-Access-Code-Guide.pdf** found in the docs folder (courtesey of Protesus.com). This gives instructions on how to set up notifications on your alexa devices.

Make sure you copy your notificatoins token into your **configure.py** file.

Run the test script **testnotify.py** from the command console. 

**python3 testnotify.py**

If you've registered your skill correctly and copied your token into configure.py - you should get a notification on your Alexa device(s).

As per instructions in the protesus documents -

**Alexa device will not announce the message aloud upon receiving the notification. It will simply make a beep and light up the ring indicating that there are new notifications available. Amazon for safety and privacy reasons controls this. When the ring lights up, you need to ask Alexa using your normal wake word,**

**“Alexa, Do I have any notifications?”, "Alexa, What are my notifications?" or “Alexa, read my notifications”.**

**To delete notifications from your Alexa device, you can say**

**“Alexa, delete my notifications”.**

## NEW NEW NEW JAN 2024 Voicemonkey Skill - Dynamic Announcements 

You can now make dynamic annoucements without the need for virtual buttons by signing up to a voicemonkey account - see
testannounce.py source file and go to https://voicemonkey.io to sign up for a free account.


## Don't have any Alexa devices?

With minimal Python skills you can modify the routine **notify_opportunities** to use your host computer's speaker.

Below is one example of a method I found with a google search.

Install pygame and gtts python modules.

* pip3 install gtts
* pip3 install pygame


```
from gtts import gTTS
import pygame
import io
import tempfile

def notify_opportunities(text):
    # Create a gTTS object and get the speech as an in-memory stream
    tts = gTTS(text)
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)

    # Save the in-memory stream to a temporary file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio_file.write(speech_stream.getvalue())
    temp_audio_file.close()

    # Load and play the audio from the temporary file
    pygame.mixer.music.load(temp_audio_file.name)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)




pygame.init()
notify_opportunities("You have 1 VTO opportunity!")
pygame.quit()

```


**NEW** 16 Nov 2024 - Make your Smart Speaker announce opportunities - See **README.md** in the **virtual_button** directory



## Running the AtoZ opportunity watcher.

First, use Chrome to authenticate an AtoZ session using your credentials.

When going through AtoZ's authentication (under a Chrome Web Browser) make sure you tick on the '30 Day Trusted Device Option'.
When you have gone through the One Time Password stage (with an SMS verification code sent to your registered phone) - simply quit your browser.


Second, from a terminal command line, run the DOS batch script

**cookie_session.bat**

Currently - there is no clean mechanism to notify you of the need to go through the OTP process. 

Every 30 days you will need to stop this script, use your Chrome browser to go through the OTP stage - before re-running the script.


### It is imperative you are not running your Chrome browser in the background at the very start of running this script!

If you leave this script running - you will get instant notifications of any opportunities offered to you as soon as management place them on their staff management system, usually 20 to 30 minutes before any push/email notifications.

The Python script can be modified to also claim opportunities.

WATCH THIS SPACE.




### WARNING - 'Restful API' to be deprecated?

Looking at the new AtoZ website - it appears that the mechanisim for retrieving data is made using **GraphQL** - so I've no idea how long the old API will be supported for. This is unfamiliar technology to me - but I have worked out how to retrieve active opportunities. See the example code below.

Grabbing opportunities by GraphQL mutation will hopefully follow very shortly.



```

def get_active_opportunities(session, employee_id):

    graphql_url = f"https://atoz-api-us-east-1.amazon.work/graphql?employeeId={employee_id}"

    query = """ query OppsPage($timeRange: DateTimeRangeInput!, $opportunityTypes: TypeFilter!, $filter: ShiftOpportunitiesFilter) {
  shiftOpportunities(timeRange: $timeRange, filter: $filter) {
    opportunities(opportunityTypes: $opportunityTypes) {
      ...OppCard_shiftOpportunity
      __typename
    }
    __typename
  }
}
fragment OppCard_shiftOpportunity on ShiftOpportunity {
  id
  type
  skill
  eligibility {
    isEligible
    unclaimableReasonCodes
    __typename
  }
  unavailability {
    reasons
    __typename
  }
  shift {
    timeRange {
      start
      end
      __typename
    }
    __typename
  }
  __typename
}
    """

    response = session.post(url= graphql_url,
            json = {
                "operationName":"OppsPage",
                'variables': {
                    'timeRange': {
                        'start':'2023-11-21T10:00:00.000Z',
                        'end':'2024-01-31T10:00:00.000Z'
                    },
                    'filter': {
                            'includeIneligible': False,
                             #"unavailableReasonsToInclude": [
                             #                               "AssociateAccepted",
                             #                               "ShiftOpportunityCapacityMet"
                             # ]
                    
                    },
                    "opportunityTypes": {
                            # VOLUNTARY_TIME_OFF, VOLUNTARY_EXTRA_TIME
                            "types": [
                                        "VOLUNTARY_TIME_OFF",
                                        "VOLUNTARY_EXTRA_TIME",

                                        ]
                    }
                },
                'query':query

              },
            headers={
                'X-Atoz-Client-Id': 'SCHEDULE_MANAGEMENT_SERVICE',
            }
    )
    return response
 
```







