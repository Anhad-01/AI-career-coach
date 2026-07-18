'''
Agent Orchestrator
Responsible for managing the execution of AI Agents
'''

from typing import List, Dict
from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory
from models.agent_response import AgentResponse

class AgentOrchestrator:
    '''
    Executes AI agents in sequence
    '''

    MAX_RETRIES = 3

    def __init__(self, memory: SharedMemory, conversation_memory):
        self.memory = memory
        self.agents: List[BaseAgent] = []
        self.conversation_memory = conversation_memory
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        '''
        Register an AI agent.
        Args:
            agent: Agent to register
        '''

        # self.agents.append(agent)
        self._agents[
            agent.get_agent_name().lower()
        ] = agent

    # def execute(self):
    #     print("\nStarting Multi-Agent Workflow...\n")
    #     for agent in self.agents:
    #         print(f"Executing {agent.get_agent_name()} Agent...")
    #         response = agent.execute()
    #         print(f"{response.agent_name} completed successfully...")

    #     print("\nWorkflow completed.")
    #     return self.memory.get("reviewer")

    def execute(self, workflow: List[str]) -> AgentResponse:
        '''
        Execute the selected workflow
        Args: 
            workflow: Ordered list of agent names
        Returns: Final AgentResponse
        '''

        print("\nStarting Multi-Agent Workflow...\n")

        final_response = None
        for step, agent_name in enumerate(workflow, start=1):
            agent = self._agents.get(agent_name.lower())
            if agent is None:
                raise ValueError(f"Agent {agent_name} is not registered")
            
            print(f"\nStep {step}: Executing {agent.get_agent_name()} Agent...")

            # final_response = agent.execute()
            final_response = self._execute_with_retry(agent)
            print(f"{agent.get_agent_name()} completed successfully...")

        print("\nWorkflow completed.")
        return final_response
    
    def _execute_with_retry(self, agent: BaseAgent) -> AgentResponse:
        '''
        Execute an AI agent with retry mechanism
        Args:
            agent: AI Agent Instance
        Returns: 
            AgentResponse
        '''

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"Attempt: {attempt}")
                response = agent.execute()
                print("Success")
                return response
            except Exception as ex:
                print(f"Attempt {attempt} failed...")
                print(ex)

                if attempt == self.MAX_RETRIES:
                    raise RuntimeError(
                        f"{agent.get_agent_name()} failed after {self.MAX_RETRIES} attempts"
                    )
                
                print ("Retrying...")
