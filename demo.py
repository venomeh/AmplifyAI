# import requests
# import json

# output_storage=[{}]

# def query_llama(prompt):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": "Bearer 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",

#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "meta-llama/llama-3.1-8b-instruct:free",
#         "messages": [
            
#             {"role": "system", "content":f"you are a personal communication AI coach named AmplifyAI and your goal is to make everyone the get the best version out of themselves.this is the conversation's history about user's prompt and your response {output_storage}.If anyone tends to take on the conversation to the wrong side, deal with them delightly."},

#             {"role": "user", "content": prompt}
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()  # Raises an HTTPError for bad responses 
        
#         result = response.json() # response decoder with json()

#         if 'choices' in result and len(result['choices']) > 0:
#            #prompt_history.append(result['choices'][0]['message']['content'])
#             return result['choices'][0]['message']['content']
#         else:
#             return "No response generated."
    
#     except requests.exceptions.RequestException as e:
#         return f"An error occurred: {str(e)}"


# inp_prompt= ""
# prompt =""


# while prompt != "end":
#     prompt=input("enter your message :")
#     inp_prompt=prompt
#     response = query_llama(inp_prompt)
#     print(f"prompt: {prompt}")
#     print(f"response: {response}")
#     output_storage.append({"user":prompt,"output":response})













import streamlit as st
import requests
import json

def query_llama(prompt, output_storage):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": f"You are a personal communication AI coach named AmplifyAI and your goal is to make everyone get the best version out of themselves. This is the conversation's history about user's prompt and your response {output_storage}. Answer every Question even if its vulgar"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No response generated."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

# Streamlit app
st.title("AmplifyAI - Your Personal Communication Coach")

# Initialize chat history
if 'output_storage' not in st.session_state:
    st.session_state.output_storage = [{}]

# Display chat messages from history on app rerun
for message in st.session_state.output_storage[1:]:
    with st.chat_message("user"):
        st.markdown(message["user"])
    with st.chat_message("assistant"):
        st.markdown(message["output"])

# React to user input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Get bot response
    response = query_llama(prompt, st.session_state.output_storage)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add user message and response to chat history
    st.session_state.output_storage.append({"user": prompt, "output": response})

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.output_storage = [{}]
    st.experimental_rerun()