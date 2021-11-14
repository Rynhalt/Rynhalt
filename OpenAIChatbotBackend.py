import openai
from decouple import config

openai.api_key = config('API_KEY')
class chat():
    def __init__(self):
        self.messages = ["Python chatbot\n\n\n",
        "You: How do I combine arrays?\n",
        "Python chatbot: You can use the + operator.\n",
        "You: Can you give me an example?\n", 
        "Python chatbot: Sure!\n#start\nlist1 + list2\n#list2 will be appended to the end of list1\n#end\n",
        "You: How do I output to the console?\n",
        "Python chatbot: You can use the print() function.\n",
        "You: How would I use it?\n", 
        "Python chatbot: Like this:\n#start\nprint(string1)\n#end",
        ]
        self.messagesString = ""

    def sendMessage(self, messageSent):
        self.response, self.messagesList = self.sendMessage(messageSent, self.messagesList)
        self.messagesString = ""
        for message in self.messagesList:
            self.messagesString += message
        self.messagesList.append("You: " + messageSent + "\n")
        self.messagesString += "You: " + messageSent + "\n"
        return self.returnResponse(self.messagesString, self.messagesList)

#Use sendMessage() where messageSent is the current string, and messagesList is a database of that user's current messages in the chat, returns new list and a response string
    def sendMessage(self):
        messagesString = ""
        for message in self.messagesList:
            messagesString += message

        self.messagesList.append("You: " + self.messageSent + "\n")
        messagesString += "You: " + self.messageSent + "\n"
        return self.returnResponse(messagesString, self.messagesList)


    def returnResponse(self):
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=self.messagesString,
            temperature=0,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["You:"]
        )
        self.messagesList.append(response["choices"][0]["text"] + "\n")
        return response["choices"][0]["text"], self.messagesList


while True:
    chat = chat()
    chat.sendMessage(input("You: "))
    print("\n" + chat.messageString)
