import openai
import json

class AddressValidator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
    
    def validate_and_format_address(self, address):
        """Validates an address"""
        
        validation_prompt = (
            "You are an address validation expert. "
            "Analyze the following text and: \n"
            "1. Identify if it contains a valid address (even if poorly structured)\n"
            "2. If you find a valid address, format it correctly\n"
            "3. If no valid address is found, explain why\n"
            "4. Consider non-conventional formats\n"
            "   like 'felipeyofre2794' which should be interpreted as 'Felipe Yofre 2794'\n"
            "5. Respond in JSON format:\n"
            "{\n"
            "  \"contains_address\": true/false,\n"
            "  \"formatted_address\": \"correctly formatted address\",\n"
            "  \"explanation\": \"detailed analysis\"\n"
            "}\n\n"
            f"Text to analyze: {address}\n"
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a specialized address validation assistant."
                    },
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            analysis = response.choices[0].message['content']
            
            try:
                result = json.loads(analysis)

                print(f"Analysis: {result.get('explanation', '')}")

                return result.get('formatted_address', False)
                
            except json.JSONDecodeError:
                return self._create_error_response('Error processing analysis response')
            
        except Exception as e:
            return self._create_error_response(f"Error processing address: {str(e)}")
    
    def _create_error_response(self, error_message):
        """Creates a standardized error response"""

        print(f"Error: {error_message}")
        return  False