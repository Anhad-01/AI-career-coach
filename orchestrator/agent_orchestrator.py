'''
Agent Orchestrator
Responsible for managing the execution of AI Agents
'''

from typing import List
from agents.base_agent import BaseAgent
from memory.shared_memory import SharedMemory

class AgentOrchestrator:
    '''
    Executes AI agents in sequence
    '''

    def __init__(self, memory: SharedMemory):
        self.memory = memory
        self.agents: List[BaseAgent] = []

    def register(self, agent: BaseAgent) -> None:
        '''
        Regiser an AI agent.
        Args:
            agent: Agent to register
        '''

        self.agents.append(agent)

    def execute(self):
        print("\nStarting Multi-Agent Workflow...\n")
        for agent in self.agents:
            print(f"Executing {agent.get_agent_name()} Agent...")
            response = agent.execute()
            print(f"{response.agent_name} completed successfully...")

        print("\nWorkflow completed.")
        return self.memory.get("reviewer")
