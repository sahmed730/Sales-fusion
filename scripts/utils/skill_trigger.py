import os

class SkillTriggerEngine:
    """
    Simulates an automated skill-triggering mechanism.
    Based on the natural language task description, it maps to the appropriate Python script.
    """
    
    def __init__(self):
        self.skill_map = {
            "forecast revenue": "scripts/revenue_forecast.py",
            "predict demand": "scripts/demand_forecast.py",
            "find anomalies": "scripts/region_analysis.py",
            "customer retention": "scripts/cohort_analysis.py",
            "conversion drop-off": "scripts/funnel_analysis.py",
            "why did revenue drop": "scripts/root_cause_analysis.py",
            "audit data": "scripts/data_quality/audit_all.py"
        }
        
    def detect_and_run(self, user_prompt: str):
        print(f"Analyzing prompt: '{user_prompt}'")
        triggered = False
        
        for keyword, script in self.skill_map.items():
            if keyword in user_prompt.lower():
                print(f"✅ Skill Matched! Triggering: {script}")
                # os.system(f"python {script}") # Executing the script
                triggered = True
                
        if not triggered:
            print("❌ No specific skill matched. Defaulting to general EDA or requesting clarification.")

if __name__ == "__main__":
    engine = SkillTriggerEngine()
    # Example Triggers:
    engine.detect_and_run("Can you find anomalies in our regional sales?")
    engine.detect_and_run("Why did revenue drop last month?")
    engine.detect_and_run("Please audit data.")
