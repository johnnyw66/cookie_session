## Restful API Example 


pip3 install argparse


Follow the instructions 

https://www.patreon.com/VirtualButtons/posts

It's usually a paid for service but you get ONE virtual button for free - so we can trigger an Alexa ANNOUNCEMENT (rather than use Notify-Me).


Alexa annoucements can happen on all your Alexa devices.

So - have something like

**'YOU HAVE OPPORTUNTIES - HURRY UP AND MAKE A CLAIM.'**



In the source code - **restful-**  Modify the line - 

'''
key="amzn1.ask.account.DEMOAFYSA4FJJTDRNMZDEMOB4GQ2LN4OMLM6NOKCXAQTWYAOK4JYHKO5BOO54HHZ3RR4WKQ4MFV2Y654KEIDX3C2NW2DEMO2LJB54TBDEMOVLHIPQVLA" 
 '''

with your own virtual button secret key - sent to you in an email after your signed up.


Once you've signed up for 'Virtual Buttons Skill' - you will have one Free 'Virtual Button' which can be used to turn on Smart Home Devices as well as make annoucements on your 
Alexa/Echo Dot speakers.


First you need to make sure that the Virtual Button appears in your list of 'Home Devices' -

Say to your Echo Dot/Alexa Speaker:-

'<ECHO>, Scan Devices.'  (<ECHO> is your Wake word.)

Your Echo Dot should respond with 'Started Discovery, ... put them in pairing mode.' - (You don't have to 'pair' anything - our button is virtual).

After a few seconds, it should tell you it found a virtual button (Virtual Button 1), so we can go on to the next stage in writing a simple routine on our alexa app.
  



On your 'Alexa App' (on your phone?) - You need to set up a new **Routine**


Launch the Alexa app on your mobile device

Tap the more/menu icon (usually lower right part of screen) and select Routines

* Select the + icon in the top right corner
* Select When This Happens, then select Smart Home and choose the Virtual Button 01 device. Select Save
* Select Add action, then select Alexa Annouce, and then input the text you want your speaker to say (for example 'OPPORTUNTIES ARE OPEN! MAKE HASTE!'). 
* Select Next in the top right corner.
* Select Choose Device, and then select the Alexa device you want to speak. Select Save in the top right corner.

 


