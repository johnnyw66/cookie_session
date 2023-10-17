import configure
import requests

def announce_opportunities(announcement):
    print(f"announce_opportunties: '{announcement}'")
    res = requests.post("https://api.notifymyecho.com/v1/NotifyMe",
            json = {
            'accessCode': configure.NOTIFICATIONS_TOKEN,
            'notification': announcement
            }) 
    print(res.text)




announce_opportunities('YOU HAVE OPPORTUNTIES AVAILABLE. MAKE HASTE!')

