import requests
import configure

def voicemonkey_announce(announcement):
    print(f"announce: '{announcement}'")
    res = requests.get("https://api-v2.voicemonkey.io/announcement",
            params = {
            'token': configure.VOICEMONKEY_TOKEN,
            'device': 'annoucegroup', #Typo
            'text':announcement
            }) 
    print(f"VoiceMonkey: {res.text}")

def notifyme_announce(announcement):
    """ Announce messages using Echo Dot Devices and the Notify-Me Skill """
    print(f"announce: '{announcement}'")
    res = requests.post("https://api.notifymyecho.com/v1/NotifyMe",
            json = {
            'accessCode': configure.NOTIFICATIONS_TOKEN,
            'notification': announcement
            }) 
    print(f"NotifyMe: {res.text}")


def announce(announcement):
    voicemonkey_announce(announcement)
    notifyme_announce(announcement)



announce('You have 3 opportunities')

