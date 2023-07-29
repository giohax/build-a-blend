def remove_whitespace_and_quotes():
    user_input = input("Please enter your message: ")
    processed_input = user_input.replace(" ", "").replace("\t", "").replace("\n", "").replace("\"", "").replace("\'", "")
    return processed_input

print(remove_whitespace_and_quotes())
