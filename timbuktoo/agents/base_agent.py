"""Base agent class with cost tracking and guardrails"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import tiktoken
from anthropic import Anthropic
import os
from datetime import datetime

from ..database.models import CostTracking, SessionLocal
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all Timbuktoo agents"""

    def __init__(
        self,
        agent_type: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 38000,
        temperature: float = 0.7
    ):
        self.agent_type = agent_type
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=api_key)

        # Token counter
        self.encoding = tiktoken.encoding_for_model("gpt-4")

        # Cost tracking
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost = 0.0

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output"""
        pass

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))

    def call_llm(
        self,
        messages: list,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Call LLM with cost tracking"""

        if system_prompt is None:
            system_prompt = self.get_system_prompt()

        if max_tokens is None:
            max_tokens = self.max_tokens

        try:
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            )

            # Track usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            self.input_tokens += input_tokens
            self.output_tokens += output_tokens

            # Calculate cost (Claude Sonnet pricing)
            # $3 per million input tokens, $15 per million output tokens
            input_cost = (input_tokens / 1_000_000) * 3.0
            output_cost = (output_tokens / 1_000_000) * 15.0
            call_cost = input_cost + output_cost
            self.total_cost += call_cost

            logger.info(
                f"{self.agent_type} LLM call",
                extra={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": call_cost
                }
            )

            # Extract text response
            text_response = response.content[0].text if response.content else ""

            return {
                "response": text_response,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": call_cost
            }

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise

    def save_cost_tracking(self, trip_id: Optional[str] = None):
        """Save cost tracking to database"""
        if self.total_cost > 0:
            db = SessionLocal()
            try:
                cost_record = CostTracking(
                    trip_id=trip_id,
                    agent_type=self.agent_type,
                    model_used=self.model,
                    input_tokens=self.input_tokens,
                    output_tokens=self.output_tokens,
                    cost_usd=self.total_cost,
                    cached=False
                )
                db.add(cost_record)
                db.commit()
                logger.info(f"Cost tracking saved for {self.agent_type}")
            except Exception as e:
                logger.error(f"Failed to save cost tracking: {str(e)}")
                db.rollback()
            finally:
                db.close()

    def check_cost_limit(self, max_cost_usd: float = 0.80) -> bool:
        """Check if cost limit exceeded"""
        if self.total_cost >= max_cost_usd:
            logger.warning(
                f"Cost limit exceeded for {self.agent_type}",
                extra={"total_cost": self.total_cost, "limit": max_cost_usd}
            )
            return False
        return True

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        try:
            # Try to find JSON in response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: try parsing entire response
                return json.loads(response)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Response: {response}")
            raise ValueError(f"Invalid JSON response from {self.agent_type}")

    def validate_output(self, output: Dict[str, Any], required_fields: list) -> bool:
        """Validate output has required fields"""
        for field in required_fields:
            if field not in output:
                logger.error(f"Missing required field: {field}")
                return False
        return True
