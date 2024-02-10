import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import os

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ''


def getLLMResposne(form_input, email_sender, email_recipient, email_style):
    try:
        # llm = CTransformers(
        #     model = "models/llama-2-7b-chat.ggmlv3.q2_K.bin",
        #     model_type = 'llama',
        #     config = {'max_new_tokens':256,
        #               'temperature':.01}
        #     )

        llm = OpenAI(temperature=.9)

        template = """
        write an email with {style} style and includes topic: {email_topic}\n\nSender: {sender}\n\nRecipient: {recipient}
        keep the email short and crisp in 150-200 words.
        \n\nEmail Text:

        """

        prompt = PromptTemplate(
            input_variables=["style", "email_topic", "sender", "recipient"],
            template=template,
        )

        response = llm(prompt.format(email_topic=form_input,
                                     sender=email_sender,
                                     recipient=email_recipient,
                                     style=email_style))

        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"



def main():
    st.set_page_config(
        page_title = "Generate Emails",
        page_icon = "📨",
        layout = "centered",
        initial_sidebar_state = "expanded"
    )

    st.header("Generate Emails 📨")

    open_api_key = st.sidebar.text_input("Enter OpenAI API Key")
    st.sidebar.write("⬆️ Enter your OpenAI API key ")

    os.environ["OPENAI_API_KEY"] = open_api_key


    form_input = st.text_area("Enter the email topic", height = 275)

    col1, col2, col3 = st.columns([10,10,5])
    with col1:
        email_sender = st.text_input("Sender name")
    with col2:
        email_recipient=st.text_input("Recipient name")
    with col3:
        email_style = st.selectbox(
            'Writing style', ('Formal','Appreciating','Not Satisfied','Neutral'),
            index=0
        )


    submit = st.button("Generate")

    if submit:
        with st.spinner():
            st.write(getLLMResposne(form_input, email_sender, email_recipient, email_style))

if __name__=='__main__':
    main()
