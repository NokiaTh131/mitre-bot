from langchain.tools import tool
from mitreattack.stix20 import MitreAttackData
from pydantic import BaseModel, Field

class MitreIdentitySchema(BaseModel):
    technique_stix_id: str = Field(description="The STIX ID of the MITRE technique, e.g., 'attack-pattern--dcaa092b...'")

class MitreIncidentTool:
    def __init__(self, stix_path: str = "enterprise-attack.json"):
        self.mitre_data = MitreAttackData(stix_path)

    @tool("get_mitre_incident_context", args_schema=MitreIdentitySchema)
    def get_context(self, technique_stix_id: str) -> dict:
        """
        Retrieves a minimalist context bundle for a MITRE technique. 
        Focuses on description, specific mitigations, and detection sources for incident analysis.
        """
        try:
            tech = self.mitre_data.get_object_by_stix_id(technique_stix_id)
            
            mit_res = self.mitre_data.get_mitigations_mitigating_technique(technique_stix_id)
            det_res = self.mitre_data.get_datacomponents_detecting_technique(technique_stix_id)

            return {
                "technique_name": tech.name,
                "summary": tech.description,
                "remediation_steps": [
                    {
                        "strategy": m['object'].name,
                        "specific_action": m['relationships'][0].description if m['relationships'] else "No specific action provided."
                    } for m in mit_res
                ],
                "detection_visibility": [
                    {"component": d['object'].name} for d in det_res
                ]
            }
        except Exception as e:
            return {"error": f"Could not retrieve MITRE data: {str(e)}"}