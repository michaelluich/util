import popen2
import simplejson as json

class PHP:
    """This class provides a stupid simple interface to PHP code."""
    
    def __init__(self, prefix=None, postfix=None):
        """prefix = optional prefix for all code (usually require statements)
        postfix = optional postfix for all code
        Semicolons are not added automatically, so you'll need to make sure to put them in!"""
        
        self.prefix = prefix or ""
        self.postfix = postfix or ""

    def __submit(self, code):
        (out, inp) = popen2.popen2("php")
        print >>inp, "<? "
        print >>inp, self.prefix
        print >>inp, code
        print >>inp, self.postfix
        print >>inp, " ?>"
        inp.close()
        return out

    def get_raw(self, code):
        """Given a code block, invoke the code and return the raw result as a string."""
        out = self.__submit(code)
        return out.read()

    def get(self, code):
        """Given a code block that emits json, invoke the code and interpret the result as a Python value."""
        out = self.__submit(code)
        return json.loads(out.read())

    def get_one(self, code):
        """Given a code block that emits multiple json values (one per line), yield the next value."""
        out = self.__submit(code)
        for line in out:
            line = line.strip()
            if line:
                yield json.loads(line)

