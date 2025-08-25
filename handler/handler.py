import time
import logging
import re
import streamlit as st
from typing import Dict, Any, Optional
from config.logger_config import setup_logger
import json

setup_logger()
logger = logging.getLogger(__name__)

class AgentHandler:
    def __init__(self):
        logger.debug("Initializing StreamlitHandler")
        self.current_reasoning = ""
        self.current_tool_input = ""
        self.current_result = ""
        
    def __call__(self, **kwargs):
        #logger.info("----------------------------------------------------------")
        #logger.info(kwargs)
        #return 
        if "event" in kwargs.keys():
            event = kwargs.get("event", {})
            if event.get("contentBlockStop"):
                if self.current_tool_input:
                    logger.info(f"📥 Tool Input: {self.current_tool_input}")
                if self.current_result:
                    logger.info(f"📝  Text: {self.current_result}")
                self.current_tool_input = ""
                self.current_result = ""
            elif event.get("contentBlockDelta"):
                delta = event.get("contentBlockDelta", {}).get("delta",{})
                if delta.get("text"):
                    #logger.info(f"📝 Text: {delta.get('text')}")
                    self.current_result += delta.get("text")
                elif delta.get("toolUse"):
                    #logger.info(f"🔧 Tool Input: {delta.get('toolUse').get('input')}")
                    self.current_tool_input += delta.get("toolUse").get("input")
            elif event.get("contentBlockStart"):
                delta = event.get("contentBlockStart", {})
                toolUse = delta.get("start", {}).get("toolUse", {})
                if toolUse.get("name"):
                    logger.info(f"🔧 Using tool: {toolUse.get('name')}")
            elif event.get("metadata"):
                logger.info(json.dumps(event.get("metadata"), indent=2))
        elif "result" in kwargs.keys():
            logger.info(kwargs)

        # Track event loop lifecycle
        if kwargs.get("init_event_loop", False):
            logger.info("🔄 Event loop initialized")
        elif kwargs.get("start_event_loop", False):
            logger.info("▶️ Event loop cycle starting")
        elif kwargs.get("start", False):
            logger.info("📝 New cycle started")
        elif kwargs.get("complete", False):
            logger.info("✅ Cycle completed")
        elif kwargs.get("force_stop", False):
            logger.info(f"🛑 Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown reason')}")

        if "reasoningText" in kwargs: 
            reasoning_text = kwargs.get("reasoningText", "")
            if isinstance(reasoning_text, dict) and "text" in reasoning_text:
                reasoning_text = reasoning_text["text"]
            self.current_reasoning += str(reasoning_text)
            
        # When reasoning is complete, output the full reasoning
        elif "reasoning_signature" in kwargs: 
            if self.current_reasoning:
                logger.info(f"🤔 Reasoning complete: {self.current_reasoning}")
            self.current_reasoning = ""
        