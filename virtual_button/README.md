## Making your Smart Speaker - announce AtoZ opportunties - using the Virtual Buttons Alexa skill.

Instead of using 'Notify-Me' - (which is useful for making 'dynamic' notifications') you may want to opt for yor smart speaker to make instant warnings on any AtoZ opportunities that appear. You can do this by making use of the Echo Dot **routines** and the 'announce' feature. 

Announcement messages are instant - but have the disadvantage that once triggered and spoken - are lost forever. It is possible to use both Notify-Me and Announcements together.'Announcements' come from running **routines** initiated in your phone's Alexa app and can not be 'dynamic'.

So, it is very difficult to say pharses like 

'You have 4 VET opportunties and 1 VTO opportunity' - (You would need to buy lots of Virtual buttons to do this!)

Instead you would have your smart speaker announce something like - 

'You have Opportunties'

## Signing up for the Virtual Button Service

Follow the instructions 

https://www.patreon.com/VirtualButtons/posts

It's usually a paid for service but can just register for ONE virtual button for free. We use this free button to trigger an Alexa ANNOUNCEMENT (rather than use Notify-Me).

Once you've signed up for 'Virtual Buttons Skill' - you will have one Free 'Virtual Button' which can be used to turn on Smart Home Devices as well as make announcements on your Alexa/Echo Dot speakers. Look out for a email from the Virtual Button Service - containing your API token/key. You need to use this in your Python code.

## Setting up Your Smart Speaker

First you need to make sure that the Virtual Button appears in your list of 'Home Devices' -

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


## Restful API Example 

Make sure Python is set up to use the 'requests' library.

**pip3 install requests**




Alexa announcements can happen on all your Alexa devices.

So - have something like

**'YOU HAVE OPPORTUNTIES - HURRY UP AND MAKE A CLAIM.'**



In the source code - **restful_alex_virtualbutton.py**  Modify the line - 

```
key="amzn1.ask.account.DEMOAFYSA4FJJTDRNMZDEMOB4GQ2LN4OMLM6NOKCXAQTWYAOK4JYHKO5BOO54HHZ3RR4WKQ4MFV2Y654KEIDX3C2NW2DEMO2LJB54TBDEMOVLHIPQVLA" 
 ```

with your own virtual button secret key - sent to you in an email after your signed up.


When you have saved your modified source - run it!

**python3 restful_alex_virtualbutton.py**

It should respond with status code **200** or **202**.

If you get **500** - check your API token/key.



