'''
Gemini service
Responsible for communicating with the Gemini API

Resposibilities:
1. Initialize Gemini CLient
2. Send prompts to Gemini
3. Return the complete Gemini response
4. Keep API-specific code isloated from agents
'''

from google import genai
from typing import Any, Optional
from config import Config

class GeminiService:
    '''
    Wrapper around Google Gemini API
    '''

    def __init__(self):
        Config.validate() #validate configuration on initialization
        #Create Gemini client
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_response(self, prompt: str, config: Optional[Any]=None) -> Any:
        '''
        Send prompt to gemini and return reesponse
        Args:
            prompt: complete prompt to send
            config: optional configuration for the API call
        Returns:
            AI generated response
        '''

        try:
            response = self.client.models.generate_content(
                model = Config.MODEL_NAME,
                contents = prompt,
                config = config)
            return response
            
        except Exception as e:
            raise RuntimeError(
                f"Gemini API Error : {e}"
            )
