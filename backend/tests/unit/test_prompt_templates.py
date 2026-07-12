"""
🧪 Unit tests for PromptTemplate rendering and predefined templates.
"""

import unittest
from app.rag.prompt_templates import PromptTemplate


class TestPromptTemplateRendering(unittest.TestCase):
    """Test template rendering with variable injection."""

    def test_qa_template_rendering(self):
        prompt = PromptTemplate.build_qa_prompt(
            question="What is the revenue?",
            context_chunks=["Revenue was $10M in 2026.", "Expenses were $5M."]
        )

        self.assertIn("What is the revenue?", prompt)
        self.assertIn("Revenue was $10M in 2026.", prompt)
        self.assertIn("Expenses were $5M.", prompt)
        self.assertIn("---", prompt)  # Separator between chunks

    def test_summary_template_rendering(self):
        prompt = PromptTemplate.build_summary_prompt(
            context_chunks=["Chapter 1: Introduction.", "Chapter 2: Findings."]
        )

        self.assertIn("Chapter 1: Introduction.", prompt)
        self.assertIn("Chapter 2: Findings.", prompt)
        self.assertIn("Summary:", prompt)
        self.assertIn("summarizer", prompt.lower())

    def test_chat_template_with_history(self):
        history = [
            {"role": "user", "content": "What is the revenue?"},
            {"role": "assistant", "content": "Revenue was $10M."},
        ]

        prompt = PromptTemplate.build_chat_prompt(
            question="How about expenses?",
            context_chunks=["Expenses totaled $5M."],
            history=history
        )

        self.assertIn("How about expenses?", prompt)
        self.assertIn("Expenses totaled $5M.", prompt)
        self.assertIn("User: What is the revenue?", prompt)
        self.assertIn("Assistant: Revenue was $10M.", prompt)

    def test_chat_template_no_history(self):
        prompt = PromptTemplate.build_chat_prompt(
            question="Hello?",
            context_chunks=["Some context."],
            history=None
        )

        self.assertIn("Hello?", prompt)
        self.assertIn("(No previous conversation)", prompt)


class TestCustomTemplate(unittest.TestCase):
    """Test custom template rendering."""

    def test_custom_template(self):
        template = PromptTemplate(template="Q: {question}\nA:")
        rendered = template.render(question="What is AI?")
        self.assertEqual(rendered, "Q: What is AI?\nA:")

    def test_missing_variable_raises_error(self):
        template = PromptTemplate(template="Answer {question} with {context}")
        with self.assertRaises(ValueError) as ctx:
            template.render(question="What?")
        self.assertIn("context", str(ctx.exception))

    def test_empty_context_chunks(self):
        prompt = PromptTemplate.build_qa_prompt(
            question="Any question?",
            context_chunks=[]
        )
        self.assertIn("Any question?", prompt)
