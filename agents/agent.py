from google.adk.agents.llm_agent import Agent, LlmAgent
from agents.rag_agent.agent import rag_retriever_agent
from models.email import EmailContent
from models.report import EmailReport
from tools.email_parser_tool import parse_eml_file
from tools.whois_lookup_tool import search_whois_api_ninja

email_parser_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="email_parser_agent",
    description="Parses email files (.eml format) and extracts structured email data including sender, subject, body, links, and headers.",
    instruction="""You are an email parsing agent that extracts structured information from email files. 
    When given an email file path, use the parse_eml_file tool to extract:
    - Email address of the sender
    - Host domain of the sender
    - Subject line
    - Email body content
    - All links found in the email
    - All email headers
    
    Return the parsed email data in the structured EmailContent format.""",
    # input_schema=EmailParseInput,
    output_schema=EmailContent,
    tools=[parse_eml_file]
)

background_check_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="background_check_agent",
    description="Agent runs checks on the domains validity and authenticity. Retrieving the webpages, DNS records and WHOIS records",
    instruction="""You are an domain verifing agent that verifies the authenticity, validity and credibility of a domain that sent a client an email.
    Rank the integrity from 0 to 10, 0 being completely fradualent, and 10 being well documented and transparent information.
    """,
    # input_schema=EmailParseInput,
    output_schema=EmailContent,
    tools=[search_whois_api_ninja]
)

root_agent = Agent(
    model='gemini-2.0-flash', #'gemini-3-pro-preview',
    name='email_fraud_agent',
    description="Checks User email and flags potential phishing emails and fraud emails",
    instruction="You are a helpful email fraud detection agent that checks user email and flags potential phishing emails and fraud emails",
    tools=[parse_eml_file],
    sub_agents=[email_parser_agent, background_check_agent, rag_retriever_agent],
    output_schema=EmailReport,
)