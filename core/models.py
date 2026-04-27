from pydantic import BaseModel, Field

class TestCase(BaseModel):
    reasoning: str = Field(..., description="Explanation of why this test case is being tried.")
    input_data: str = Field(..., description="The actual raw string input to feed into the code.")
