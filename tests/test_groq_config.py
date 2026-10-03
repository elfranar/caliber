import os
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from backend.config_groq import (
    DEFAULT_GROQ_MODEL,
    get_groq_api_key,
    get_groq_model,
    groq_processing_enabled,
)
from backend.case1_agent import answer_case1_query


class GroqConfigTests(unittest.TestCase):
    def test_groq_is_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(groq_processing_enabled())
            with self.assertRaisesRegex(RuntimeError, "processing is disabled"):
                get_groq_api_key()

    def test_groq_requires_key_after_consent(self):
        with patch.dict(
            os.environ,
            {"CALIBER_ALLOW_GROQ_PROCESSING": "true"},
            clear=True,
        ):
            self.assertTrue(groq_processing_enabled())
            with self.assertRaisesRegex(RuntimeError, "Set GROQ_API_KEY"):
                get_groq_api_key()

    def test_groq_key_is_trimmed_after_consent(self):
        with patch.dict(
            os.environ,
            {
                "CALIBER_ALLOW_GROQ_PROCESSING": " YES ",
                "GROQ_API_KEY": "  replacement-key  ",
            },
            clear=True,
        ):
            self.assertEqual(get_groq_api_key(), "replacement-key")

    def test_groq_model_uses_default_or_configured_model(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_groq_model(), DEFAULT_GROQ_MODEL)
        with patch.dict(os.environ, {"GROQ_MODEL": "  org-approved-model  "}, clear=True):
            self.assertEqual(get_groq_model(), "org-approved-model")

    def test_groq_model_rejects_empty_configuration(self):
        with patch.dict(os.environ, {"GROQ_MODEL": "  "}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GROQ_MODEL cannot be empty"):
                get_groq_model()

    def test_groq_key_is_not_returned_without_consent(self):
        with patch.dict(
            os.environ,
            {"GROQ_API_KEY": "replacement-key"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "processing is disabled"):
                get_groq_api_key()

    def test_approved_evidence_triggers_groq_generation(self):
        document = SimpleNamespace(
            page_content="Pump GA-1201A rated flow is 18 m3/h.",
            metadata={
                "doc_id": "datasheet-ga-1201a",
                "doc_name": "GA-1201A Datasheet",
                "version": "Rev 1",
                "section": "Hydraulic data",
                "dataset_id": "dataset_01",
                "approval_status": "approved",
                "approved_by": "test SME",
            },
        )
        vector_store = SimpleNamespace(
            similarity_search_with_score=lambda *args, **kwargs: [(document, 0.1)]
        )
        llm_calls = []

        class FakeChatGroq:
            def __init__(self, **kwargs):
                llm_calls.append(("init", kwargs))

            def invoke(self, prompt):
                llm_calls.append(("invoke", prompt))
                return SimpleNamespace(content="Mock grounded answer.")

        langchain_groq = ModuleType("langchain_groq")
        langchain_groq.ChatGroq = FakeChatGroq
        with (
            patch.dict(
                os.environ,
                {
                    "CALIBER_ALLOW_GROQ_PROCESSING": "true",
                    "GROQ_API_KEY": "test-key",
                },
                clear=True,
            ),
            patch.dict(sys.modules, {"langchain_groq": langchain_groq}),
            patch("backend.case1_agent._load_vector_store", return_value=vector_store),
            patch("backend.case1_agent._sync_vector_store"),
            patch("backend.case1_agent._search_maintenance", return_value=[]),
        ):
            result = answer_case1_query("What is the rated pump flow?")

        self.assertEqual(result["generation_mode"], "groq_grounded")
        self.assertEqual(result["answer"], "Mock grounded answer.")
        self.assertEqual([call[0] for call in llm_calls], ["init", "invoke"])
        self.assertEqual(llm_calls[0][1]["model"], DEFAULT_GROQ_MODEL)

    def test_no_approved_evidence_skips_groq_request(self):
        vector_store = SimpleNamespace(
            similarity_search_with_score=lambda *args, **kwargs: []
        )
        with (
            patch.dict(
                os.environ,
                {"CALIBER_ALLOW_GROQ_PROCESSING": "true"},
                clear=True,
            ),
            patch("backend.case1_agent._load_vector_store", return_value=vector_store),
            patch("backend.case1_agent._sync_vector_store"),
            patch("backend.case1_agent._search_maintenance", return_value=[]),
        ):
            result = answer_case1_query("What is the rated pump flow?")

        self.assertEqual(result["generation_mode"], "local_no_approved_evidence")


if __name__ == "__main__":
    unittest.main()
