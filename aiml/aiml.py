import sys
sys.path.insert(0, "PyAIML")

import aiml
#import os

# The Kernel object is the public interface to
# the AIML interpreter.
kernel = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
kernel.learn("inicial.xml")


kernel.respond("LOAD AIML B")

# Loop forever, reading user input from the command
# line and printing responses.
while True: 
	print kernel.respond(raw_input("HABLAME...> "))
