#!/usr/bin/python

import sys, getopt
def main(argv):
    short_options = "hreo:v"
    long_options = ["help", "run", "exit", "output=", "verbose"]
    try:
        arguments, values = getopt.getopt(argv, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)
    # Evaluate given options
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            print ("Enabling verbose mode")
        elif current_argument in ("-h", "--help"):
            print("To run the program \t -r")
            print("To exit the program \t -e")
        elif current_argument in ("-r", "--run"):
            import hashtag
            hashtag.runsetup()
        elif current_argument in ("-e", "--exit"):
            print('Godbye')
            sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
