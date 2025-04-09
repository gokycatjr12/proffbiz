import streamlit as st
import openai
import PyPDF2
from streamlit_card import card

# 🔐 Check if OpenAI key is set in secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("🚫 OpenAI API key not found. Please set it in Streamlit Cloud secrets.")
    st.stop()

# ✅ Secure OpenAI Client Setup using the secret
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🧠 App Introduction
st.title("👋 Welcome to RetireGPT!")
st.write("Tell us about your career so we can build your AI-powered retirement strategy.")
st.markdown("""
You can:
- 🗂️ **Drag & drop your PDF resume**
- 📋 **Paste your biography**
- 💼 **Tell us about your current job** in the box below
""")

# 📁 Resume Upload or Text Input
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
user_input = st.text_area(
    "Or describe your job/paste your bio here:",
    placeholder="Example: I've worked as a marketing manager for 15 years, leading teams, managing ad campaigns, and analyzing market trends..."
)

# 📄 Extract text from uploaded PDF
resume_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = "\n".join(
                page.extract_text() for page in pdf_reader.pages if page.extract_text()
            )
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")
    else:
        st.error("❌ Please upload a valid PDF file.")

# 🧾 Final user input for AI prompt
final_prompt = resume_text.strip() if resume_text else user_input.strip()

# 💳 Passive Income Cards Display Function
def show_passive_income_cards():
    st.markdown("## 💸 AI-Powered Passive Income Ideas (Visual Summary)")

    income_ideas = [
        {
            "title": "YouTube Automation",
            "desc": "Create faceless, AI-generated video channels.",
            "image": "https://cdn-icons-png.flaticon.com/512/1384/1384060.png",
            "link": "https://pictory.ai"
        },
        {
            "title": "AI Course Creation",
            "desc": "Use ChatGPT + Canva to create sellable online courses.",
            "image": "https://cdn-icons-png.flaticon.com/512/4325/4325931.png",
            "link": "https://teachable.com"
        },
        {
            "title": "Newsletter Automation",
            "desc": "Use AI to summarize news and grow a Substack following.",
            "image": "https://cdn-icons-png.flaticon.com/512/5968/5968899.png",
            "link": "https://substack.com"
        },
        {
            "title": "Digital Products",
            "desc": "Generate eBooks, templates, or prompts with AI.",
            "image": "https://cdn-icons-png.flaticon.com/512/2784/2784482.png",
            "link": "https://gumroad.com"
        },
    ]

    cols = st.columns(2)
    for i, idea in enumerate(income_ideas):
        with cols[i % 2]:
            card(
                title=idea["title"],
                text=idea["desc"],
                image=idea["image"],
                url=idea["link"]
            )

# 🚀 Process input and generate strategy
if final_prompt:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """You are now acting as RetireGPT — an expert AI career strategist and retirement income advisor.

Your mission is to help professionals (typically age 40+) use AI to:
Enhance their current job using AI tools
Build realistic, AI-powered passive income streams
Follow a clear 3–6 month action plan

When given a resume or career summary, perform the following:

Part 1: Job Enhancement
Identify 3–5 ways AI can assist in the user’s current role
Recommend specific AI tools and describe their benefits
Match the user’s skills to tools that automate or enhance them

Part 2: Passive Income Strategy
Recommend 5 AI-powered passive income ideas aligned to the user’s background
For each, include:
A short explanation
Suggested tools or platforms
Beginner-level monthly income estimates (only include higher tiers if the keyword “unlock” is used)

Part 3: Demonstration Summary
Summarize the above as a demo-ready overview of how this plan creates perpetual AI-powered income for retirement
Make it clear, motivational, and structured for slides or speaking

Use plain English. Be concise but specific. Wait for a resume, job summary, or background details before responding."""
            },
            {"role": "user", "content": final_prompt}
        ]
    else:
        st.session_state.messages.append({"role": "user", "content": final_prompt})

    # 🧠 Show input back to user
    st.subheader("📄 Analyzing your background...")
    st.markdown(final_prompt)

    # 🤖 Generate AI Response
    with st.spinner("RetireGPT is crafting your personalized strategy..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

    # ✅ Display response
    st.success("✅ Strategy Ready!")
    st.markdown(reply, unsafe_allow_html=True)

    # 💳 Show passive income ideas visually
    show_passive_income_cards()

    # 💾 Save assistant's reply
    st.session_state.messages.append({"role": "assistant", "content": reply})