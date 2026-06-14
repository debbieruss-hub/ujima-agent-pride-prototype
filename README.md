# Ujima SACCO – Agent Pride Prototype

A working demonstration of the Scout → Guardian → Hunter multi-agent system for ethical loan triage, built as part of the Pride Leader capstone.

## Overview

This prototype simulates three AI agents with strict boundaries (RANK), handoff triggers (HUNT), safety rails (GUARD), and a human-in-the-loop pause (PRIDE). It processes a member's SMS about school fees, screens the loan against harvest-cycle data, and escalates decisions that require a human loan officer.

## How to run

Requires Python 3.7+ (no additional packages).

```bash
python agent_pride.py
Type approve or deny when the PRIDE pause prompts you.

Technical note on CrewAI
The capstone option "CrewAI agent team running locally" was the target, but CrewAI 0.11.2 pins dependencies (langchain<0.2.0, instructor<0.6.0, numpy<2) that are incompatible with Python 3.14 and unavailable as pre-built wheels for Windows. To ensure the evaluator can run the prototype instantly with zero dependency friction, the exact same RANK/HUNT/GUARD/PRIDE architecture is implemented in native Python. Every constraint, handoff, and safety check is identical to what a CrewAI orchestration would perform.

Demo Video
https://drive.google.com/file/d/1BsPXTQyGYMu3zcN4MW2FYl0T_qoudpDm/view?usp=sharing

Repository structure
text
ujima-agent-pride-prototype/
├── agent_pride.py          # Native Python prototype (recommended)
├── agent_pride_crew.py     # CrewAI attempt (needs old dependencies, included for completeness)
└── README.md


Technical note on CrewAI
The capstone option "CrewAI agent team running locally" was the target, but CrewAI 0.11.2 pins dependencies (langchain<0.2.0, instructor<0.6.0, numpy<2) that are incompatible with Python 3.14 and unavailable as pre-built wheels for Windows. To ensure the evaluator can run the prototype instantly with zero dependency friction, the exact same RANK/HUNT/GUARD/PRIDE architecture is implemented in native Python. Every constraint, handoff, and safety check is identical to what a CrewAI orchestration would perform.
