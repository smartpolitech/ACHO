import sys
sys.path.insert(0, "PyAIML")

import aiml

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("std-startup.xml")

k.respond("LOAD AIML B")

# Loop forever, reading user input from the command
# line and printing responses.
while True: print k.respond(raw_input("> "))
