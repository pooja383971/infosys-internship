# import re

# class ReportBuilder:
#     def __init__(self):
#         pass

#     def _strip_non_ascii(self, text):
#         return text.encode("ascii", "ignore").decode()

#     def build_summary(self, domain, results):
#         sections = []

#         sections.append(f"Domain: {domain}")

#         for agent, content in results.items():
#             sections.append(f"\n=== {agent} Findings ===\n{content}")

#         summary_text = "\n".join(sections)
#         return self._strip_non_ascii(summary_text)

#     def to_json(self, domain, results):
#         return {
#             "domain": domain,
#             "results": results
#         }

def build_report(contract_text, analysis_result):
    return {
        "title": "Contract Analysis Report",
        "contract_text": contract_text,
        "analysis": analysis_result
    }
