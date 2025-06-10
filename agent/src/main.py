from LLMClient import LLMClient
from PineconeHandler import PineconeHandler
#from Users import MongoHandler

class Agent:
    
    def __init__(self, reasoningModel=True, contextPrompt="../config/contextPrompt.txt", topK=5, targetThreshold=0.5900, minimumThreshold=0.3400, maxHierarchyLevel=3):
        
        self.contextPrompt = self.loadInitialPrompt(contextPrompt)
        self.pineconeHandler = PineconeHandler(topK, targetThreshold, minimumThreshold, maxHierarchyLevel)
        self.llmClient = LLMClient(reasoningModel)
        #self.mongo_handler = MongoHandler("mongodb://localhost:27017/", "md", "users")
        
    def loadInitialPrompt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
        
    def submitQuestion(self, prompt):

        username = "sophie_lee24"

        #user_data = self.mongo_handler.getUserData(username)
        #user_data_prompt = self.mongo_handler.generateUserDataPrompt(user_data)
        
        context = self.pineconeHandler.query(prompt)
        
        if context == "":
            print("The articles do not provide enough information to answer completely.")
            return
        
        # Create the final prompt for the LLM
        finalPrompt = (
            f"{self.contextPrompt}\n\n"
            #f"{user_data_prompt}"
            "Question:\n"
            f"{prompt}\n\n"
            "Articles context:\n"
            f"{context}"
        )

        # # Debugging output 
        # print("\nAll context:")
        # print(finalPrompt)
        # print("########")
        # print("########")
        # print("########\n")
        
        
        # Get the LLM response
        try:
            response = self.llmClient.generateResponse(finalPrompt)

            print("Response:")
            print(response)
            return response
            
        except Exception as e:
            raise
            

if __name__ == "__main__":
    agent = Agent(reasoningModel=True)
    while True:
        # Prompt the user for a question
        prompt = input("\n\nAsk anything (or 'EXIT' to leave): \n>>>")

        if prompt.strip().upper() == "EXIT":
            break
        
        # Retrieve relevant chunks using the embeddings
        agent.submitQuestion(prompt)
