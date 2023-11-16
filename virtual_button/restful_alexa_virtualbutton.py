import requests


# Simple Class to Handle Restful API for Echo Dot/Alexa 'Virtual Button' application

class RestfulAlexaVirtualButton():

    def __init__(self, url="", key=""):

        self.url = url
        self.api_key = key

    def press_button(self, button):


        print(f'press_button: button = {button}')

        session = requests.session()

        response = session.post(url = self.url,
            params = {
                    'accessCode': self.api_key,
                    'virtualButton': button
                    })

        print(f'Response : {response}')
        return response

def main():

    # Make sure you have Python 'requests' library installed
    # pip3 install requests - (one off - install)

    # Put your OWN 'Virtual Buttons' key here - (sent to you in an email - once you've signed up for the virtual button skill)
    # https://www.patreon.com/VirtualButtons/posts

    key = "amzn1.ask.account.DEMOAFYSA4FJJ5YRKNPRAHHS3KFATDRHQSUSHFJLQD6E673B5DQL3TO666PAMX3ZG4NMZAWOFO3RR4WKQ4MFV2Y654KEIDX3C2NW27JMYY32LJB54TBJTWODVRAYBVLHIPQVLA"
 
    button = 1  # You can pay for more buttons - the 1st one is free.

    restful_alexabutton_service = RestfulAlexaVirtualButton(
                                                        url = "https://api.virtualbuttons.com/v1/",
                                                        key = key)

    resp = restful_alexabutton_service.press_button(button)
    print(resp.status_code)
    print(resp.text)

if __name__ == "__main__":
    main()
