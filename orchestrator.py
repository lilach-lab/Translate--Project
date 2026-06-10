import subprocess
import os
import re
import sys

class IntelligenceOrchestrator:
    """
    Manages a multi-agent translation chain to ensure conceptual integrity 
    across linguistic boundaries.
    """
    
    def __init__(self, source_path="manifesto.txt"):
        self.source_path = source_path
        self.fr_path = "fr.txt"
        self.he_path = "he.txt"
        self.final_path = "final.txt"
        self.audit_path = "audit_report.txt"
        self.drift_threshold = 3.0

    def execute_step(self, step_number, cmd, output_file=None):
        """Executes a chain step and logs completion in managerial tone."""
        try:
            # Capture output for the audit/file saving
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
        """Orchestrates the full multi-lingual feedback loop."""
        
        # Step 1: English to French
        self.execute_step(1, ["claude", "--skill", "Translator-FR", self.source_path], self.fr_path)

        # Step 2: French to Hebrew
        self.execute_step(2, ["claude", "--skill", "Translator-HE", self.fr_path], self.he_path)

        # Step 3: Hebrew to English (Final)
        self.execute_step(3, ["claude", "--skill", "Translator-EN", self.he_path], self.final_path)

        # Step 4: Managerial Comparison & Audit
        audit_output = self.execute_step(4, ["claude", "--skill", "Comparator", self.source_path, self.final_path], self.audit_path)

        # Feedback Loop: Analyze Semantic Drift
        self.evaluate_semantic_integrity(audit_output)

    def evaluate_semantic_integrity(self, audit_text):
        """Parses the audit report to detect drift based on the threshold."""
        # Extracts numeric score (e.g., "Score: 0.5" or "0.5")
        match = re.search(r"(\d+(?:\.\d+)?)", audit_text)
        if match:
            score = float(match.group(1))
            if score > self.drift_threshold:
                print(f"WARNING: Semantic Drift detected (Score: {score}). Manual intervention required.")
            else:
                print(f"Chain Validation Successful: Semantic drift ({score}) is within acceptable managerial tolerances.")
        else:
            print("Error: Could not parse semantic score from audit report.")

if __name__ == "__main__":
    # Ensure source exists before starting the orchestration
    if not os.path.exists("manifesto.txt"):
        print("Error: manifesto.txt not found. Orchestration aborted.")
        sys.exit(1)

    orchestrator = IntelligenceOrchestrator()
    orchestrator.run_chain()
