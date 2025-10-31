"""Hardcoded Soal Labs Full Stack Engineer interview template data."""

TEMPLATE = {
    "id": "soal-labs-full-stack-engineer",
    "title": "Soal Labs Full Stack Engineer Interview Framework (Punchy Edition)",
    "description": (
        "An unconventional, deeply human interview framework for evaluating full stack "
        "engineers across ethics, flexibility, professionalism, and depth."
    ),
    "tags": ["hiring", "interview", "framework", "full stack", "soal labs"],
    "phases": [
        {
            "id": "phase-1",
            "title": "CEO Behavioral / Values Interview",
            "format": "CEO Behavioral + Message Chain",
            "owner": "CEO",
            "focus": [
                "Values",
                "Ethics",
                "Flexibility",
                "Character",
            ],
            "what_it_tests": [
                "Ethical compass and maturity",
                "Low-ego collaboration",
                "Calm under ambiguity",
                "Real communication skill",
                "Personality (not persona)",
            ],
            "sections": [
                {
                    "title": "⚡️ Opening Questions",
                    "prompts": [
                        "If I ask your last boss what your flaws and bad habits are, what would they say?",
                        "Say that boss is really disrespectful and belittles you in front of other people — what do you do?",
                    ],
                },
                {
                    "title": "🧭 Ethics / Integrity",
                    "prompts": [
                        "You see a senior teammate taking credit for juniors’ work — what do you do?",
                    ],
                },
                {
                    "title": "🕰 Flexibility & Reliability",
                    "prompts": [
                        "You’re supposed to demo to the client tomorrow, and your code isn’t ready. Do you sleep 4 hours, delay, or fake it?",
                        "How do you know you’re giving enough without burning out?",
                    ],
                },
                {
                    "title": "🌱 Kindness & Low Ego",
                    "prompts": [
                        "What’s your instinct when someone’s just wrong in a code review?",
                        "Who’s the kindest person you’ve worked with — what made them kind?",
                    ],
                },
                {
                    "title": "🗣 Communication & Professionalism",
                    "prompts": [
                        "Write a one-sentence summary for a client who just wants to know: ‘Is it done yet?’",
                        "How would you explain an API rate limit to a CFO who doesn’t know what an API is?",
                        "If I read your Slack messages, would I think you’re an optimist or a pessimist?",
                    ],
                },
                {
                    "title": "💬 Live Message Chain Simulation (Slack-Style)",
                    "summary": "Tests tone, judgment, flexibility, and client maturity.",
                    "scenarios": [
                        {
                            "title": "Scenario 1 – Empathy, Boundaries, Clarifying",
                            "prompt": "Client: “Hey, I know it’s late, but I would love to make some changes to the UI we just released.”",
                        },
                        {
                            "title": "Scenario 2 – Tone under accusation",
                            "prompt": "Teammate: “Dude, your changes just broke my build again. DevOps team is swamped. What did you do?”",
                        },
                        {
                            "title": "Scenario 3 – Clarifying and reframing",
                            "prompt": "PM: “Can we just make the app ‘feel faster’ by Monday?”",
                        },
                    ],
                    "scoring": {
                        "trait_headers": ["Tone", "Judgment", "Clarity"],
                        "scale": {
                            "1": ["Defensive", "Rigid", "Rambling"],
                            "3": ["Polite", "Safe", "Adequate"],
                            "5": [
                                "Calm, respectful, concise",
                                "Client-aware, sets healthy boundaries",
                                "Decisive, direct, professional",
                            ],
                        },
                    },
                },
            ],
        },
        {
            "id": "phase-2",
            "title": "Async Mini-Test",
            "format": "Async",
            "owner": "Async",
            "focus": ["Code reasoning", "Clarity"],
            "prompt": (
                "Imagine Soal Labs is pitching a client. They want to see an AI tool that can summarize "
                "credit memos and surface key risks. They asked whether it could ‘talk to their existing systems’ "
                "and ‘understand private credit nuance.’ No further details provided. What would you build quickly as a demo, "
                "what would you fake, and what would you ignore? What would the suggested next steps be and what questions would you ask?"
            ),
            "instructions": "Max 200 words — clarity over detail.",
            "scoring": {
                "1": "Generic, no trade-offs",
                "3": "Technically fine, shallow reasoning",
                "5": "Sharp, self-aware, prioritizes impact & humans",
            },
        },
        {
            "id": "phase-3",
            "title": "Take-Home Design Doc",
            "format": "Async",
            "owner": "Async",
            "focus": ["Architecture", "Trade-offs", "Writing"],
            "prompt": (
                "Design a full-stack app for private credit funds — this app is for deal teams to manage the "
                "whole underwriting process. Deals / Securities / Due Diligence / IC Memo Generation."
            ),
            "requirements": [
                "Product Flow Diagrams",
                "Low-fidelity wireframes",
                "ERD",
                "Decisions: Infra (what’s hosted, what’s not), Auth, RBAC, Backend Server, Frontend Paradigm, Database choice",
                "Endpoints",
                "Section: ‘What I would not do and why.’",
                "Include how you’d handle analytics and caching.",
                "Do not write code.",
            ],
            "scoring": {
                "Clarity": {
                    "1": "Disorganized",
                    "3": "Understandable",
                    "5": "Crisp and visual",
                },
                "Technical depth": {
                    "1": "Surface-level",
                    "3": "Sound",
                    "5": "Thoughtful, cost-aware",
                },
                "Business awareness": {
                    "1": "Pure tech",
                    "3": "Generic MVP",
                    "5": "Client-savvy, phased",
                },
                "Writing": {
                    "1": "Messy",
                    "3": "Adequate",
                    "5": "Clear, narrative voice",
                },
            },
            "curveball": "Include how you’d handle analytics and caching.",
        },
        {
            "id": "phase-4",
            "title": "Super Day",
            "format": "CTO + Panel",
            "owner": "CTO + Panel",
            "focus": ["Technical", "Business", "Mentorship"],
            "segments": [
                {"title": "Design Review", "duration": "45 min", "focus": "Deep architecture discussion"},
                {"title": "Pair Programming", "duration": "60 min", "focus": "Code + communication"},
                {"title": "Business Interview", "duration": "30 min", "focus": "Consulting & context thinking"},
                {"title": "Mentorship Panel", "duration": "30 min", "focus": "Feedback quality & empathy"},
            ],
            "design_review": {
                "questions": [
                    "What’s something you know you overengineer sometimes?",
                    "If you had to delete 30% of your system, what would you delete?",
                    "Your app’s backend budget just got cut in half. What’s the first thing to simplify?",
                    "What’s your opinionated take on testing? Be honest.",
                    "How would you explain your architecture to a client who thinks everything should be in Excel?",
                ]
            },
            "pair_programming": {
                "exercise": "Build a simple notes app with one endpoint and one React component.",
                "bonus": ["Add basic validation", "Add one test"],
                "curveballs": [
                    "Now make it multi-user.",
                    "What if the API is 400ms slow — how do you handle it?",
                    "Client wants dark mode but budget’s gone. Your move?",
                ],
                "scoring": {
                    "Trait headers": ["Technical ability", "Collaboration", "Adaptability"],
                    "scale": {
                        "1": ["Fumbles", "Silent", "Rigid"],
                        "3": ["Competent", "Cooperative", "Adjusts"],
                        "5": ["Sharp, efficient", "Empathetic, verbalizes reasoning", "Smiles through chaos"],
                    },
                },
            },
            "business_interview": {
                "prompts": [
                    "A CFO wants to ‘modernize their stack.’ What question do you ask first?",
                    "If an investor presentation needs metrics tomorrow, what do you cut corners on — and what do you protect?",
                    "What’s something engineers overcomplicate for clients?",
                    "What’s something you’d never say to a client even if you believed it?",
                ]
            },
            "mentorship_panel": {
                "prompt": "Here’s a teammate’s PR with some weird naming and a missing null check. Review it out loud.",
                "follow_ups": [
                    "How do you start a hard code review comment?",
                    "What kind of feedback makes you defensive?",
                    "What advice would you give to your younger self about collaboration?",
                ],
            },
        },
        {
            "id": "phase-5",
            "title": "Paid Trial",
            "format": "Project Team",
            "owner": "Project Team",
            "focus": ["Real-world behavior"],
            "tasks": [
                "Build or extend a feature in your stack (small full-stack ticket)",
                "Async Slack communication, short daily update, short demo",
            ],
            "curveball": "Change a requirement midweek — see how they respond.",
            "scoring": {
                "Trait headers": ["Reliability", "Communication", "Ownership", "Craft"],
                "scale": {
                    "1": ["Misses updates", "Silent", "Blames others", "Sloppy"],
                    "3": ["Consistent", "Adequate", "Accountable", "Fine"],
                    "5": ["Proactive, anticipates", "Transparent, calm", "Sees gaps, patches them", "Production-ready, thoughtful"],
                },
            },
        },
    ],
    "steps": [
        {
            "id": "ceo-behavioral",
            "title": "CEO Behavioral / Values Interview",
            "order": 1,
            "summary": "Probe ethics, judgment, tone, and communication through behavioral prompts and live message simulations.",
            "prompts": {
                "what_it_tests": [
                    "Ethical compass and maturity",
                    "Low-ego collaboration",
                    "Calm under ambiguity",
                    "Real communication skill",
                    "Personality (not persona)",
                ],
                "opening_questions": [
                    "If I ask your last boss what your flaws and bad habits are, what would they say?",
                    "Say that boss is really disrespectful and belittles you in front of other people — what do you do?",
                ],
                "ethics": [
                    "You see a senior teammate taking credit for juniors’ work — what do you do?",
                ],
                "flexibility": [
                    "You’re supposed to demo to the client tomorrow, and your code isn’t ready. Do you sleep 4 hours, delay, or fake it?",
                    "How do you know you’re giving enough without burning out?",
                ],
                "kindness": [
                    "What’s your instinct when someone’s just wrong in a code review?",
                    "Who’s the kindest person you’ve worked with — what made them kind?",
                ],
                "communication": [
                    "Write a one-sentence summary for a client who just wants to know: ‘Is it done yet?’",
                    "How would you explain an API rate limit to a CFO who doesn’t know what an API is?",
                    "If I read your Slack messages, would I think you’re an optimist or a pessimist?",
                ],
                "message_chain": {
                    "scenario_1": {
                        "title": "Scenario 1 – Empathy, Boundaries, Clarifying",
                        "prompt": "Client: “Hey, I know it’s late, but I would love to make some changes to the UI we just released.”",
                    },
                    "scenario_2": {
                        "title": "Scenario 2 – Tone under accusation",
                        "prompt": "Teammate: “Dude, your changes just broke my build again. DevOps team is swamped. What did you do?”",
                    },
                    "scenario_3": {
                        "title": "Scenario 3 – Clarifying and reframing",
                        "prompt": "PM: “Can we just make the app ‘feel faster’ by Monday?”",
                    },
                },
            },
            "scoring_guidance": {
                "Tone": {"1": "Defensive", "3": "Polite", "5": "Calm, respectful, concise"},
                "Judgment": {
                    "1": "Rigid",
                    "3": "Safe",
                    "5": "Client-aware, sets healthy boundaries",
                },
                "Clarity": {
                    "1": "Rambling",
                    "3": "Adequate",
                    "5": "Decisive, direct, professional",
                },
            },
        },
        {
            "id": "async-mini-test",
            "title": "Async Mini-Test",
            "order": 2,
            "summary": "Short-form written response assessing clarity and prioritization under ambiguity.",
            "prompts": {
                "main": (
                    "Imagine Soal Labs is pitching a client. They want to see an AI tool that can summarize credit memos "
                    "and surface key risks. They asked whether it could ‘talk to their existing systems’ and ‘understand private credit nuance.’ "
                    "No further details provided. What would you build quickly as a demo, what would you fake, and what would you ignore? "
                    "What would the suggested next steps be and what questions would you ask?"
                ),
                "instructions": "Max 200 words — clarity over detail.",
            },
            "scoring_guidance": {
                "1": "Generic, no trade-offs",
                "3": "Technically fine, shallow reasoning",
                "5": "Sharp, self-aware, prioritizes impact & humans",
            },
        },
        {
            "id": "take-home-design-doc",
            "title": "Take-Home Design Doc",
            "order": 3,
            "summary": "Evaluate architecture rigor, communication, and decision making via a structured design deliverable.",
            "prompts": {
                "main": "Design a full-stack app for private credit funds — this app is for deal teams to manage the whole underwriting process. Deals / Securities / Due Diligence / IC Memo Generation.",
                "requirements": [
                    "Product Flow Diagrams",
                    "Low-fidelity wireframes",
                    "ERD",
                    "Decisions: Infra (what’s hosted, what’s not), Auth, RBAC, Backend Server, Frontend Paradigm, Database choice",
                    "Endpoints",
                    "Section: ‘What I would not do and why.’",
                    "Include how you’d handle analytics and caching.",
                    "Do not write code.",
                ],
                "curveball": "Include how you’d handle analytics and caching.",
            },
            "scoring_guidance": {
                "Clarity": {
                    "1": "Disorganized",
                    "3": "Understandable",
                    "5": "Crisp and visual",
                },
                "Technical depth": {
                    "1": "Surface-level",
                    "3": "Sound",
                    "5": "Thoughtful, cost-aware",
                },
                "Business awareness": {
                    "1": "Pure tech",
                    "3": "Generic MVP",
                    "5": "Client-savvy, phased",
                },
                "Writing": {
                    "1": "Messy",
                    "3": "Adequate",
                    "5": "Clear, narrative voice",
                },
            },
        },
        {
            "id": "super-day",
            "title": "Super Day",
            "order": 4,
            "summary": "Multi-segment live day covering design review, pair programming, business thinking, and mentorship.",
            "prompts": {
                "segments": [
                    {"title": "Design Review", "duration": "45 min", "focus": "Deep architecture discussion"},
                    {"title": "Pair Programming", "duration": "60 min", "focus": "Code + communication"},
                    {"title": "Business Interview", "duration": "30 min", "focus": "Consulting & context thinking"},
                    {"title": "Mentorship Panel", "duration": "30 min", "focus": "Feedback quality & empathy"},
                ],
                "design_review_questions": [
                    "What’s something you know you overengineer sometimes?",
                    "If you had to delete 30% of your system, what would you delete?",
                    "Your app’s backend budget just got cut in half. What’s the first thing to simplify?",
                    "What’s your opinionated take on testing? Be honest.",
                    "How would you explain your architecture to a client who thinks everything should be in Excel?",
                ],
                "pair_programming": {
                    "exercise": "Build a simple notes app with one endpoint and one React component.",
                    "bonus": ["Add basic validation", "Add one test"],
                    "curveballs": [
                        "Now make it multi-user.",
                        "What if the API is 400ms slow — how do you handle it?",
                        "Client wants dark mode but budget’s gone. Your move?",
                    ],
                },
                "business_prompts": [
                    "A CFO wants to ‘modernize their stack.’ What question do you ask first?",
                    "If an investor presentation needs metrics tomorrow, what do you cut corners on — and what do you protect?",
                    "What’s something engineers overcomplicate for clients?",
                    "What’s something you’d never say to a client even if you believed it?",
                ],
                "mentorship_panel": {
                    "prompt": "Here’s a teammate’s PR with some weird naming and a missing null check. Review it out loud.",
                    "follow_ups": [
                        "How do you start a hard code review comment?",
                        "What kind of feedback makes you defensive?",
                        "What advice would you give to your younger self about collaboration?",
                    ],
                },
            },
            "scoring_guidance": {
                "Technical ability": {
                    "1": "Fumbles",
                    "3": "Competent",
                    "5": "Sharp, efficient",
                },
                "Collaboration": {
                    "1": "Silent",
                    "3": "Cooperative",
                    "5": "Empathetic, verbalizes reasoning",
                },
                "Adaptability": {
                    "1": "Rigid",
                    "3": "Adjusts",
                    "5": "Smiles through chaos",
                },
            },
        },
        {
            "id": "paid-trial",
            "title": "Paid Trial",
            "order": 5,
            "summary": "Validate real-world execution, communication, and ownership through a scoped paid engagement.",
            "prompts": {
                "tasks": [
                    "Build or extend a feature in your stack (small full-stack ticket)",
                    "Async Slack communication, short daily update, short demo",
                ],
                "curveball": "Change a requirement midweek — see how they respond.",
            },
            "scoring_guidance": {
                "Reliability": {
                    "1": "Misses updates",
                    "3": "Consistent",
                    "5": "Proactive, anticipates",
                },
                "Communication": {
                    "1": "Silent",
                    "3": "Adequate",
                    "5": "Transparent, calm",
                },
                "Ownership": {
                    "1": "Blames others",
                    "3": "Accountable",
                    "5": "Sees gaps, patches them",
                },
                "Craft": {
                    "1": "Sloppy",
                    "3": "Fine",
                    "5": "Production-ready, thoughtful",
                },
            },
        },
    ],
    "weightings": [
        {"stage": "CEO Behavioral / Message Chain", "weight": 25, "pass_bar": 4.0},
        {"stage": "Async Mini-Test", "weight": 10, "pass_bar": 3.8},
        {"stage": "Take-Home Design", "weight": 20, "pass_bar": 4.0},
        {"stage": "Super Day (All Segments)", "weight": 30, "pass_bar": 4.0},
        {"stage": "Paid Trial", "weight": 15, "pass_bar": 4.2},
    ],
}
