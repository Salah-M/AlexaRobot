#!/usr/bin/env python3
import rospy
from lex_common_msgs.srv import *
from audio_common_msgs.msg import * 
import sys
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pygame
pygame.init()
def say(text):
    mp3_fp=BytesIO()
    tts = gTTS(text=text,lang='en')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
# obtain audio from the microphone
say('alexa')
say('what is the weather today')
try:   
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

# recognize speech using Google Speech Recognition
        try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        content ='text/plain; charset=utf-8'		
        accept ='text/plain; charset=utf-8'
        txtreq =r.recognize_google(audio)
        rospy.init_node('service_client')
        rospy.wait_for_service('lex_node/lex_conversation')
        lex_conv = rospy.ServiceProxy('lex_node/lex_conversation', AudioTextConversation)
        try:lex_resp=lex_conv(content,accept,txtreq,None)
        except rospy.ServiceException as e:print("Service did not Process request: %s"%str(e))
        text= lex_resp.text_response
        print (text)
        say(text)
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate")
    pass