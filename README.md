## ESP32 NextCloud chatbot 
Using MicroPython on an ESP32, the included code manages a network connection with a remote NextCloud server. The device signs in as a predefined user in order to send and receive messages in a dedicated chatroom. The application which manages the chat session is Nextcloud Talk. Any new message received in the chatroom will be analyzed, processed and displayed an LCD1602 display. For creativity purposes, I added 9 of these displays. The same message is shown on all of them. The backlight on each display however is individually activated by different pins on the ESP32. An animation code is included to illustrate multiple sequences that were prepared. This is done electronically by sending PWM signals to a network of a BC337 transistors, one for each screeen. 

<p align="center">
  <img src="images/screens-small.jpg" />
</p>

### Hardware Used
- **LOLIN D32 V1.0.0 (ESP32)**
- **LCD1602** (x9)
- **BC337 Transistors**

<p align="center">
  <img src="images/circuit-small.jpg" />
</p>


### Custom modules and their source links
- **[LCD](https://github.com/rdagger/micropython-charlcd)**
- **[uping](https://gist.github.com/shawwwn/91cc8979e33e82af6d99ec34c38195fb)**

### Notes on some of the internal modules used
- **urequest** is used to manage communication with the NextCloud Talk API
- **ubinascii** is required for managing encryption of username and password

### Required code modifications
- **main.py** : credentials for your nextcloud server must be provided (url, username, password, chatroom token)
- **netconn.py** : credentials for local routers are required (SSID, password). This is prepared as a list, in case you wish to test multiple routers.

### Code usage and behavior
All included code must be uploaded to the ESP32 in order to run **main.py** . When the device boots, it will connect to the router and announce on the LCD display that it is connecting to the network. Once it has connected, it will then begin an animated sequence of the multiple displays. The code **dictionary.py** provides a list of messages that will be randomly displayed on the screens. This is the default sequence. <br/>
At the moment the bot connects to the dedicated NextCloud chatroom, it will send a chat message to notify chat users that it is online. It will then await the next message. If the message sent is under 32 characters length, it will then be analyzed and cut for compatibility with the 16x2 display. If all goes well, the chatbot will respond with a chat to verify success. If something goes wrong, the chatbot will respond and describe the error.<br/>
Commands are also prepared for the chatbot. To send a command, simply begin the message with dollar sign. To get a list of available commands simply type \$help.

<br/>

### Chatroom Debugging

The following curl commands are useful for initial testing of the chat server. Open a Linux terminal and follow the given instruction to make sure we have basic send and receive working.

```bash
#------------------- get last message in chat feed ----------------------
#change username and password. Replace URL with your domain name. Replace the xxxxxxxx with your room token.

curl -k -s -u "username:password" -H "OCS-APIRequest: true" -X GET "https://yourDomainName.ddns.net/ocs/v1.php/apps/spreed/api/v1/chat/xxxxxxxx?lookIntoFuture=0&limit=1&setReadMarker=1" | grep "<message>" | sed -r "s|<?/message>||g" | tail -1

#-------------------- post a message in chat feed -----------------------
#Change chatRoom name for the name of your chat room. Chage someOtherUser to the name of a user to whom you wish to address the message. Change username and password. Replace URL with your domain name. Replace the xxxxxxxx with your room token.
curl -d '{"chatRoom": "chatRoom", "message": "Hello World @someOtherUser"}' -H "Content-Type: application/json" -H "Accept: application/json" -H "OCS-APIRequest: true" -u "username:password" https://yourDomainName.ddns.net/ocs/v1.php/apps/spreed/api/v1/chat/xxxxxxxx
```

### References:
- [NextCloud Talk API](https://nextcloud-talk.readthedocs.io/en/latest/chat/)
- [Excellent ressource for 1602 LCD display](https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/)
- [micropython urequests documentation](https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html)
