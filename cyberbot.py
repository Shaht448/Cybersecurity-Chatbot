import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import gradio as gr

# In[5]:
load_dotenv()

class ChatBot:
    def __init__(self,
                 name: str,
                 instructions: str,
                 model: str = "gpt-4o-mini",
                 temperature: float = 0.8):
        self.name = name

        # TODO - Instantiate your chat model properly
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )


        self.messages = [SystemMessage(content=instructions)]

        # Add few-shot examples manually
        for ex in examples:
            self.messages.append(HumanMessage(content=ex["input"]))
            self.messages.append(AIMessage(content=ex["output"]))

    def invoke(self, user_message: str) -> AIMessage:
        self.messages.append(HumanMessage(content=user_message))
        ai_msg = self.llm.invoke(self.messages)
        self.messages.append(ai_msg)
        return ai_msg


system_prompt = """You are a user-friendly Cybersecurity Assistant.

Your role is to help users understand cybersecurity threats, stay safe online, and improve their overall digital security awareness.

You must:
- Explain cybersecurity concepts in simple, clear, and non-technical language.
- Promote cybersecurity threat awareness and safe online behavior.
- Help users understand common risks related to the internet, networks, devices, and applications.
- Provide guidance on safety, protection, and prevention—not attacks.

Core Focus Areas:
- Common cybersecurity threats (phishing, malware, scams, data breaches).
- Network and internet security basics (Wi-Fi safety, public networks, passwords).
- Everyday cybersecurity knowledge for normal users.
- Incident awareness: how to recognize suspicious activity and what steps to take.
- Personal and organizational safety best practices.

Rules:
- Never provide hacking, exploitation, or illegal instructions.
- If asked about attacks, redirect to prevention, detection, or awareness.
- Keep all advice ethical, defensive, and safety-focused.
- For cybersecurity question always give 'how it works'.

Mandatory Output Format (for every cybersecurity question):
- Definition (1-2 lines)
- How it works (2-5 bullets)

Response Style:
- Friendly, calm, and easy to understand.
- Use bullet points and short explanations.
- Focus on awareness, protection, and practical safety tips.

Your goal is to help users stay informed, protected, and confident while using the internet and digital systems"""

#
examples = [{
    "input": "what is phishing?",
    "output": """It is a type of attack where scammers try to extract personal information for instance, password, bank detail, othre sensitive information. 
    how it works: 
    - attcker send fake emails, text messgaes or website that looks like they came from the trusted sources. 
    - when users click the link or enter their detail in an instance attcker got their all personal informations."""},

    {
        "input": "How can i protect my laptop from the viruses?",
        "output": """To protect your laptop from viruses, install reputable antivirus software (e.g., Microsoft Defender), keep your operating system updated, avoid clicking suspicious links or downloading unknown attachments, and use a firewall. Antivirus software works by scanning files for known malware signatures, monitoring behavior for suspicious activity in real-time, and isolating threats.
    how it works: 
    - Keep your operating system (Windows/macOS) and applications patched to close security gaps. 
    - Avoid clicking on unexpected links in emails, and do not download software from untrusted sources. 
    - Use a firewall to block unauthorized network access."""}

]


bot = ChatBot(name = "Alax", instructions = system_prompt)
def respond(message, history):
    return bot.invoke(message).content
gr.ChatInterface(
    fn=respond,
    title="Cybersecurity Assistant",
    description="Ask questions about online safety, phishing, malware, and scams."
).launch(share=True)
