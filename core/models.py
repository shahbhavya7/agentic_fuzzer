from pydantic import BaseModel, Field

class TestCase(BaseModel):
    reasoning: str = Field(..., description="Explanation of why this test case is being tried.")
    input_data: str = Field(..., description="The actual raw string input to feed into the code.")

class ProfileResult(BaseModel):
    reasoning: str = Field(..., description="Explanation for the estimated time limit.")
    estimated_time_limit: float = Field(..., description="Estimated strict time limit in seconds.")

class PatchResult(BaseModel):
    reasoning: str = Field(..., description="Explanation of the fix.")
    patched_code: str = Field(..., description="The fully corrected and optimized code.")
