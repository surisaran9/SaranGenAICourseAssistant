import streamlit as st

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages
        #self.employee_information = assistant.employee_information

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        messages = self.messages

        for message in messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            if message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def set_state(self, key, value):
        st.session_state[key] = value

    def render_user_input(self):

        user_input = st.chat_input("Type here...", key="input")
        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)

            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})

            self.set_state("messages", self.messages)

    def render(self):

        with st.sidebar:
            # st.logo(
            #     "https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg"
            # )
            # st.logo(
            #     "./data/logo.png"
            # )

            st.image("./data/logo1.png", use_column_width=True)
            #st.title("Saran GenAI Course Assistant")
            st.sidebar.markdown("<h1 style='text-align: center;'>Saran GenAI Course Assistant</h1>", unsafe_allow_html=True)
            st.sidebar.markdown("<h2 style='text-align: center;'>WhatsApp@9999457026</h2>", unsafe_allow_html=True)
            #st.sidebar.markdown("<h300 style='text-align: center;'>WhatsApp@9999457026</h300>", unsafe_allow_html=True)


            #st.subheader("Employee Information")
            #st.write(self.employee_information)

        self.render_messages()
        self.render_user_input()
