import csv
import os
import random
from datetime import datetime, timedelta

os.makedirs('data/market_data', exist_ok=True)

# 1. Sample Articles for quick test in Text Analyzer
sample_articles = [
    {
        "id": "sample_1",
        "title": "Tesla Reports Q3 Production and Delivery Numbers",
        "company": "Tesla",
        "text": "Tesla reported stronger-than-expected quarterly revenue driven by increased vehicle deliveries, although rising production costs and price cuts in China could pressure operating margins. Operating income rose 8% year-over-year to $2.5 billion, but automotive gross margin contracted to 17.2%. Chief Financial Officer noted persistent supply chain bottlenecks and elevated raw material expenditures."
    },
    {
        "id": "sample_2",
        "title": "NVIDIA Blackwell AI Superchip Shipments Accelerate",
        "company": "NVIDIA",
        "text": "NVIDIA Corporation announced surging enterprise demand for its next-generation Blackwell architecture GPUs. CEO Jensen Huang highlighted unprecedented data center capital expenditure from Microsoft, Google, and Amazon totaling over $40 billion. Operating cash flow expanded 125%, though executives acknowledged geopolitical export restrictions and foundry capacity limits remain key operational risks."
    },
    {
        "id": "sample_3",
        "title": "Reliance Industries Announces Mega Clean Energy Investment",
        "company": "Reliance Industries",
        "text": "Reliance Industries announced a ₹75,000 crore investment in renewable energy gigafactories and green hydrogen infrastructure in Gujarat. Chairman Mukesh Ambani affirmed that the digital and retail divisions registered 18% EBITDA growth, while debt-to-equity ratio moderated to 0.42. Analysts praised the capital allocation discipline amid global interest rate volatility."
    },
    {
        "id": "sample_4",
        "title": "Apple Services Revenue Hits All-Time High Amid Hardware Headwinds",
        "company": "Apple",
        "text": "Apple Inc. posted quarterly revenue of $94.9 billion, fueled by record $24.97 billion Services revenue across App Store, Cloud, and Apple Pay. iPhone sales grew a modest 5.5% while Greater China revenue fell 0.3% due to intensifying competition from Huawei. Regulatory scrutiny from the European Commission and antitrust litigation represent sustained legal risks."
    },
    {
        "id": "sample_5",
        "title": "Infosys Revises Annual Revenue Guidance Amid Tech Spending Caution",
        "company": "Infosys",
        "text": "Infosys narrowed its constant-currency revenue growth guidance to 3.75%-4.5% as banking and financial services clients in North America curtailed discretionary digital transformation spending. Operating margin stood resilient at 21.1%. Wage hikes and elevated attrition in specialized AI engineering roles present near-term margin pressure."
    },
    {
        "id": "sample_6",
        "title": "Microsoft Cloud Momentum Continues with Azure Expansion",
        "company": "Microsoft",
        "text": "Microsoft Corp delivered stellar commercial cloud revenue exceeding $38.9 billion, up 21% driven by commercial demand for Azure AI copilot solutions. Capital expenditure increased sharply to $19 billion to fund data center buildouts. Management warned that compute capacity shortages could restrain cloud revenue acceleration."
    }
]

