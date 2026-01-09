import gradio as gr
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
import os

# Use HF_TOKEN environment variable (set by HF Spaces automatically)
# For local testing, ensure HF_TOKEN is set in your environment
hf_token = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    task="text-generation",
    huggingfacehub_api_token=hf_token,
    max_new_tokens=400
)

template = """You are a professional LinkedIn branding expert for a cybersecurity-to-AI transitioning analyst.
Generate an engaging LinkedIn post (200-300 words) about these recent achievements:
{achievements}

Style: Professional yet enthusiastic, first-person ("I" statements), include calls to action (e.g., "Connect if you're in AI/security!"), relevant hashtags (#Cybersecurity #AI #MachineLearning #CareerTransition), and emojis sparingly.
End with a question to boost engagement."""

prompt = PromptTemplate(template=template, input_variables=["achievements"])

def generate_post(custom_input=None):
    if custom_input:
        achievements = custom_input
    else:
        try:
            with open('achievements.txt', 'r') as f:
                achievements = f.read()
        except:
            achievements = "No achievements logged yet."
    
    chain = prompt | llm
    return chain.invoke({"achievements": achievements})

iface = gr.Interface(
    fn=generate_post,
    inputs=gr.Textbox(label="Optional: Paste custom achievements (or leave blank to use achievements.txt)", lines=5),
    outputs=gr.Textbox(label="Ready-to-Post LinkedIn Draft", lines=10),
    title="LinkedIn Branding AI Agent",
    description="Generates polished posts from your logged achievements. Run weekly for consistent branding!"
)
iface.launch()