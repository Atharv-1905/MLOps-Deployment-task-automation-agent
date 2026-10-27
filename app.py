
# Build a web application that searches the web and summarizes results.

import os
import time
import logging
import streamlit as st
from openai import OpenAI
from ddgs import DDGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Research Brief", page_icon="🔎")
st.title("AI Research Brief Generator")
st.write("Enter a topic to get a three-point research brief.")

def search_web(topic):
    # Search DuckDuckGo and collect useful results.
    with DDGS() as search:
        results = list(search.text(topic, max_results=5))

    if not results:
        raise ValueError("No search results found. Try another topic.")

    return "\n\n".join(
        f"Title: {r.get('title', '')}\n"
        f"URL: {r.get('href', '')}\n"
        f"Summary: {r.get('body', '')}"
        for r in results
    )

def summarize(topic, search_results):
    # Summarize the retrieved information using the Groq API.
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=[
            {
                "role": "system",
                "content": "You summarize web research accurately and concisely."
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the topic: {topic}\n"
                    "Use only the provided search results. Do not invent facts. "
                    "Return exactly three bullet points, with no introduction "
                    "or conclusion.\n\n"
                    f"Search results:\n{search_results}"
                )
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def research_brief(topic):
    # Run the search and summarization stages in sequence.
    start_time = time.time()
    logger.info("Request received for topic: %s", topic)

    try:
        st.info("Stage 1/2: Searching the web...")
        results = search_web(topic)

        st.info("Stage 2/2: Summarizing results...")
        brief = summarize(topic, results)

        logger.info("Request completed in %.2f seconds", time.time() - start_time)
        return brief

    except Exception:
        logger.exception("Research workflow failed")
        raise

topic = st.text_input("Enter your research topic")

if st.button("Generate Brief"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating your research brief..."):
                brief = research_brief(topic.strip())
            st.subheader("Your Research Brief")
            st.markdown(brief)
        except Exception as error:
            st.error(f"Something went wrong: {error}")