with open('data/sample_articles.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["id", "title", "company", "text"])
    writer.writeheader()
    for row in sample_articles:
        writer.writerow(row)

print("Created sample_articles.csv")

# 2. Comprehensive Financial News Dataset (80 articles across 8 companies)
companies_data = {
    "NVIDIA": [
        ("NVIDIA Data Center Revenue Surges 154% on Generative AI Surge", "NVIDIA posted record revenue of $30.0 billion, up 122% from a year ago, driven by hyper-scaler AI clustering demand. Data center compute revenue surged with gross margins reaching 75.1%. Executives highlighted strong cash generation of $14.5 billion.", "Positive", "Reuters"),
        ("Export Control Tightening May Restrict NVIDIA Chip Shipments to Key Asian Markets", "U.S. Department of Commerce unveiled tighter licensing thresholds on advanced semiconductor accelerators. NVIDIA disclosed that sales to affected regions previously accounted for 20-25% of data center revenue, posing regulatory risk.", "Negative", "Bloomberg"),
        ("NVIDIA and Foxconn Partner on Sovereign AI Infrastructure in Asia", "NVIDIA entered a collaborative manufacturing and data center deployment pact with Foxconn to build high-performance computing centers in Taiwan and Mexico. The initiative strengthens supply chain integration.", "Positive", "Financial Times"),
        ("Supply Chain Constraints at TSMC Advanced Packaging Limit Near-Term GPU Output", "NVIDIA acknowledged that CoWoS packaging capacity at Taiwan Semiconductor Manufacturing Co remains tight through early next year. While customer backlog remains multi-quarter, shipment delivery timelines face operational friction.", "Negative", "Wall Street Journal"),
        ("NVIDIA Expands Automotive and Robotics AI Ecosystem with Orin Architecture", "Automotive revenue expanded 37% year-over-year to $346 million as electric vehicle manufacturers adopted autonomous driving silicon. Software licensing margins improved overall profitability.", "Positive", "MarketWatch"),
        ("Wall Street Analysts Maintain Overweight on NVIDIA Ahead of Blackwell Rollout", "Morgan Stanley reiterated its Top Pick rating with an increased price target of $150, citing high ROI on enterprise AI infrastructure investments and pricing power.", "Positive", "CNBC"),
        ("NVIDIA Enterprise AI Software Subscriptions Gain Momentum", "Annualized recurring revenue from NVIDIA AI Enterprise software suite crossed $1 billion, showcasing software diversification beyond core GPU hardware manufacturing.", "Positive", "Reuters"),
        ("Competition Intensifies as Custom Cloud Silicon from Google and Amazon Emerges", "Cloud service providers accelerate internal TPU and Trainium accelerator deployments. While NVIDIA maintains software moat via CUDA, long-term merchant silicon pricing pressure looms.", "Neutral", "The Verge"),
        ("NVIDIA Quarterly Dividend Declared Alongside $50 Billion Share Buyback Plan", "Board of directors approved an additional $50 billion share repurchase authorization following record operating cash flow and balance sheet strength.", "Positive", "PR Newswire"),
        ("NVIDIA Faces Regulatory Review Over Run:ai Acquisition in European Union", "Antitrust authorities in the European Union initiated preliminary merger inquiries regarding NVIDIA's proposed acquisition of workload management startup Run:ai.", "Negative", "Financial Times")
    ],
    "Tesla": [
        ("Tesla Quarterly Deliveries Surpass Expectations Driven by Model Y Demand", "Tesla delivered 462,890 vehicles in the third quarter, marking a 6.4% rebound from previous quarters as financing promotions stimulated North American retail demand.", "Positive", "Reuters"),
        ("Price Reductions in European and Asian Markets Dampen Automotive Gross Margins", "Tesla cut prices across Model 3 and Model Y variants in response to intensifying competition from BYD. Automotive gross margin excluding regulatory credits dropped to 14.6%, heightening cost pressure.", "Negative", "Bloomberg"),
        ("Tesla Energy Storage Deployment Surges to Record 6.9 GWh", "Megapack and Powerwall installations achieved 157% annual growth, generating $3.0 billion in quarterly revenue with record gross margin of 30.5%, proving energy division profitability.", "Positive", "Electrek"),
        ("NHTSA Opens Safety Defect Investigation into Tesla Full Self-Driving Feature", "National Highway Traffic Safety Administration launched a preliminary evaluation examining low-visibility collision incidents involving Full Self-Driving system, signaling regulatory compliance risk.", "Negative", "Wall Street Journal"),
        ("Tesla Robotaxi Cybercab Unveiled with Autonomous Ride-Hail Ambitions", "Elon Musk presented the two-seater Cybercab and autonomous Robovan prototypes, projecting sub-$30,000 retail pricing and unsupervised regulatory approvals in Texas and California.", "Neutral", "TechCrunch"),
        ("Raw Material Costs for Lithium Iron Phosphate Batteries Normalize", "Battery cell input costs declined 18% over the past two quarters, helping offset assembly line retooling expenses at Giga Texas and Berlin factories.", "Positive", "Reuters"),
        ("Tesla Giga Mexico Timeline Paused Amid Trade Tariff Uncertainties", "Construction planning for the Nuevo Leon gigafactory remains paused pending geopolitical trade policy clarification and electric vehicle tariff reviews.", "Negative", "Mexico Daily Post"),
        ("Tesla Free Cash Flow Recovers to $2.7 Billion on Capital Expenditure Discipline", "Third-quarter free cash flow demonstrated sharp rebound as inventory buildup reversed and operating efficiencies scaled across manufacturing plants.", "Positive", "CNBC"),
        ("Rising Labor Costs and Unionization Scrutiny at German Gigafactory", "IG Metall union raised concerns over worker overtime and safety standards at the Berlin-Brandenburg facility, potentially raising European operating wage costs.", "Negative", "Handelsblatt"),
        ("Tesla Megafactory Shanghai Construction Approaches Final Mechanical Testing", "Commercial scale Megapack production in China remains on schedule to initiate commercial deliveries, targeting expanding grid storage markets in Australia and Europe.", "Positive", "Xinhua")
    ],
    "Apple": [
        ("Apple Q4 Revenue Hits Record $94.9 Billion with Robust Services Momentum", "Apple reported quarterly revenue growth across Americas and Europe, led by record Services gross margins of 74.0%. Active installed device base exceeded 2.2 billion units globally.", "Positive", "Reuters"),
        ("EU Digital Markets Act Compliance Forces Fee Restructuring on iOS App Store", "European Commission investigated Apple's Core Technology Fee structure, raising legal risks and potential regulatory penalties up to 10% of annual worldwide revenue.", "Negative", "Financial Times"),
        ("Apple Intelligence Launch Drives Strong iPhone 16 Pro Upgrade Cycle", "Initial carrier data indicates consumer demand for Apple Intelligence features accelerated high-margin Pro and Pro Max sales mix across the United States and Japan.", "Positive", "Bloomberg"),
        ("China Smartphone Shipments Encounter Fierce Domestic Flagship Competition", "Counterpoint Research indicated iPhone sales in Mainland China contracted 2.4% as domestic competitors Huawei and Vivo gained market share in premium tiers.", "Negative", "South China Morning Post"),
        ("Apple Authorizes $110 Billion Share Repurchase and Dividend Increase", "Apple returned $29 billion to shareholders during the quarter through dividends and open-market share buybacks, reinforcing robust capital return policy.", "Positive", "Wall Street Journal"),
        ("Supply Chain Transition Toward India Accelerates for Global iPhone Exports", "Foxconn and Pegatron expanded assembly capacity in Tamil Nadu, targeting 25% of worldwide iPhone assembly from India by 2026 to mitigate geographic risk.", "Positive", "Economic Times"),
        ("Legal Ruling in Department of Justice Antitrust Lawsuit Sets Protracted Timeline", "Federal district court set pretrial deadlines for the ongoing DOJ monopolization lawsuit examining smartphone ecosystem integration, prolonging litigation overhang.", "Negative", "Reuters"),
        ("Apple Watch Health Sensor Patent Dispute Incurs R&D Redesign Costs", "Customs clearance modifications and legal patent licensing talks continued with Masimo, requiring software workarounds for pulse oximetry features.", "Negative", "CNBC"),
        ("M4 Chip Family Unveiled Across Mac Lineup Featuring Industry-Leading NPU Performance", "Apple introduced updated MacBook Pro and iMac models powered by TSMC 3-nanometer M4 silicon, lifting computer hardware average selling prices.", "Positive", "MacRumors"),
        ("Supply Cost Pressures from Advanced OLED Displays Manageable Through Vendor Diversity", "Display panel procurement from Samsung Display and LG Display allowed Apple to negotiate stable unit costs for next-generation tablet and phone lines.", "Neutral", "Nikkei Asia")
    ],
    "Microsoft": [
        ("Microsoft Cloud Revenue Tops $38.9 Billion with 29% Azure Cloud Growth", "Microsoft reported outstanding fiscal first quarter revenue of $65.6 billion, up 16% year-over-year. Intelligent Cloud division operating income reached $10.5 billion.", "Positive", "Reuters"),
        ("Capital Expenditures Surge to $19 Billion to Meet Skyrocketing AI Datacenter Capacity", "Satya Nadella emphasized that AI infrastructure investments are required to satisfy customer waitlists, though higher depreciation may moderate near-term margins.", "Neutral", "Bloomberg"),
        ("Copilot Enterprise Adoption Reaches 70% of Fortune 500 Enterprises", "Microsoft 365 Copilot recorded triple-digit seat expansion as enterprise customers automated business workflows, raising software average revenue per seat.", "Positive", "ZDNet"),
        ("UK Competition and Markets Authority Reviews Microsoft OpenAI Multi-Billion Partnership", "British and European competition watchdogs examined cloud computing exclusivity provisions and equity governance in foundational AI developer alliances.", "Negative", "Financial Times"),
        ("Cybersecurity Initiatives and Secure Future Overhaul Require Internal Resource Reallocation", "Following federal security review recommendations, Microsoft dedicated over 34,000 engineers to core infrastructure security remediation.", "Neutral", "The Register"),
        ("Xbox Content and Services Revenue Soars 61% Post Activision Blizzard Integration", "Gaming segment revenue grew substantially following inclusion of Call of Duty franchise, diversifying consumer digital subscription revenue streams.", "Positive", "VentureBeat"),
        ("Energy and Grid Interconnection Delays Pose Operational Risk to Data Center Expansion", "Public utilities in Virginia and Ireland warned of extended grid power connection queues, challenging timelines for new hyperscale cloud data centers.", "Negative", "Wall Street Journal"),
        ("Microsoft Returns $9.0 Billion to Shareholders via Dividends and Buybacks", "Operating cash flow expanded 34% to $34.2 billion, enabling simultaneous high-intensity AI CapEx and disciplined shareholder cash distribution.", "Positive", "PR Newswire"),
        ("Enterprise Software Churn Remains Historic Low Amid Windows 11 Refresh", "Corporate PC replacement cycles and end-of-support timelines for legacy operating systems supported stable commercial Windows licensing revenue.", "Positive", "Computerworld"),
        ("AI Inference Unit Economics Improve Through In-House Maia 100 Accelerators", "Deployment of custom silicon in production Azure clusters reduced operational reliance on third-party GPUs, lowering unit token serving costs.", "Positive", "AnandTech")
    ],
    "Amazon": [
        ("Amazon Operating Income Jumps 55% as AWS and Retail Efficiency Accelerate", "Amazon posted net income of $15.3 billion as North American retail fulfillment optimization and 19% AWS cloud growth lifted corporate operating margins to 11.0%.", "Positive", "Reuters"),
        ("Amazon Web Services Secures Multi-Billion Dollar Enterprise AI Migrations", "AWS announced strategic enterprise cloud migrations with major financial institutions, generating record sales pipeline and expanding recurring contract backlogs.", "Positive", "Bloomberg"),
        ("Federal Trade Commission Antitrust Lawsuit Moves Toward Discovery Phase", "FTC litigation challenging Amazon marketplace algorithms and logistics tie-ins poses long-term compliance overhead and potential structural remedies.", "Negative", "Wall Street Journal"),
        ("Project Kuiper Satellite Constellation Deployment Faces Launch Delays", "Capital expenditures for orbital broadband infrastructure increased to $2.5 billion, while rocket booster delivery setbacks from launch providers created timeline risk.", "Negative", "SpaceNews"),
        ("Amazon Advertising Services Revenue Expands 19% to $14.3 Billion", "Sponsored products and Prime Video ad-tier rollout generated high-margin revenue streams, outpacing digital advertising industry peers.", "Positive", "Adweek"),
        ("Regional Fulfillment Network Restructuring Lowers Per-Unit Shipping Costs", "Inbound fulfillment architecture improvements shaved $0.45 per unit in handling costs while accelerating same-day and next-day delivery speeds.", "Positive", "SupplyChainBrain"),
        ("Rising Delivery Fleet Insurance and Driver Wage Pressures in Urban Hubs", "Contracted delivery service partners faced increased vehicle insurance rates and localized wage increases, elevating transport operating expenses.", "Negative", "FreightWaves"),
        ("Amazon Pharmacy and Healthcare Services Expand Same-Day Prescription Delivery", "Expansion into 20 metropolitan areas enhanced Prime subscriber retention and unlocked healthcare digital commerce monetization.", "Positive", "Fierce Healthcare"),
        ("European Retail Sales Soften Amid Consumer Discretionary Spending Caution", "Inflationary pressure in Germany and France moderated non-essential merchandise sales, although grocery and consumable volumes held steady.", "Neutral", "Retail Week"),
        ("Robotics Automation at Next-Gen Sortation Centers Boosts Throughput 25%", "Deployment of Sequoia and Sparrow robotic handling systems minimized package sorting cycle times and reduced repetitive workplace injuries.", "Positive", "Modern Materials Handling")
    ],
    "Reliance Industries": [
        ("Reliance Industries Q2 Net Profit Reaches ₹19,324 Crore on Retail and Jio Strength", "RIL reported consolidated quarterly EBITDA of ₹43,934 crore. Telecom subscriber additions reached 498 million, with 5G data traffic crossing 30% of aggregate network volume.", "Positive", "Economic Times"),
        ("Oil-to-Chemicals Margins Soften Amid Global Refinery Oversupply and Weak Cracks", "O2C segment EBITDA declined 23.7% due to subdued global transportation fuel crack spreads and planned maintenance turnaround at Jamnagar refinery complex.", "Negative", "Business Standard"),
        ("Reliance Jio and Meta Partner to Launch AI Enterprise Solutions in India", "Joint initiative targets deploying indigenous localized AI models and digital retail commerce tools for 30 million small and medium enterprises across India.", "Positive", "LiveMint"),
        ("Reliance New Energy Gigafactory in Jamnagar on Track for Phased Commissioning", "Solar PV module manufacturing facility with 10 GW capacity enters final testing, advancing the conglomerate's ₹75,000 crore clean tech transition.", "Positive", "Hindu BusinessLine"),
        ("Debt-to-Equity Ratio Remains Prudent at 0.44 Despite Sustained Capital Outlays", "Consolidated net debt stabilized at ₹1.16 lakh crore as strong operating cash flows from consumer businesses funded ongoing infrastructure expansions.", "Positive", "Financial Express"),
        ("Petrochemical Feedstock Volatility and Chinese Polymer Inflows Impact Realizations", "Surge in low-cost polymer exports from Northeast Asia pressured domestic pricing power, prompting domestic industry representations for anti-dumping duties.", "Negative", "Plastics News"),
        ("Reliance Retail Expands Store Network to 18,918 Outlets with 79 Million Sq Ft", "Retail footfalls surpassed 297 million during festive shopping quarter, with digital and omnichannel orders accounting for 18% of total gross sales.", "Positive", "Retail4Growth"),
        ("Jio Financial Services Expands Digital Lending and Asset Management Tie-Ups", "Strategic wealth joint venture with BlackRock received regulatory clearance, opening scalable distribution channels across retail investor bases.", "Positive", "CNBC-TV18"),
        ("Crude Oil Benchmark Volatility Presents Upstream Revenue Fluctuations", "Fluctuations in Brent crude benchmarks and windfall tax adjustments created short-term variability in offshore KG-D6 gas realization yields.", "Neutral", "Energy World"),
        ("Green Hydrogen Electrolyzer Production Facility Breaks Ground in Gujarat", "Partnership with Stiesdal on alkaline electrolyzer manufacturing positions company to achieve sub-$2 per kg green hydrogen production targets.", "Positive", "Renewable Watch")
    ],
    "TCS": [
        ("TCS Posts Q2 Revenue of ₹64,259 Crore with Robust 24.1% Operating Margin", "Tata Consultancy Services recorded 8% year-on-year revenue expansion, securing $8.6 billion in total contract value driven by cost optimization and cloud transformation deals.", "Positive", "Economic Times"),
        ("Cautious Tech Discretionary Spending in North American Banking and Insurance", "BFSI segment client decision cycles remained elongated as enterprise customers deferred non-critical digital transformation projects amid elevated interest rates.", "Negative", "Business Standard"),
        ("TCS Wins £800 Million UK National Insurance and Pension Transformation Contract", "Multi-year deal with UK government agency solidifies European market leadership and provides stable long-term recurring revenue visibility.", "Positive", "Financial Times"),
        ("Employee Retention Improves as Trailing Twelve Month Attrition Drops to 12.3%", "HR interventions and campus training programs stabilized workforce churn, reducing subcontracting and lateral recruitment expenditure.", "Positive", "LiveMint"),
        ("TCS Announces Interim Dividend of ₹10 Per Share Following Healthy Cash Conversion", "Free cash flow to net income conversion stood at 102%, reflecting disciplined collections and minimal client credit delinquency across global geos.", "Positive", "CNBC-TV18"),
        ("Wage Increment Cycle and Visa Compliance Expenses Squeeze Q1 Margins Slightly", "Annual merit salary hikes and seasonal visa application fees contributed 150 basis points headwind to operating margin before operational offsets.", "Negative", "Deccan Herald"),
        ("TCS AI-Ready Workforce Reaches 350,000 Trained Associates on Generative AI", "Largest corporate upskilling program positions IT major to deliver enterprise GenAI pilots in banking, retail, and manufacturing sectors.", "Positive", "TechCircle"),
        ("Continental European Geographies Experience Slower Deal Conversion Cycles", "Macroeconomic headwinds in Germany and Nordic markets delayed manufacturing technology modernization contracts by 2 to 3 quarters.", "Negative", "Economic Times"),
        ("TCS BaNCS Core Banking Platform Deployed at Major European Commercial Bank", "Cloud-native banking software suite processed record high-frequency transaction volumes, boosting IP-led software licensing revenue.", "Positive", "IBS Intelligence"),
        ("Geopolitical Tensions in Middle East and Eastern Europe Monitored for Client Delivery", "Management confirmed business continuity measures in regional delivery centers remain robust with no material disruption to offshore service delivery.", "Neutral", "The Hindu")
    ],
    "Infosys": [
        ("Infosys Raises Annual Revenue Growth Guidance to 3.75%-4.5% After Strong Q2", "Infosys posted quarterly revenue of $4,894 million with constant currency growth of 3.1% sequentially, powered by manufacturing, energy, and retail recovery.", "Positive", "Economic Times"),
        ("Large Deal Total Contract Value Reaches $2.4 Billion with High New Deal Mix", "Company signed 21 large transformation deals, with net new commitments representing 52% of total contract value across Europe and North America.", "Positive", "LiveMint"),
        ("BFSI and Telecom Client Discretionary Spending Remains Subdued in US", "While core maintenance and regulatory compliance projects continued, experimental cloud discretionary investments experienced budgeting scrutiny.", "Negative", "Business Standard"),
        ("Infosys Topaz Generative AI Platform Embedded in Over 300 Client Projects", "Proprietary generative AI platform accelerated code refactoring and customer operations modernization, unlocking higher billing rates on specialized squads.", "Positive", "TechCrunch"),
        ("Operating Margin Expands 30 Basis Points to 21.1% on Project Maximus Cost Efficiency", "Comprehensive cost optimization program generated savings in subcontractor utilization, travel, and onsite-offshore delivery pyramid ratios.", "Positive", "Financial Express"),
        ("Voluntary Attrition Moderates to 12.9% Amid Tailored Career Progression Plans", "Attrition levels declined for the sixth consecutive quarter, supporting operational productivity and minimizing talent replacement costs.", "Positive", "Deccan Herald"),
        ("Elevated Onsite Subcontractor Costs in Specialized Cybersecurity Roles", "Shortage of certified cloud architects in Western European locations necessitated higher temporary contractor spending, exerting localized cost pressure.", "Negative", "The Hindu"),
        ("Infosys Declares Interim Dividend of ₹21 Per Share and Affirms Capital Allocation", "Strong balance sheet liquidity with cash and investments of $4.1 billion supported steady returns to global institutional and retail investors.", "Positive", "CNBC-TV18"),
        ("Litigation Over Former Employee Restrictive Covenants Handled Internally", "Arbitration matters concerning senior leadership transitions and non-compete clauses resolved with negligible financial impact on corporate operations.", "Neutral", "Business Today"),
        ("Automotive Software Engineering Pact Expanded with Leading German OEM", "Multi-year deal to build in-vehicle infotainment operating system architecture enhances company's engineering R&D market share.", "Positive", "Autocar Pro")
    ]
}

start_date = datetime(2025, 1, 10)
all_articles = []
article_counter = 1

for company, articles in companies_data.items():
    for i, (headline, text, sentiment, source) in enumerate(articles):
        pub_date = (start_date + timedelta(days=i * 22 + random.randint(1, 5))).strftime("%Y-%m-%d")
        all_articles.append({
            "article_id": f"art_{article_counter:03d}",
            "company": company,
            "date": pub_date,
            "headline": headline,
            "text": text,
            "sentiment": sentiment,
            "source": source
        })
        article_counter += 1

with open('data/financial_news.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["article_id", "company", "date", "headline", "text", "sentiment", "source"])
    writer.writeheader()
    for row in all_articles:
        writer.writerow(row)

print(f"Created financial_news.csv with {len(all_articles)} articles.")

# 3. Market Data Generation (Historical OHLCV for 8 companies, ~350 trading days)
base_prices = {
    "NVIDIA": {"ticker": "NVDA", "base": 115.0, "drift": 0.0018, "vol": 0.028, "vol_base": 45000000},
    "Tesla": {"ticker": "TSLA", "base": 210.0, "drift": 0.0008, "vol": 0.032, "vol_base": 75000000},
    "Apple": {"ticker": "AAPL", "base": 185.0, "drift": 0.0009, "vol": 0.015, "vol_base": 48000000},
    "Microsoft": {"ticker": "MSFT", "base": 405.0, "drift": 0.0011, "vol": 0.016, "vol_base": 22000000},
    "Amazon": {"ticker": "AMZN", "base": 175.0, "drift": 0.0012, "vol": 0.020, "vol_base": 35000000},
    "Reliance Industries": {"ticker": "RELIANCE", "base": 2750.0, "drift": 0.0007, "vol": 0.014, "vol_base": 6500000},
    "TCS": {"ticker": "TCS", "base": 3950.0, "drift": 0.0006, "vol": 0.012, "vol_base": 2200000},
    "Infosys": {"ticker": "INFY", "base": 1620.0, "drift": 0.0008, "vol": 0.016, "vol_base": 7800000}
}

random.seed(42)
days = 320
start_trading_day = datetime(2025, 1, 2)

for comp_name, config in base_prices.items():
    ticker = config["ticker"]
    curr_price = config["base"]
    rows = []
    
    current_date = start_trading_day
    day_count = 0
    
    while day_count < days:
        if current_date.weekday() < 5: # Monday - Friday
            ret = random.gauss(config["drift"], config["vol"])
            curr_price = max(10.0, curr_price * (1 + ret))
            day_high = curr_price * (1 + abs(random.gauss(0.005, 0.006)))
            day_low = curr_price * (1 - abs(random.gauss(0.005, 0.006)))
            day_open = curr_price * (1 + random.gauss(0, 0.004))
            day_vol = int(config["vol_base"] * random.uniform(0.7, 1.45))
            
            rows.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "company": comp_name,
                "ticker": ticker,
                "open": round(day_open, 2),
                "high": round(max(day_high, day_open, curr_price), 2),
                "low": round(min(day_low, day_open, curr_price), 2),
                "close": round(curr_price, 2),
                "volume": day_vol
            })
            day_count += 1
        current_date += timedelta(days=1)
        
    filepath = f"data/market_data/{ticker}.csv"
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["date", "company", "ticker", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Generated {filepath} with {len(rows)} trading days.")

print("All datasets successfully generated!")
