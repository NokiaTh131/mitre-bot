# MITRE Bot

An intelligent Incident Analysis Agent that leverages the MITRE ATT&CK framework to analyze security incidents, identify techniques, and provide mitigation strategies using a multi-agent system.
```bash
[Incident Analysis Agent]
-----------------------
Input >> A user received an email with a PDF attachment. After opening it, the workstation spawned mshta.exe, which reached
out to an external domain and downloaded additional content.

[PROCESS LOG]
>> Pattern Analyst: Searching for 'user received an email with a PDF attachment that spawned mshta.exe'...
✓ Patterns retrieved
>> MITRE Specialist: Retrieving context for attack-pattern--a127c32c-cbb0-4f9d-be07-881a792408ec...
✓ MITRE context retrieved
>> MITRE Specialist: Retrieving context for attack-pattern--840a987a-99bd-4a80-a5c9-0cb2baa6cade...
✓ MITRE context retrieved

[INCIDENT ANALYSIS REPORT]

TECHNIQUE IDENTIFICATION
------------------------
* Name: Mshta
* ID: attack-pattern--840a987a-99bd-4a80-a5c9-0cb2baa6cade
* Summary: The incident involves the use of mshta.exe, a Windows utility for executing Microsoft HTML Applications (HTA).
Adversaries abuse mshta.exe to execute malicious scripts(e.g., VBScript or JavaScript) embedded in PDFs or downloaded
from external domains. This technique bypasses application whitelisting and browser security controls because mshta.exe
operates outside the Internet Explorer security context.

In this case:
* A PDF attachment triggered mshta.exe execution.
* The process communicated with an external domain to download additional payloads.

MITIGATION STRATEGIES
---------------------
1. Execution Prevention
   * Action: Configure Windows Defender Application Control (WDAC) to block execution of mshta.exe unless explicitly required.
   * Rationale: Prevents adversaries from leveraging mshta.exe to bypass security controls.

2. Disable or Remove Feature/Program
   * Action: Disable or remove mshta.exe if its functionality is not critical.
   * Rationale: Reducing attack surface lowers the risk of exploitation.

DETECTION OPPORTUNITIES
-----------------------
* Monitor Process Execution: Alert on unexpected execution of mshta.exe from non-trusted sources (PDFs, emails).
* Behavioral Analysis: Use EDR to detect unusual script execution (VBScript/JS) via mshta.exe.
* Network Traffic Analysis: Block or investigate outbound traffic from mshta.exe to unknown domains.
* Email and File Analysis: Scan PDF attachments for embedded scripts or use sandboxing before execution.

ANALYSIS & RESPONSE
-------------------
This incident aligns with the Mshta technique in MITRE ATT&CK. Key indicators:
1. Triggers: Execution via PDF attachment.
2. Communication: Outbound C2/payload delivery via external domain.
3. Bypass: Evasion of traditional browser security.

Recommended Response Actions:
1. Isolate the affected workstation.
2. Investigate the external domain for payload nature.
3. Update security controls (WDAC/Blocking).
4. Enhance monitoring (EDR/XDR deployment).
5. User Training on phishing risks.
```
## Features

- **Incident Analysis**: Analyzes natural language descriptions of security incidents.
- **MITRE Mapping**: Identifies relevant MITRE ATT&CK techniques (STIX IDs).
- **Expert Guidance**: Provides technical details, detection opportunities, and mitigation strategies.
- **Multi-Agent Architecture**:
  - **Incident Analysis Lead**: Orchestrates the investigation.
  - **Pattern Analyst**: Identifies ATT&CK techniques from descriptions.
  - **MITRE Specialist**: Retrieves deep technical context and defense strategies.

## Prerequisites

- Python 3.12+
- `uv` (recommended for dependency management) or `pip`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd mitre-bot
    ```

2.  **Install dependencies**:
    Using `uv`:
    ```bash
    uv sync
    ```
    Or using `pip`:
    ```bash
    pip install .
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add the following variables:
    ```env
    # Model to use and add prefix as providers
    # example MODEL=groq:openai/gpt-oss-20b
    MODEL=
    GEMINI_API_KEY=your_api_key_here
    YOUR_PROVIDER_API_KEY=your_api_key_here
    ```

## Usage

**Interactive Mode**:
Run the agent without arguments to enter the interactive prompt:
```bash
uv run -m main
```

## Project Structure

- `app/`: Source code for agents and tools.
  - `agents/`: Agent definitions and prompts.
  - `tools/`: Tools for retrieving MITRE data.
- `main.py`: Entry point for the application.
- `AGENTS.md`: Detailed agent personas and workflows.
- `attack-patterns.json` / `enterprise-attack.json`: MITRE ATT&CK dataset.
