'''
Workflow router

Uses Gemini to intelligently select the most appropriate workflow for user's request

Responsibilities:
1. Build the routing prompt
2. Retrieve available workflows from Registry
3. Ask Gemini to classify the request
4. Return Workflow Decision
'''

from services.gemini_service import GeminiService
from routing.workflow_registry import WorkflowRegistry
from models.workflow_decision import WorkflowDecision

from google.genai import types

class WorkflowRouter:
    '''
    LLM-powered workflow router
    Gemini analyzes the user's request and selects the most appropriate workflow
    '''

    def __init__(self, gemini_service: GeminiService,
                 workflow_registry: WorkflowRegistry) -> None:
        '''
        Initialize workflow router
        '''

        self.gemini = gemini_service
        self.registry = workflow_registry

    def route(self, user_query: str) -> WorkflowDecision:
        '''
        Route the user query
        Args:
            user_query
        Returns:
            WorkflowDecision
        '''
        prompt = self.build_prompt(user_query)
        response = self.gemini.generate_response(
            prompt=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=WorkflowDecision
            )
        )

        return response.parsed

    def build_prompt(self, user_query: str) -> str:
        '''
        Build the routing prompt
        Args: 
            user_query
        Returns:
            Prompt string
        '''

        workflow_details = []
        for workflow in self.registry.get_available_workflows():
            workflow_details.append(f"- {workflow}")

        available_workflows = "\n".join(workflow_details)
        '''
        roadmap: planner, researcher, writer, reviewer
        certification: researcher, writer
        project: researcher, writer
        review: reviewer
        '''

        prompt = f"""
        You are an enterprise AI workflow router.
        Your job is to determine which workflow should be executed.
        Available workflows:
        {available_workflows}

        Instructions:
        1. Select ONLY ONE workflow
        2. Return your answer using the provided schema.
        3. Do NOT explain anything.

        User Request:
        {user_query}
"""
        return prompt
        