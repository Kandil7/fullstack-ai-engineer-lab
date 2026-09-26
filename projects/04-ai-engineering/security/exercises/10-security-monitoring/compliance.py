"""
10 Security Monitoring: Compliance
"""

from ._types import *
from .incident_response import Incident


class ComplianceFramework(Enum):
    SOC2 = "soc2"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    ISO27001 = "iso27001"
    PCI_DSS = "pci_dss"


@dataclass
class ComplianceControl:
    """A compliance control."""

    control_id: str
    framework: ComplianceFramework
    title: str
    description: str
    category: str
    required: bool = True


@dataclass
class ComplianceAssessment:
    """Assessment result for a control."""

    control_id: str
    status: str  # compliant, non_compliant, partial, not_applicable
    evidence: List[str]
    findings: List[str]
    assessed_at: float
    assessed_by: str


class ComplianceAuditor:
    """
    Compliance auditing system.

    Features:
    - Control library management
    - Assessment tracking
    - Evidence collection
    - Gap analysis
    - Reporting
    """

    def __init__(self):
        self._controls: Dict[str, ComplianceControl] = {}
        self._assessments: Dict[str, List[ComplianceAssessment]] = defaultdict(list)
        self._setup_ai_security_controls()

    def _setup_ai_security_controls(self):
        """Setup AI security compliance controls."""
        ai_controls = [
            ComplianceControl(
                control_id="AI-001",
                framework=ComplianceFramework.SOC2,
                title="Model Access Control",
                description="Implement role-based access control for AI model access",
                category="access_control",
            ),
            ComplianceControl(
                control_id="AI-002",
                framework=ComplianceFramework.SOC2,
                title="Training Data Protection",
                description="Encrypt and protect training data at rest and in transit",
                category="data_protection",
            ),
            ComplianceControl(
                control_id="AI-003",
                framework=ComplianceFramework.SOC2,
                title="Model Audit Logging",
                description="Log all model access and inference requests",
                category="monitoring",
            ),
            ComplianceControl(
                control_id="AI-004",
                framework=ComplianceFramework.GDPR,
                title="Right to Explanation",
                description="Provide explanations for AI decisions affecting individuals",
                category="transparency",
            ),
            ComplianceControl(
                control_id="AI-005",
                framework=ComplianceFramework.GDPR,
                title="Data Minimization",
                description="Collect only necessary data for AI model training",
                category="data_protection",
            ),
            ComplianceControl(
                control_id="AI-006",
                framework=ComplianceFramework.SOC2,
                title="Incident Response",
                description="Maintain incident response plan for AI security events",
                category="incident_response",
            ),
            ComplianceControl(
                control_id="AI-007",
                framework=ComplianceFramework.ISO27001,
                title="Risk Assessment",
                description="Conduct regular risk assessments for AI systems",
                category="risk_management",
            ),
            ComplianceControl(
                control_id="AI-008",
                framework=ComplianceFramework.SOC2,
                title="Vendor Management",
                description="Assess security of AI service providers",
                category="third_party",
            ),
        ]

        for control in ai_controls:
            self._controls[control.control_id] = control

    def add_control(self, control: ComplianceControl):
        """Add a compliance control."""
        self._controls[control.control_id] = control

    def assess_control(
        self,
        control_id: str,
        status: str,
        evidence: List[str],
        findings: List[str],
        assessed_by: str,
    ) -> ComplianceAssessment:
        """Assess a compliance control."""
        assessment = ComplianceAssessment(
            control_id=control_id,
            status=status,
            evidence=evidence,
            findings=findings,
            assessed_at=time.time(),
            assessed_by=assessed_by,
        )

        self._assessments[control_id].append(assessment)
        return assessment

    def get_compliance_status(
        self,
        framework: Optional[ComplianceFramework] = None,
    ) -> Dict:
        """Get compliance status for a framework."""
        controls = self._controls.values()
        if framework:
            controls = [c for c in controls if c.framework == framework]

        results = {
            "total_controls": 0,
            "compliant": 0,
            "non_compliant": 0,
            "partial": 0,
            "not_assessed": 0,
            "compliance_score": 0,
            "control_details": [],
        }

        for control in controls:
            results["total_controls"] += 1
            assessments = self._assessments.get(control.control_id, [])

            if not assessments:
                results["not_assessed"] += 1
                status = "not_assessed"
            else:
                latest = assessments[-1]
                status = latest.status
                if status == "compliant":
                    results["compliant"] += 1
                elif status == "non_compliant":
                    results["non_compliant"] += 1
                elif status == "partial":
                    results["partial"] += 1

            results["control_details"].append(
                {
                    "control_id": control.control_id,
                    "title": control.title,
                    "framework": control.framework.value,
                    "status": status,
                }
            )

        # Calculate compliance score
        assessed = results["total_controls"] - results["not_assessed"]
        if assessed > 0:
            results["compliance_score"] = (results["compliant"] / assessed) * 100

        return results

    def generate_gap_analysis(self, framework: ComplianceFramework) -> Dict:
        """Generate gap analysis for a framework."""
        controls = [c for c in self._controls.values() if c.framework == framework]
        gaps = []

        for control in controls:
            assessments = self._assessments.get(control.control_id, [])
            if not assessments:
                gaps.append(
                    {
                        "control_id": control.control_id,
                        "title": control.title,
                        "gap_type": "not_assessed",
                        "recommendation": f"Conduct assessment for {control.title}",
                    }
                )
            elif assessments[-1].status == "non_compliant":
                gaps.append(
                    {
                        "control_id": control.control_id,
                        "title": control.title,
                        "gap_type": "non_compliant",
                        "findings": assessments[-1].findings,
                        "recommendation": f"Remediate: {control.title}",
                    }
                )

        return {
            "framework": framework.value,
            "total_controls": len(controls),
            "gaps_found": len(gaps),
            "gaps": gaps,
            "compliance_score": ((len(controls) - len(gaps)) / len(controls) * 100)
            if controls
            else 0,
        }


# =============================================================
# DEMONSTRATIONS
# =============================================================
