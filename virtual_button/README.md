## Making your Smart Speaker - announce AtoZ opportunties - using the Virtual Buttons Alexa skill.

Instead of using 'Notify-Me' - (which is useful for making 'dynamic' notifications) you may want to opt for yor smart speaker to make instant warnings on any AtoZ opportunities that appear. You can do this by making use of the Echo Dot **routines** and the 'announce' feature. 

Announcement messages are instant - but have the disadvantage that once triggered and spoken - are lost forever. It is possible to use both Notify-Me and Announcements together. 'Announcements' come from running **routines** initiated in your phone's Alexa app and can not be 'dynamic'.

This means it is very difficult to say pharses like 

'You have 4 VET opportunties and 1 VTO opportunity' - (You would need to buy lots of Virtual buttons to do this!)

Instead you would have your smart speaker announce something like - 

'You have Opportunties'

Edit: **NEW** Jan 2024. Since writing the above - I have discovered a new service called 'Voice Monkeys' https://voicemonkey.io/ which allows dynamic annoucements.

```
def voicemonkey_announce(announcement):
    logging.info(f"announce: '{announcement}'")
    res = requests.get("https://api-v2.voicemonkey.io/announcement",
            params = {
            'token': configure.VOICEMONKEY_TOKEN,
            'device': 'annoucegroup', #Typo
            'text':announcement
            }) 
    logging.info(f"VoiceMonkey: {res.text}")

def notifyme_announce(announcement):
    """ Announce messages using Echo Dot Devices and the Notify-Me Skill """
    logging.info(f"announce: '{announcement}'")
    res = requests.post("https://api.notifymyecho.com/v1/NotifyMe",
            json = {
            'accessCode': configure.NOTIFICATIONS_TOKEN,
            'notification': announcement
            }) 
    logging.info(f"NotifyMe: {res.text}")


def announce(announcement):
    voicemonkey_announce(announcement)
    notifyme_announce(announcement)

```


## Signing up for the Virtual Button Service

Follow the instructions on https://www.patreon.com/VirtualButtons/posts

The is usually a paid-for service but can just register for ONE virtual button for free. You use this free button to trigger an Alexa ANNOUNCEMENT (rather than use Notify-Me).

Once you've signed up for **Virtual Buttons Skill** - you will have one free **Virtual Button** ('Virtual Button 1') which can be used to turn on Smart Home Devices as well as make announcements on your Alexa/Echo Dot speakers. After signing-up, look out for an email from the Virtual Button Service - containing your API token/key. You need to use this in your Python code.

## Setting up Your Smart Speaker

I'm assuming you have already signed up for the virtual button service. First you need to make sure that the Virtual Button appears in your list of 'Home Devices' -

Say to your Echo Dot/Alexa Speaker:-

'&lt;**ECHO**&gt;, scan devices.'  

(Note: &lt;**ECHO**&gt; is your wake word.)

Your Echo Dot should respond with 'Started Discovery, ... put them in pairing mode.' - 

(You don't have to 'pair' anything - our button is virtual).

After a few seconds, your smart speaker should tell you it found a virtual button (Virtual Button 1), so we can go on to the next stage in writing a simple routine on our alexa app.
  

On your 'Alexa App' (on your phone?) - You need to set up a new **Routine**


Launch the Alexa app on your mobile device

Tap the more/menu icon (usually lower right part of screen) and select Routines

* Select the **+** icon in the top right corner
* Select **When This Happens**, then select **Smart Home** and choose the **Virtual Button 01** device. Select **Save**
* Select **Add** action, then select Alexa **Announce**, and then input the text you want your speaker to say (eg. 'OPPORTUNTIES ARE OPEN! MAKE HASTE!'). 
* Select **Next** in the top right corner.
* Select **Choose Device**, and then select the Alexa device(s) you want announcements to be made from.
* Select **Save** in the top right corner.

You should now be ready to run some python code to trigger the virtual button and make an announcement...

### My Alexa Device keeps telling me "Somebody is at Virtual Button..." whenever I get an announcement.

To turn this off, open your Alexa App and choose the Devices icon in the lower right part of the screen.

Next choose All Devices and scroll through the list to find your Virtual Button XX device(s), select it, then switch the **Doorbell Press Announcements** slider to the off position. You might have to do this for each Virtual Button you own.



## Restful API Example 

If you've set up a routine on your Alexa app and have your API token - you are ready to start some Python coding to set off an announcement on your smart speaker.

Make sure Python is set up to use the 'requests' library.

**pip3 install requests**



In the source code - **restful_alex_virtualbutton.py**  Modify the line - 

```
key="amzn1.ask.account.DEMOAFYSA4FJJTDRNMZDEMOB4GQ2LN4OMLM6NOKCXAQTWYAOK4JYHKO5BOO54HHZ3RR4WKQ4MFV2Y654KEIDX3C2NW2DEMO2LJB54TBDEMOVLHIPQVLA" 
 ```

with your own virtual button secret key - sent to you in an email after your signed up.


When you have saved your modified source - run it!

**python3 restful_alex_virtualbutton.py**

It should respond with status code **200** or **202**.

If the response is **500** - check your API token/key.




