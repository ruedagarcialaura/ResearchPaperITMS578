# ResearchPaperITMS578: Comparative Study of International Cybersecurity and AI Policies

**Team Members:**
* Laura Rueda García
* Felipe Susaeta Miguel


## 1. Project Overview

This research project aims to conduct a quantitative comparative study of the cybersecurity and AI governance frameworks of the European Union (EU) and the United States (US): Our core objective is to find real, documented cases of AI-driven cybersecurity incidents in the US and EU to test our central hypothesis. To achieve this, our strategy relies on two key components: precise keywords and high-quality data sources.

Our **central hypothesis** is that a tangible difference exists in the volume of publicly reported cyber incidents between the two regions, influenced by their distinct regulatory environments. Our primary goal is to build a dataset of publicly reported incidents from 2020 to 2025 by systematically collecting data from various online sources. This dataset will form the basis of our statistical analysis.

## 2. Definitive Keywords (Our AI Filter)
Our script will use the following list of keywords to identify an incident as "AI-driven". These terms focus on the specific techniques and tactics used in modern AI-related attacks.

* **Specific Attack Techniques:**
    * `deepfake`
    * `adversarial attack`
    * `model poisoning`
    * `data poisoning`
    * `model inversion`

* **Tools & Tactics:**
    * `ai-powered phishing`
    * `generative ai fraud`
    * `ai-driven malware`

* **Broader Context:**
    * `machine learning breach`
    * `ai security incident`



## 3. Research Strategy & Methodology

Our methodology is a **quantitative-first comparative analysis**. The strategy is as follows:

1.  **Identify Data Sources:** We will identify and vet a list of reliable public data sources for cyber incidents. These will include government breach notification portals (US State Attorneys General sites), vulnerability databases (via APIs like the NIST NVD), and specialized cybersecurity news feeds (via RSS). 

2.  **Automated Data Collection:** We will develop a Python script to automatically query, scrape, and parse these sources. The script's main function is to aggregate incident reports into a single, standardized format.

3.  **Unified Dataset Generation:** The script will output a structured `incidents_database.csv` file. Each entry will contain key metadata: date, region (US/EU), source URL, and a brief description or title.

4.  **Statistical Analysis:** Our primary analysis will involve comparing the frequency of reported incidents between the US and the EU over our defined time period. We will visualize this data to identify trends.


https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/ai-powered-cyberattacks/
