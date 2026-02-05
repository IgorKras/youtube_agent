import logging
import json
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


logger = logging.getLogger(__name__)

class LangChainUtils:
    def __init__(self, api_base: str, model: str, temperature: float = 0.0):
        # Helper to ensure unique /v1 suffix
        base = api_base.rstrip('/')
        if not base.endswith('/v1'):
            base += '/v1'
            
        self.llm = ChatOpenAI(
            base_url=base,  # OpenAI compatible
            api_key="lm-studio",  # Dummy key for local LLM
            model=model,
            temperature=temperature
        )
        
        # Intent Classifier Chain
        self.intent_parser = JsonOutputParser()
        self.intent_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant for a YouTube Bot. Your job is to classify user messages into structured intents.
            
            Supported Actions:
            - ADD_CHANNEL: User wants to add a YouTube channel.
              - ARG: The channel name or URL.
            - REMOVE_CHANNEL: User wants to remove a YouTube channel.
              - ARG: The channel name.
            - LIST_CHANNELS: User wants to see the list of monitored channels.
            - RUN_REVIEW: User wants to run the review manually.
              * Examples: "check for new videos", "run review", "give me summary of latest videos", "what's new on my channels", "overview of videos", "summary of latest videos from each channel"
            - STATUS: User wants to check bot status.
            - HELP: User asks for help or greeting.
            - UNKNOWN: If the intent is unclear.

            Output JSON format:
            {{
                "action": "ACTION_NAME",
                "arg": "optional_argument"
            }}
            """),
            ("user", "{text}")
        ])
        self.intent_chain = self.intent_prompt | self.llm | self.intent_parser

        # Summarization Chain
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an assistant that summarizes YouTube video content.
            Write a concise summary in {language} using at most {max_sentences} sentences.
            
            IMPORTANT:
            - If the 'Transcript' is available, base your summary on it.
            - If the 'Transcript' is missing or "N/A", you MUST generate a summary based on the 'Title' and 'Description'.
            - Do NOT just say "Transcript is missing". Provide a summary of what the video is likely about based on available info.
            """),
            ("user", """
            Title: {title}
            Description: {description}
            Transcript: {transcript}
            
            Summary:""")
        ])
        self.summary_chain = self.summary_prompt | self.llm

    def classify_intent(self, text: str) -> Dict[str, Any]:
        try:
            result = self.intent_chain.invoke({"text": text})
            
            # Validate that result is a dict with expected structure
            if not isinstance(result, dict):
                logger.warning(f"Intent classifier returned non-dict: {type(result).__name__} = {result}")
                return {"action": "UNKNOWN"}
            
            if "action" not in result:
                logger.warning(f"Intent classifier returned dict without 'action' key: {result}")
                return {"action": "UNKNOWN", **result}
            
            return result
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return {"action": "UNKNOWN"}

    def generate_summary(self, title: str, description: str, transcript: str, max_sentences: int, language: str) -> str:
        try:
            response = self.summary_chain.invoke({
                "title": title,
                "description": description or "N/A",
                "transcript": transcript or "N/A",
                "max_sentences": max_sentences,
                "language": language
            })
            return response.content.strip()
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return "Error generating summary."
