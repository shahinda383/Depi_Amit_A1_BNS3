
if __name__ == "__main__":
    print("chatbot: Hi How can i assist you today?")
    
    while True:
        user_input = input("User:  ").lower()
        response = get_response(user_input)
        print("Chatbot : ",response)
        
        if user_input == "goodbye":
            break