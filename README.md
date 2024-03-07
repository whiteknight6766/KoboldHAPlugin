# KoboldHAPlugin
This is the code repo as submitted for the Home Assistant voice code challenge. Because I need documention for the challenge. 

# Prerequisites:
1. A Kobold Horde API Key. Freely available at https://horde.koboldai.net/register<br>
2. A Python3 enviroment<br>
3. The pip packages requests and http3 <br><p>
        I had trouble installing http3 with pip version 20 but it does install with 23.3.2<br>
        My notes say "apt update && apt upgrade followed by a reboot." <br>
        Alot of my issues may have been caused by spinning up a fresh ubuntu server 20.4. However, I am leaving these bread crumbs in case the user is also not updating their OS enviroment. <br>
        
# Setup:
1. Get this repo into the "homeassistant/custom_components" folder. <br>

        git pull https://github.com/whiteknight6766/KoboldHAPlugin

2. Reboot HomeAssistant. <br><p>
3. From the main dashboard:<br><p>
  Click settings, <br><p>
  Click devices and services,<br><p>
  Add integration, "Kobold conversation"<br><p>
      The first box is for a human friendly name<br><p>
      The second box is your API key -go get one its free- <br>
          The default is the horde Anonymous user, complete with end of the line privlidges. That key is 0000000000<br><p>
      Third box is the base url, this should be the default as entered. <br>
      However, the local version of Koboldcpp does has its own API. So you could point that at your local machine for full offline mode if that is your particular kink. Head on over to https://github.com/LostRuins/koboldcpp and check them out.<br>

# Initialize your assistant  
1. From the main dashboard:<br><p>
  Click Settings<br><p>
  Click Voice Assistants<br><p>
  Click Add Assistant<br><p>
      Name: Again a human friendly name, your choice. <br><p>
      Conversation agent: You should see the human friendly name you entered during initialization. Chose that. <br><P>
      *** all other options are up to you. TTS and STT are not part of this scope. This is just a conversation agent. Wyoming protocol and "google en com" works well enough for me. See these guys: https://github.com/rhasspy/wyoming-faster-whisper<br><P>
      I do suggest setting up a unique wake word. I am useing "ok nabu" for device control and a second assistant all together with ok jarvis for the kobold conversation agent.
  Repeat as many time as desired for different Kobold agents. one anonymous, one with your API Key, one with your significant others api key, you do you. <br><P>

# Use the Conversation agent from the dashboard:
Click the conversation icon in the upper right corner. <br><p>
A new box pops up, Under the word "assist" there is a drop down menu. <br>
  Make that read your second human friendly name that you assigned to the assistant. <br><p>
    
# Uninteresting conjecture on the personal reflection of my attempts to code this: (I.E. Troubleshooting tips)   
During my testing the anonymous key gave me the following response. <br><p>
    "Due to heavy demand, for requests over 463 tokens, the client needs to already have the required kudos. This request requires 78.57 kudos to fulfil."<br><p>
    I highly recommend getting a free API key. <br><p>

If you care to see whats happening, I intentionally left my debugging events firing in the code. <br><p>
    1. Open a seperate browser<br><p>
    2. Goto Developer tools from your home assistant<br><p>
    3. Select "events tab"<br><p>
    4. In the "listen to evenets" enter "kobold_event" <br><p>
      These events are the communication to and from the horde API. You can see the prompt, the models, temperature settings ect. <br><p>
      Yes its very chatty, particularly after the generation request.<br><p>
        the API responds with an "expected time frame." Kobold Conversation plugin uses this time to hang around and wait. Yes there is a nasty gram in the *.log file, something about a "blocking wait, please contact the author." Kobold Conversation plugin will recheck the Horde's API every half interval. the API does give an updated generation time estimate if the generation isn't complete. and that loop continues until one of two things happens. The horde sends a generated response, OR 20 seconds has elapsed. Home Assistant has a maximum time limit before it gives up. To which I will re-pursade you to get a horde API key. the Key is free, and gets your generation request ahead of the anonymous ones. 
