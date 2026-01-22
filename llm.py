"""
LLM integration module using LangChain.

Provides utilities for AI-powered generation, specifically for
creating project-structure.md files.
"""

import os
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_llm(provider: str = "openai", model: Optional[str] = None):
    """
    Get an LLM instance based on the provider.
    
    Args:
        provider: 'openai' or 'anthropic'
        model: Specific model name (optional)
        
    Returns:
        LLM instance or None if API key not found
    """
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model or "gpt-4o-mini",
            api_key=api_key,
            temperature=0.7,
        )
    
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model or "claude-3-5-sonnet-20241022",
            api_key=api_key,
            temperature=0.7,
        )
    
    return None


def create_prompt_chain(llm, prompt_template: str):
    """
    Creates a simple prompt chain with string output.
    
    Args:
        llm: LangChain LLM instance
        prompt_template: Template string with {variables}
        
    Returns:
        Runnable chain
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    return prompt | llm | StrOutputParser()


PROJECT_STRUCTURE_PROMPT = """You are an expert at documenting software projects. Generate a comprehensive project-structure.md file for a Cursor Rules configuration.

Project Details:
- Project Name: {project_name}
- Tech Stack: {tech_stack}
- Main Files/Directories: {main_files}
- Architecture Notes: {architecture_notes}

Generate a well-structured markdown document that includes:
1. YAML frontmatter with description, globs: [], and alwaysApply: true
2. Clear overview of the project
3. Directory layout in tree format
4. Architecture explanation
5. Key technologies section
6. Running instructions
7. Environment variables (if applicable)

The output should be a complete, ready-to-use project-structure.md file.
Use proper markdown formatting with headers, code blocks, and lists.

Output ONLY the markdown content, no explanations before or after."""


async def generate_project_structure(
    project_name: str,
    tech_stack: str,
    main_files: str,
    architecture_notes: str,
    provider: str = "openai",
) -> Optional[str]:
    """
    Generate a project-structure.md file using AI.
    
    Args:
        project_name: Name of the project
        tech_stack: Comma-separated list of technologies
        main_files: Description of main files/directories
        architecture_notes: Notes about the architecture
        provider: LLM provider ('openai' or 'anthropic')
        
    Returns:
        Generated markdown content or None if LLM unavailable
    """
    llm = get_llm(provider)
    if not llm:
        return None
    
    chain = create_prompt_chain(llm, PROJECT_STRUCTURE_PROMPT)
    
    result = await chain.ainvoke({
        "project_name": project_name,
        "tech_stack": tech_stack,
        "main_files": main_files,
        "architecture_notes": architecture_notes,
    })
    
    return result


def generate_project_structure_sync(
    project_name: str,
    tech_stack: str,
    main_files: str,
    architecture_notes: str,
    provider: str = "openai",
) -> Optional[str]:
    """
    Synchronous version of generate_project_structure.
    
    Args:
        project_name: Name of the project
        tech_stack: Comma-separated list of technologies
        main_files: Description of main files/directories
        architecture_notes: Notes about the architecture
        provider: LLM provider ('openai' or 'anthropic')
        
    Returns:
        Generated markdown content or None if LLM unavailable
    """
    llm = get_llm(provider)
    if not llm:
        return None
    
    chain = create_prompt_chain(llm, PROJECT_STRUCTURE_PROMPT)
    
    result = chain.invoke({
        "project_name": project_name,
        "tech_stack": tech_stack,
        "main_files": main_files,
        "architecture_notes": architecture_notes,
    })
    
    return result


def check_api_keys() -> dict:
    """
    Check which API keys are configured.
    
    Returns:
        Dict with 'openai' and 'anthropic' keys indicating availability
    """
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
    }
