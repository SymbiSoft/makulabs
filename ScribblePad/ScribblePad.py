# Scribble Pad v0.2
# Distributed under GNU GPL License.

# For any comments/suggestions/...
# please contact makuchaku at 
# mayank.gnu@gmail.com
# http://makuchaku.tk
# Scribble Pad uses Unicode (to-&-fro) conversions, based on "Myeditor.py" code.

import appuifw
import codecs
import e32

class ScribblePad:
	
	def __init__(self):
	        self.lock = e32.Ao_lock()

		# For restoration
		old_title = appuifw.app.title
		appuifw.app.title = u"Scribble Pad"
		
		# For new usage
		menu_save = (u"Save", self.on_menu_save)
		menu_open = (u"Open", self.on_menu_open)
		menu_exit = (u"Exit", self.on_menu_exit)
		
		appuifw.app.body = appuifw.Text()
		appuifw.app.menu = [menu_save, menu_open]
		
		appuifw.app.exit_key_handler = self.on_menu_exit
	        
	        # Needed to keep Form visible to UI
	        self.exit_flag = False
	        self.loop()
	
	def on_menu_save(self):
		# When this is called, app.body is set to a TextBox.
		# Hence get() will return the unicode text.
		path_to_save = appuifw.query(u"Where to save?","text", u"E:\\System\\Apps\\python\\my\\")
		if path_to_save == None:
			return
		(encoding,decoding,reader,writer) = codecs.lookup('UTF-8')
		# All this needed for unicode <--> UTF-8 conversion
		text = appuifw.app.body.get().encode('utf8').replace("\xE2\x80\xA9","\x0D\x0A")
		try:
			output = open(path_to_save,'wb')
			output.write(text)
			output.close()
		except IOError:
			appuifw.note(u"Error in writing to the file!", "error")

	def on_menu_open(self):
		path_to_open = appuifw.query(u"Where to open from?","text", u"E:\\System\\Apps\\python\\my\\")
		if path_to_open == None:
			return
		(encoding,decoding,reader,writer) = codecs.lookup('UTF-8')
		try:
			input = reader(open(path_to_open,'rb'))
			appuifw.app.body.set(input.read())
			input.close()
		except IOError:
			appuifw.note(u"The file does not exist!", "error")
		
	def on_menu_exit(self):
	        # Needed to exit
	        self.exit_flag = True
                self.lock.signal()
	        
	# Needed to keep Form visible to UI
	def loop(self):
		while not self.exit_flag:
			self.lock.wait()
	 

if __name__ == "__main__":
	sp = ScribblePad()
	appuifw.note(u"Thank you for using Scribble Pad v0.2 ;-)\nhttp://makuchaku.tk", "info")

