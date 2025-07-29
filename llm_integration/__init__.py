"""
LLM Integration Package for Serviplagas Reporting System

This package provides LLM integration capabilities including:
- Prompt generation from data tables
- Configurable YAML-based prompt templates
- Integration with report generation workflow
"""

from .prompt_generator import LLMPromptGenerator, print_prompt_with_separator

__version__ = "1.0.0"
__all__ = [
    "LLMPromptGenerator",
    "print_prompt_with_separator"
]