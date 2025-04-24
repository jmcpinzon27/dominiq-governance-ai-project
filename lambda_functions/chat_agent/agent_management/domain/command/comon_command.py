from collections import namedtuple

Sources = namedtuple('Sources', [
    'sql', 'asistant', 'storage'
])
sql = namedtuple('sql', [
    "agent",
    "axis",
    "comon",
    "company",
    "domain_agent_response",
    "domain",
    "domain_question",
    "industry",
    "maturity_agent_response",
    "maturity_answer",
    "maturity_question",
    "project",
    "registration",
    "role",
    "session",
    "subdomain",
    "user"
], defaults=(None, )*17)
