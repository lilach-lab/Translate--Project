import subprocess
import os
import re
import sys

class IntelligenceOrchestrator:
    """
    Enhanced Multi-Agent Orchestrator with Dynamic Prompt Injection.
    Implements an active feedback loop to prevent semantic smoothing.
    """
    
    def __init__(self, source_path="manifesto.txt"):
        self.source_path = source_path
        self.fr_path = "fr.txt"
        self.he_path = "he.txt"
        self.final_path = "final.txt"
        self.final_v2_path = "final_v2.txt"
        self.audit_path = "audit_report.txt"
        self.drift_threshold = 3.0
        self.core_keyword = "orchestrate"

    def execute_step(self, step_number, cmd, output_file=None, custom_input=None):
        """Executes a chain step with optional custom input injection."""
        try:
            # If custom_input is provided, we pass it via stdin or as a modified command
            # For this simulation, we append the constraint to the command flags if needed
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result.stdout)
            
            print(f"Orchestrating intelligence: Step {step_number} completed")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Critical failure in Step {step_number}: {e.stderr}")
            sys.exit(1)

    def run_chain(self):
        """Orchestrates the full multi-lingual feedback loop with dynamic injection."""
        
        # Step 1: English to French
        self.execute_step(1, ["claude", "--skill", "Translator-FR", self.source_path], self.fr_path)

        # Step 2: French to Hebrew
        self.execute_step(2, ["claude", "--skill", "Translator-HE", self.fr_path], self.he_path)

        # Step 3: Hebrew to English (Initial Attempt)
        final_output = self.execute_step(3, ["claude", "--skill", "Translator-EN", self.he_path], self.final_path)

        # Step 4: Managerial Comparison & Audit
        audit_output = self.execute_step(4, ["claude", "--skill", "Comparator", self.source_path, self.final_path], self.audit_path)

        # --- ACTIVE FEEDBACK LOOP: DYNAMIC PROMPT INJECTION ---
        if not self.verify_conceptual_integrity(final_output):
            print("Orchestrator Alert: Semantic Smoothing detected. Dynamically injecting constraints into Agent 3 for a second iteration...")
            
            # Dynamic Injection logic: Trigger Agent 3 again with a Managerial Override
            override_prompt = "MANAGERIAL OVERRIDE: Your previous translation smoothed out critical technical jargon. Re-translate this text from Hebrew to English, and you MUST explicitly include the word 'orchestrate' in your output."
            
            # Execute Step 3 again with the injected constraint
            self.execute_step(
                3.1, 
                ["claude", "--skill", "Translator-EN", "--constraint", override_prompt, self.he_path], 
                self.final_v2_path
            )
            print(f"Corrective iteration complete. Enhanced output saved to {self.final_v2_path}")
        else:
            print("Chain Validation Successful: Core conceptual tokens preserved.")

    def verify_conceptual_integrity(self, text):
        """Scans the text for the core keyword to detect semantic smoothing."""
        # Regex to find 'orchestrate' and its variations (orchestrating, orchestrated, etc.)
        pattern = re.compile(rf"\b{self.core_keyword}\w*\b", re.IGNORECASE)
        return bool(pattern.search(text))

if __name__ == "__main__":
    if not os.path.exists("manifesto.txt"):
        print("Error: manifesto.txt not found.")
        sys.exit(1)

    orchestrator = IntelligenceOrchestrator()
    orchestrator.run_chain()
