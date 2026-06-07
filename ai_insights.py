import json
import os
from dotenv import load_dotenv

from openai import OpenAI

INSTRUCTIONS_PATH = "./instructions.md"
SCHEMA_PATH = "./schema.md"
MODEL = "gpt-4o-mini"

class AiInsights:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.tools = [
                    {
                        "type": "function",
                        "name": "run_sql",
                        "description": "Execute a read-only SQL query",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "sql": {
                                    "type": "string"
                                }
                            },
                            "required": ["sql"]
                        }
                    }
                ]
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_instructions(self) -> str:
        with open(INSTRUCTIONS_PATH, "r") as f:
            instructions = f.read()
        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()
        return instructions + f" {self.ticker} (case-sensitive)\n" + schema

    def get_insights(self):
        response = self.client.responses.create(
        model=MODEL,
        tools=self.tools,
        input=self.get_instructions()
        )
        return {"explanation": self.get_description_from_response(response), "sql": self.get_sql_from_response(response)}

    def get_sql_from_response(self, response) -> str:
        queries = self.get_queries_from_response(response)
        return queries[0].get("sql", "No SQL provided")

    def get_queries_from_response(self, response) -> dict:
        text = None
        if hasattr(response, "output_text") and response.output_text:
            text = response.output_text
        elif isinstance(response, dict):
            text = response.get("output", [{}])[0].get("content", [{}])[0].get("text")

        if not text:
            raise RuntimeError("No response text available from OpenAI response")

        cleaned = self._strip_code_fence(text)
        parsed = json.loads(cleaned)

        queries = parsed.get("queries")
        if not queries or not isinstance(queries, list):
            raise RuntimeError("Unexpected response JSON structure: 'queries' missing")

        return queries

    def get_description_from_response(self, response: list) -> str:
        queries = self.get_queries_from_response(response)
        return queries[0].get("explanation", "No explanation provided")

    def _strip_code_fence(self, text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```"):
            # remove opening fence line
            parts = stripped.split("\n", 1)
            if len(parts) == 2:
                stripped = parts[1]
        if stripped.endswith("```"):
            stripped = stripped[: -3].rstrip()
        return stripped

if __name__ == "__main__":
    ai_insights = AiInsights("amzn")
    ai_insights.get_insights()
