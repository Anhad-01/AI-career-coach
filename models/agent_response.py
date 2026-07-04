'''
Agent Response Model
Represents the standardized response returned by every AI Agent.
'''

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class AgentResponse:
    '''
    Standard response returned by every AI Agent
    '''
    agent_name: str # name of the agent
    output: str #AI generated output
    status: str #execution status of agent
    error: Optional[str] = None #error message (if any)
    timestamp: datetime = field(default_factory=datetime.now) #response generation time

    def is_success(self) -> bool:
        '''
        Return True if execution was successful
        '''
        return self.status.upper() == "SUCCESS"

    def __str__(self):
        '''
        Pretty string representation
        '''
        return (
            f"\nAgent : {self.agent_name}"
            f"\nStatus : {self.status}"
            f"\nTimestamp : {self.timestamp}"
            f"\nOutput : {self.output}"
        )