#from pyblocks import quoteStatus
import pyblocks

print(pyblocks.quoteStatus("   # fdsfs", None))
print(pyblocks.quoteStatus("   dsds ''' ''' # '''", None))
print(pyblocks.quoteStatus("   dsds ''' ''' # '''", "'''"))
print(pyblocks.quoteStatus("   dsds ''' ''' # '''", '"""'))
