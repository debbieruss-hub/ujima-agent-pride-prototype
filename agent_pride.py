"""
Ujima SACCO - Agent Pride Prototype
Simulates Scout, Guardian, Hunter agents.
Run: python agent_pride.py
"""

import sys

# ---------- Scout Agent ----------
class ScoutAgent:
    def __init__(self):
        self.sent_today = 0
        self.max_per_day = 3

    def process(self, message):
        self.sent_today += 1
        if self.sent_today > self.max_per_day:
            print("[Scout] Daily message limit reached, pausing.")
            return {"action": "pause"}

        # detect stress keywords
        if "school fee" in message.lower() or "no money" in message.lower():
            print("[Scout] Financial stress detected. Passing context to Guardian...")
            context = {
                "name": "Grace",
                "next_harvest": "2026-10-15",
                "savings_kes": 2000,
                "youngest_child": 14,
                "county": "Kakamega"
            }
            print("       Context:", context)
            return {"action": "handoff_guardian", "context": context}
        else:
            # generic tip
            print("[Scout] Sending literacy tip.")
            return {"action": "tip", "msg": "Panga bajeti yako kulingana na msimu wa mavuno."}

# ---------- Guardian Agent ----------
class GuardianAgent:
    # max auto-approve amount
    AUTO_LIMIT = 15000

    def screen(self, amount, context):
        print("\n[Guardian] Screening loan request...")
        flags = 0

        if amount > self.AUTO_LIMIT:
            flags += 1
            print("        Flag: amount above 15K")
        if context.get("youngest_child", 18) < 5:
            flags += 1
            print("        Flag: child under 5")
        if amount > context.get("savings_kes", 0) * 3:
            flags += 1
            print("        Flag: loan > 3x savings")

        if flags >= 3:
            print("        Denied (>=3 flags). Reason: hakuna akiba ya kutosha.")
            return {"decision": "deny"}
        elif amount <= self.AUTO_LIMIT and flags == 0:
            print("        Approved (<=15K, no flags).")
            return {"decision": "approve", "msg": f"Mkopo wa KES {amount} umepitishwa."}
        else:
            print("        Escalating to Hunter.")
            return {"decision": "escalate", "context": context, "flags": flags}

# ---------- Hunter Agent ----------
class HunterAgent:
    def prep_briefing(self, amount, ctx):
        print("\n[Hunter] Preparing briefing for human officer...")
        # match officer based on crop (hardcoded for now)
        if ctx.get("crop") == "maize":
            officer = "Sarah"
            specialty = "maize farmers"
        else:
            officer = "John"
            specialty = "general"

        print(f"        Assigned to: {officer} ({specialty})")
        briefing = {
            "officer": officer,
            "member": ctx["name"],
            "amount": amount,
            "harvest_peak": ctx["next_harvest"],
            "flags": ctx.get("flags", 0),
            "suggestion": "Cross-sell drought insurance" if officer == "Sarah" else ""
        }
        print("        Briefing:", briefing)
        return briefing

# ---------- GUARD rail ----------
def guard_check(amount, ctx):
    if amount > 50000 and ctx["youngest_child"] < 5:
        print("[GUARD] Blocked: >50K and child under 5. Needs human review.")
        return False
    return True

# ---------- PRIDE pause ----------
def human_review(brief):
    print("\n[PRIDE Pause] This application requires human approval.")
    print(f"Member: {brief['member']}, Amount: KES {brief['amount']}")
    decision = input("Human officer (approve/deny): ").strip().lower()
    if decision == "approve":
        print("        Human approved. Disbursing loan.")
        return "approved"
    else:
        print("        Human denied. Sending feedback.")
        return "denied"

# ---------- Main flow ----------
def main():
    print("=" * 50)
    print("Ujima SACCO - Agent Pride Prototype")
    print("=" * 50)

    scout = ScoutAgent()
    guardian = GuardianAgent()
    hunter = HunterAgent()

    # sample input
    msg = "No money for school fees, please help."
    amt = 28000

    print(f"\nMember SMS: \"{msg}\"")
    print(f"Requested amount: KES {amt}")

    # Scout
    res = scout.process(msg)
    if res["action"] != "handoff_guardian":
        print("No handoff triggered. Exiting.")
        return

    ctx = res["context"]
    ctx["crop"] = "maize"   # for officer matching

    # Guard rail check
    if not guard_check(amt, ctx):
        return

    # Guardian
    g_res = guardian.screen(amt, ctx)
    if g_res["decision"] == "deny":
        print("\nFinal: Denied.")
        return
    elif g_res["decision"] == "approve":
        print(f"\nFinal: Approved. {g_res['msg']}")
        return
    else:
        # Escalation to Hunter
        ctx["flags"] = g_res["flags"]
        briefing = hunter.prep_briefing(amt, ctx)
        final = human_review(briefing)
        print(f"\nFinal outcome: {final}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)