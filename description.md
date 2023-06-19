## Inspiration
I'm inspired to do this project because climate change is without a doubt one of the biggest challenges to humanity & corporations in the world need to act more responsibly to combat it. And while there are a few ESG - E(nvironmental),S(ocial),G(overance) rating agencies (MSCI, Sustainalytics) that provide ESG ratings and scores for companies, As per existing research[1] **these ratings have not correlated with actual sustainability outcomes** because ESG ratings have been largely based on _self-reported data_ and different ratings agencies also assign radically different ratings to the same firms. Rating agencies are mainly focussed on producing a single score for E,S,G pillars for a company leading to news/company information to be aggregated across a lot of datasets *that it essentially invalidates any conflicting/contradicting data sources or information* which is why greenwashing is still difficult to detect through current approaches. 
And while ESG investing has become a mainstream investing strategy, with one third of assets under management(~30-40 trillion $) claiming to take ESG information into account in portfolio allocation decisions, there hasn't been many AI approaches to detect greenwashing and contradicting claims about sustainability efforts of companies. 

Thus Asset management companies, banks, regulatory authorities like `SEC` all **need to analyze companies by more than just looking at their ESG scores**, to see if the sustainability efforts that they claim are true or not i.e. **detect greenwashing and what other environmental risks** a company might be exposed to. This tool provides them some insights and the ability to do so and has potential for a broad applicability and user base. 

## What it does
**Impact AI** is a project to _Identify conflicting/contradictory information of companies sustainability claims aka Greenwashing & identify the environmental, social, governance (ESG) risk exposures of companies_ 

The tool uses AI models like [FinBERT](https://github.com/ProsusAI/finBERT), a model trained on financial text(Yahoo Finance, Financial News) and [Spark Databricks](https://www.databricks.com/spark/getting-started-with-apache-spark) to detect **conflicting sentiments** in a given dataset like earnings call transcripts. Every quarter, a company's leadership holds an earnings call with investors and analysts to update them on the status & performance of the company. The transcript of these calls contain 2 sections -  prepared remarks of C-suite leadership and Q&A which are questions from financial analysts and answers by the C-suite management. These answers unlike the prepared remarks are **more unsuspecting and unrehearsed**

We break down these transcripts into the self-reported prepared remarks and Q&A (Question & Answers) sections and detect ESG topics and compare the sentiments of the statements related to them between the prepared remarks and the Q&A sections and in doing so, we are to detect companies where there have been consistently conflicting information between C-suite leadership and analysts on ESG topics. 

## How we built it
1. We used [Spark Databricks](https://www.databricks.com/spark/getting-started-with-apache-spark) to read the earnings call transcripts dataset available from [Kaggle](https://www.kaggle.com/datasets/tpotterer/motley-fool-scraped-earnings-call-transcripts) and split it into QnA and Prepared Remarks sections. 
This transcript dataset has transcripts from 2019-04-11  to 2023-02-23 so does not have the latest data. 
Since this is a huge dataset Spark distributed system provides us the scale to analyze thousands of companies transcripts across time. Code - `01_clean_split_transcripts_db.py`

2. We used [FinBERT](https://github.com/ProsusAI/finBERT) model to detect the statements related to  E,S,G topics in each of these sections (Qna, Prep. remarks) and then produce sentiments for each of the topics for every transcript per company across these sections. We also set a high thresold for topic detection of 0.7 to avoid false positives in ESG label classification and then store these generated sentiments for further analysis.  Code - `02_esg_score_generation.ipynb`

3. We find conflicting sentiments between C-suite leadership and analysts for each topic and by doing so, we can analyse the companies which have consistently conflicting information between C-suite leadership and analysts on ESG topic and detect greenwashing . We also find the _E,S,G Risk exposures_ that the company faces. Statements related to greenwashing or Risk exposures are also extracted and shown to provide _explainability_ in our model/approach. In the demo we show some contrast examples of contradicting statements b/w leadership and analysts and ESG Risks. You'll be able to see more variation in the Q&A sections because analysts challenges leadership on their ESG initiatives whereas prepared remarks are generally quite positive about their own sustainability initiatives, a contradiction that we are trying to find.  Code - `03_greenwashing_detection.ipynb`

4. We also setup a LLM like [dolly-v2-3b](https://huggingface.co/databricks/dolly-v2-3b) from databricks and ask this LLM if the chosen company is greenwashing. In quite some cases the response is not very informative as it can be seen in the demo. We have also tried some _prompt engineering_ and provide a  context like the company's transcript itself,  which though was not explored in much depth,  initial results were not very promising. Since running dolly requires high compute, we cached the responses in a file in `data` folder for some companies. Code - `dolly_test.py` 

5. We also built an interactive dashboard with ipywidgets and [voila](https://github.com/voila-dashboards/voila) which hosts our application locally. In our dashboard  you can select which company and label(E/S/G) you would like to analyze view the some examples of conflicting statements as described above and shown in the demo. We also add some information like number of companies we analyzed and in which sectors are more likely to have companies with greenwashing claims. 

We have also included a `README.md` file in this git repo on how to start the app and view the dashboard. 

## Challenges we ran into
- Detecting greenwashing is hard 
- Running LLMs requires high computing power and thus performing similar analysis with LLMs require GPUs, which was a limitation for its use.  

## Accomplishments that we're proud of
- Developed a novel method to analyse greenwashing, a topic incredibly important for Climate change, governments and financial institutions
- Incorporated explainabilty into our AI models by providing examples of conflicting statements. Explainabilty is a key concern in adoption of AI in finance. 

## What we learned
- Applicability of LLM and other AI approaches to detecting greenwashing 

## What's next for Impact AI
- Our LLM model(dolly) can be explored further with bigger parameter(12 billion) model and additional prompt engineering. 
- This approach can also be applied to non ESG topics like detecting supply-chain issues and other risks facing companies and such use-case can be explored too. 
- Scale up our model and datasets further with Spark & databricks
- Project pitch to external entities

## References
1. Green or Greenwashing? How Manager and Investor Preferences Shape Firm Strategy - Nathan Barrymore, March 2022. 