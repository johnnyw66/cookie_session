import configure
import requests

def voicemonkey_announce(announcement, speaker='annoucegroup'):
    print(f"announce: '{announcement}'")
    res = requests.get("https://api-v2.voicemonkey.io/announcement",
            params = {
            'token': configure.VOICEMONKEY_TOKEN,
            'device': speaker, 
            'text':announcement
            }) 
    print(f"VoiceMonkey: {res.text}")

def notify_opportunities(announcement):
    print(f"notify_opportunities: '{announcement}'")
    res = requests.post("https://api.notifymyecho.com/v1/NotifyMe",
            json = {
            'accessCode': configure.NOTIFICATIONS_TOKEN,
            'notification': announcement
            }) 
    print(res.text)

def announce_opportunities(announcement):
    notify_opportunities(announcement):        
    voicemonkey_announce(announcement,


announce_opportunities('YOU HAVE OPPORTUNTIES AVAILABLE. MAKE HASTE!', speaker='annoucegroup')

