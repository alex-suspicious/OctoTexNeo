import sys

f = open( f"logs","w")
f.write( "" )
f.close()

class Logger():
    stdout = sys.stdout
    messages = ""

    def start(self): 
        sys.stdout = self

    def stop(self): 
        sys.stdout = self.stdout

    def write(self, text): 
        self.messages += text
        self.stdout.write(text)
        f = open( f"logs","w")
        f.write( self.messages )
        f.close()

log = Logger()
