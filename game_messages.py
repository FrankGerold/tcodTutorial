import tcod
import textwrap

class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        #split message on multiple lines if necessary
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            #if buffer is full, remoge first line to make room
            if len(self.messages) == self.height:
                del self.messages[0]

            #add new line as Message object, with text and color
            self.messages.append(Message(line, message.color))
