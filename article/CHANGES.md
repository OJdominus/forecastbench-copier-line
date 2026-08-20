# Every change to your two documents

Compared against the text of the two PDFs you shared. Formatting artifacts from the PDF
export are filtered out, so what follows is editorial only.


---

## Long-form: your document to DRAFT_v7

*40 sentences rewritten, 39 added, 17 removed.*

### Rewritten

**1.**

> ~~Namely, Cassi-2026-05-10 and the superforecaster median .~~

> **Namely, Cassi-2026-05-10 and the superforecaster median.**

**2.**

> ~~Those two are what this piece focuses on Why we are looking into this:~~

> **Those two are what this piece focuses on.**

**3.**

> ~~In July this year, the Forecasting Research Institute (FRI) released a report that claims AI models are performing at the same level with superforecasters on ForecastBench.~~

> **Why we are looking into this In July this year, the Forecasting Research Institute (FRI) released a report that claims AI models are performing at the same level with superforecasters on ForecastBench.**

**4.**

> ~~Now, market questions are a better test of human-like forecasting skill, as they often require judgment about novel, one-off events, making it a huge deal that an AI system beat superforecasters on those questions.~~

> **FRI argues that market questions are the better test of human-like forecasting skill, as they often require judgment about novel, one-off events.**

**5.**

> ~~Three weeks later, Good Judgement countered with a response.~~

> **Three weeks later, Good Judgment countered with a response.**

**6.**

> ~~Another piece of evidence we can put into view is a test run by the Financial Times (FT) on AI against both the market and human superforecasters on Federal Reserve interest rate decisions.~~

> **Another piece of evidence we can put into view is a test run by the Financial Times (FT) on AI against both the market and human superforecasters on Federal Reserve interest rate decisions, reported here secondhand through Good Judgment's summary.**

**7.**

> ~~The AI drew level with humans and not better.~~

> **The AI drew level with the market and not better.**

**8.**

> ~~The two that are clear are Cassi-2026-05-10 ( -0.0220, CI -0.0403 to -0.0055) and the superforecaster median ( 0.0173, CI 0.0354 to 0.0016).~~

> **Cassi-2026-05-10 (-0.0220, CI -0.0403 to -0.0055, exact bootstrap p = 0.004) and the superforecaster median (-0.0173, CI -0.0354 to -0.0016, p = 0.017).**

**9.**

> ~~Superforecasters sit 4.67 above it, and Cassi 5.67 above it.~~

> **Superforecasters sit 4.67 above it, Cassi 5.67.**

**10.**

> ~~FRI reports a bootstrap one-sided p-value of 0.41 for Cassi against the null that it is equally accurate as superforecasters, with 0.16 and 0.15 for xAI's submissions and 0.14 for Google DeepMind's.~~

> **Two different nulls, and 527 tests FRI reports a bootstrap one-sided p-value of 0.41 for Cassi against the null that it is equally accurate as superforecasters, with 0.16 and 0.15 for xAI's submissions and 0.14 for Google DeepMind's.**

**11.**

> ~~Both findings can be true:~~

> **Both findings can be true, and they are complementary.**

**12.**

> ~~What Counts as a Market Question Each forecasting round has 500 questions total, split evenly into 250 market questions and 250 dataset questions.~~

> **What Counts as a Market Question Each round contains 500 questions, 250 market and 250 dataset.**

**13.**

> ~~Market questions take one forecast, and dataset questions go up to eight.~~

> **Market questions take one forecast, dataset questions up to eight.**

**14.**

> ~~The preliminary board scores only the dataset questions.~~

> **The preliminary board scores dataset questions only.**

**15.**

> ~~The tournament board includes both dataset and market questions and determines the overall score.~~

> **The tournament board adds market questions and produces the overall score, and it is the board the parity commentary cites.**

**16.**

> ~~The baseline board contains forecast files without the frozen market prices.~~

> **The baseline board holds forecast files without freeze values.**

**17.**

> ~~The tournament and baseline boards also use different adjustments for question difficulty, but the methodology does not explain how they differ.~~

> **The two boards use different difficulty adjustments, which the methodology addendum does not state.**

**18.**

> ~~Over five consecutive days, none of the 2,987 market-question adjustments changed on the tournament board, while all 2,987 changed on the baseline board.~~

> **Across five consecutive days of published fixed-effects files, 0 of 2,987 market question fixed effects changed on the tournament board and 2,987 of 2,987 changed on the baseline board.**

**19.**

> ~~The analysis below therefore focuses only on the tournament board.~~

> **Everything below concerns the tournament board.**

**20.**

> ~~How the Market Score Is Computed Everything after this section depends on how the benchmark calculates its market score.~~

> **How the Market Score Is Computed Everything after this section depends on it.**

**21.**

> ~~All three scoring functions are in src/leaderboard/main.py, which is MIT licensed.~~

> **All of it is in src/leaderboard/main.py in the ForecastBench repository, MIT licensed.**

**22.**

> ~~That distinction sets the range of the copier line below, and it limits behavioral inference.~~

> **That distinction sets the range of the copier line below, and it limits behavioural inference.**

**23.**

> ~~The Copier Line Because market question difficulty is the market's own Brier score, a forecaster submitting a price verbatim scores zero on the adjusted scale, and its index is (1 √ C) × Two prices give two lines.~~

> **The Copier Line Because market question difficulty is the market's own Brier score, a forecaster submitting a price verbatim scores zero on the adjusted scale, and its index is (1 - √C) × 100.**

**24.**

> ~~The shown-price line at 70.93 is the behavioral zero, the score for adding nothing to what was in the prompt.~~

> **The shown-price line at 70.93 is the behavioural zero, the score for adding nothing to what was in the prompt.**

**25.**

> ~~Superforecasters sit 4.67 above it and Cassi 5.67.~~

> **Superforecasters sit 4.67 above it, Cassi 5.67.**

**26.**

> ~~ForecastBench runs its own baseline models twice on identical question sets, once with the freeze value in the prompt and once without.~~

> **What the Freeze Value Buys ForecastBench runs its own baseline models twice on identical question sets, once with the freeze value in the prompt and once without.**

**27.**

> ~~Median improvement: 15.66 Brier Index points, and 29 of 30 runs improved.~~

> **Median improvement per run: 15.66 Brier Index points, and 29 of 30 runs improved.**

**28.**

> ~~Without the price, ForecastBench's own baseline models score 51.5, close to the 50 that always predicts 50% would score.~~

> **Without the price, ForecastBench's own baseline models score 51.5, close to the 50 that always predicting 50% would score.**

**29.**

> ~~Among the top 30 entries, the share of forecasts within half a percentage point of the market price reaches 67% for red-lizard, 58% for blue-turtle, 47% for green-plant, 45% for blue-croc, 42% for the voicetree-axiom entries, and 41% for big-green-leaf.~~

> **Among top-30 entries the share of forecasts within half a percentage point of the market price reaches 67% for red-lizard, 58% for blue-turtle, 47% for green-plant, 45% for blue-croc, 42% for the voicetree-axiom entries, and 41% for big-green-leaf.**

**30.**

> ~~Those are anonymized external submissions whose prompt conditions are unpublished.~~

> **Those are anonymised external submissions whose prompt conditions are unpublished.**

**31.**

> ~~One reads, "I think the current market price of 36% is about right." Another describes updating toward a crowd consensus as more confident than the forecaster's own view.~~

> **One reads, "I think the current market price of 36% is about right." Another describes updating toward a crowd consensus more confident than the forecaster's own view.**

**32.**

> ~~Of the 57 market questions from that round that have resolved, none were imputed; their raw Brier is 0.0830 against the market's 0.1003.~~

> **On the 57 market questions from that round that have resolved, none imputed, their raw Brier is 0.0830 against the market's 0.1003.**

**33.**

> ~~Platform mix implies a difficulty of 0.0799 for the human subset against 0.0768 for the pool.~~

> **Platform mix implies difficulty of 0.0799 for the human subset against 0.0768 for the pool.**

**34.**

> ~~Pool-wide bin means an average of 527 entries, 437 of which score below the market, and some sit near +0.20.~~

> **Pool-wide bin means average 527 entries, 437 of which score below the market, and some sit near +0.20.**

**35.**

> ~~The demand generalizes past this benchmark.~~

> **The demand generalises past this benchmark.**

**36.**

> ~~Agentic benchmarks hand it to the tooling and often the hints.~~

> **Agentic benchmarks hand it the tooling and often the hints.**

**37.**

> ~~Eight Things This Doesn't Cover The bootstrap covers 527 entries with at least 50 resolved market questions from the processed forecast sets.~~

> **The bootstrap covers 527 entries with at least 50 resolved market questions, from the processed forecast sets.**

**38.**

> ~~Reproduction python copierline.py --date 2026-08-11 --processed <extracted processed forecast sets> python figures.py --blob copierline.2026-08-11.json Analysis code at [author repository].~~

> **Reproduction python copierline.py --date 2026-08-11 --processed <extracted processed forecast sets> python figures.py --blob copierline.2026-08-11.json Analysis code and derived data: https://github.com/OJdominus/forecastbench-copier-line Inputs, all public: git clone https://github.com/forecastingresearch/forecastbench-datasets.git git clone https://github.com/forecastingresearch/forecastbench.git curl -O https://www.forecastbench.org/assets/data/processed-forecast-sets/processedforecastsets.tar.gz https://forecastbench.org/assets/data/question-fixed-effects/questionfixedeffects.YYYY-MM-DD.{tournament,baseline}leaderboard.json Leaderboard history requires a full clone.**

**39.**

> ~~Scoring rule at src/leaderboard/main.py, lines 2348, 2610, 2954, and 2985.~~

> **Scoring rule at src/leaderboard/main.py, lines 2348, 2610, 2954, 2985.**

**40.**

> ~~Data: forecastingresearch/forecastbench-datasets, CC BY-SA 4.0, plus processed forecast sets and question fixed-effects files from forecastbench.org.~~

> **Data: forecastingresearch/forecastbench-datasets, CC BY-SA 4.0, plus processed forecast sets and question fixed-effects files from forecastbench.org. --- Four hundred and forty-two forecasters out of 527 scored worse than the price they were shown.**

### Added

**1.** Of those with enough resolved market questions to test, 442 scored worse than the market price provided to them, and none can be shown to have beaten it once you account for having run 527 tests at once.

**2.** Two come closest, and they are the two the argument was already about.

**3.** Every entry's Brier score minus the market's Brier score on the same questions, with 95% bootstrap intervals.

**4.** This is the benchmark's own difficulty-adjusted market score.

**5.** Two intervals lie entirely below the line.

**6.** On that reading it is a significant result that an AI system beat superforecasters on those questions.

**7.** Tldr Of 527 entries, 442 score significantly below the market price at a 5% false discovery rate across all 527 tests.

**8.** Zero entries survive the same correction in the other direction.

**9.** Two clear an uncorrected test, and they are the two that clear it:

**10.** Both were named in advance by other people, which is why it is fair to read them uncorrected.

**11.** The second test carries a cost the first does not.

**12.** Running it once per entry means running it 527 times, and a two-sided 95% interval falls entirely below zero 2.5% of the time when the true edge is exactly zero.

**13.** Of the 527, 437 are significantly below the market on the uncorrected test, so their true effect is not near zero.

**14.** That leaves 90 whose edge could plausibly be nothing.

**15.** If none of those 90 had any edge at all, chance alone would put 2.2 of them below the line.

**16.** Benjamini-Hochberg at a 5% false discovery rate returns zero discoveries in that direction and 442 in the other.

**17.** So the honest reading is that no entry on this board demonstrably beats the price it was shown, and the great majority demonstrably lose to it.

**18.** Cassi and the superforecasters stay interesting for a different reason.

**19.** They were not selected by this search.

**20.** FRI's July post named Cassi.

**21.** Good Judgment's reply named the superforecasters.

**22.** Testing those two is a hypothesis someone else registered three weeks in advance, and on that basis their exact bootstrap p-values of 0.004 and 0.017 are worth reporting.

**23.** They are also the only two that come close: the next strongest sits at 0.035, and nothing else clears 0.05.

**24.** Two prices give two lines.

**25.** Scoring against a reference forecast is old.

**26.** The Brier Skill Score does it, Metaculus's Peer Score does it, and FRI's own addendum evaluates both as alternatives before selecting the difficulty- adjusted Brier.

**27.** The point here is narrower: setting the market weight to 1 makes the published market column a skill score against the market price already, and the zero point that implies has never been drawn.

**28.** Thirty ForecastBench baseline runs, 2,916 matched question pairs, same model and same questions in both conditions.

**29.** The two medians in the table differ by 16.55, which is a slightly larger number because the median of the paired differences is not the difference of the medians.

**30.** The paired figure is the right one for a design where every run appears in both columns.

**31.** Adjusted score by how far the market price sat from 0.5.

**32.** Bins are formed on the price, which is observable in advance, never on the outcome.

**33.** The mechanism is real and sizeable.

**34.** The human question mix happens not to exploit it.

**35.** Nine Things This Doesn't Cover The board carries 527 simultaneous tests, so some entries clear a 95% bar by chance.

**36.** Zero survive a 5% false discovery rate in the beats-the-market direction and 442 survive it in the other.

**37.** Cassi and the superforecasters are reported uncorrected because both were named publicly before this analysis existed.

**38.** Bonferroni cannot be assessed here: with 2,000 resamples the smallest achievable p is 0.0005, above the 0.000095 threshold.

**39.** None can be shown to have beaten it.

### Removed

**1.** ~~With enough resolved market questions to test, only two beat the market price provided to them.~~

**2.** ~~Of 527 entries, 2 beat the market price at 95% confidence, 88 are indistinguishable from it, and 437 score below it.~~

**3.** ~~The general public median sits significantly below the market at +0.0200.~~

**4.** ~~Two different nulls Figure 1.~~

**5.** ~~Every entry's Brier score minus the market's Brier score on the same questions, with 95% bootstrap intervals.~~

**6.** ~~This is the benchmark's own difficulty-adjusted market score.~~

**7.** ~~Two intervals sit entirely below zero.~~

**8.** ~~Cassi and the superforecasters perform similarly to each other, and both outperform the market.~~

**9.** ~~The other systems do not show a statistically significant advantage over the market.~~

**10.** ~~So market questions constitute 50% of the questions in each round.~~

**11.** ~~There are three separate scoring boards.~~

**12.** ~~This is also the board used in the parity comparison.~~

**13.** ~~What the Freeze Value Buys Figure 2.~~

**14.** ~~Thirty ForecastBench baseline runs, 2,916 matched question pairs, same model, and same questions in both conditions.~~

**15.** ~~Adjusted score by how far the market price sat from 0.5.~~

**16.** ~~Bins are formed on the price, which is observable in advance, never on the outcome.~~

**17.** ~~Inputs, all public: git clone https://github.com/forecastingresearch/forecastbench-datasets.git git clone https://github.com/forecastingresearch/forecastbench.git curl -O https://www.forecastbench.org/assets/data/processed-forecast-sets/processedforecastsets.t ar.gz https://forecastbench.org/assets/data/question-fixed-effects/questionfixedeffects.YYYY-MM- DD.{tournament,baseline}leaderboard.json Leaderboard history requires a full clone.~~


---

## X article: your document to X_ARTICLE_v2

*15 sentences rewritten, 24 added, 5 removed.*

### Rewritten

**1.**

> ~~Introduction In July this year, the Forecasting Research Institute (FRI) released a report that claims AI models are performing at the same level with superforecasters on ForecastBench.~~

> **What ForecastBench's Market Scores Actually Measure Introduction In July this year, the Forecasting Research Institute (FRI) released a report that claims AI models are performing at the same level with superforecasters on ForecastBench.**

**2.**

> ~~Now, market questions are a better test of human-like forecasting skill, as they often require judgment about novel, one-off events; this was why it was a huge deal that an AI system beat superforecasters on those questions.~~

> **FRI argues that market questions are the better test of human-like forecasting skill, as they often require judgment about novel, one-off events.**

**3.**

> ~~Three weeks later, Good Judgement countered with a response.~~

> **Three weeks later, Good Judgment countered with a response.**

**4.**

> ~~When ForecastBench asks a forecaster about a prediction market, the market price (the crowd's prediction) sits right there in the question.~~

> **When ForecastBench asks a forecaster about a prediction market, the market price, which is the crowd's prediction, sits right there in the question.**

**5.**

> ~~Will this person still hold office next year? etc They put those questions to AI systems, and they have also put them to a panel of thirty-nine people known as superforecasters.~~

> **They put those questions to AI systems, and they have also put them to a panel of thirty-nine people known as superforecasters.**

**6.**

> ~~Findings I pulled every forecast in the system: 423,000 of them, from 527 different entries, going back to the start.~~

> **Findings I pulled every forecast in the system: 423,396 of them, across 572 entries, going back to the start. 527 of those entries had enough resolved market questions to test.**

**7.**

> ~~Out of 527 entries, 437 of them did worse than the price they were shown, 88 could not be distinguished from it, and only 2 beat the market price.~~

> **Out of 527 entries, 437 of them did worse than the price they were shown, 88 could not be distinguished from it, and 2 beat it.**

**8.**

> ~~The two entries that beat the market price are an AI system called Cassi and the superforecaster panel.~~

> **The two that come closest are an AI system called Cassi and the superforecaster panel.**

**9.**

> ~~The FRI's July post was specifically about Cassi ranking above the humans on market questions for the first time, while Good Judgment's rebuttal was specifically defending the humans against that claim.~~

> **FRI's July post was specifically about Cassi ranking above the humans on market questions for the first time, while Good Judgment's rebuttal was specifically defending the humans against that claim.**

**10.**

> ~~Turns out both sides were right about their claims.~~

> **Turns out both sides were right about their own claim.**

**11.**

> ~~Conclusion The Forecast Research Institute was right, and Good Judgment's numbers were accurate on the day they published them.~~

> **Conclusion The Forecasting Research Institute was right, and Good Judgment's numbers were accurate on the day they published them.**

**12.**

> ~~Reading comprehension tests hand it to the passage.~~

> **Reading comprehension tests hand it the passage.**

**13.**

> ~~Medical benchmarks hand it to the clinical guideline.~~

> **Medical benchmarks hand it the clinical guideline.**

**14.**

> ~~I did not show that AI cannot forecast; what I have shown is that on one specific benchmark, on one specific kind of question, the published score measures something narrower than people think it measures, and that by that narrower measure almost nothing on the board is adding information.~~

> **What I have shown is that on one specific benchmark, on one specific kind of question, the published score measures something narrower than people think it measures, and that by that narrower measure nothing on the board is demonstrably adding information.**

**15.**

> ~~The AI model that cleared the bar cleared it by a wider margin than the humans did.~~

> **The AI model that came closest came closer than the humans did.**

### Added

**1.** On that reading it was a significant result that an AI system beat superforecasters on those questions.

**2.** Good Judgment is a company that sells superforecasting services, staffed by individuals with a documented track record of predicting world events more accurately than almost anyone else, including intelligence analysts with access to classified material.

**3.** Will this person still hold office next year?

**4.** Scoring against a reference is not a new idea.

**5.** The Brier Skill Score does it, Metaculus's Peer Score does it, and FRI's own methodology paper weighs both before choosing the method it uses.

**6.** What is new here is narrower: on this benchmark the market price is already the reference, whether or not anyone reads the column that way, and nobody has drawn where zero sits.

**7.** Then I corrected for the fact that I had run 527 tests at once.

**8.** This matters, because when you test enough things, some clear a 95% bar by luck alone.

**9.** Of the 527, 437 are clearly below the market, so their true score is not near zero.

**10.** That leaves 90 that could plausibly be sitting at zero.

**11.** If none of those 90 had any real edge, chance alone would put 2.2 of them below the line.

**12.** Running the standard correction, a 5% false discovery rate across all 527, gives zero entries that demonstrably beat the market and 442 that demonstrably lose to it.

**13.** So the honest version is this.

**14.** Nobody on that board can be shown to beat the price they were handed.

**15.** Almost everybody can be shown to lose to it.

**16.** Their exact p-values are 0.004 and 0.017, and the next strongest entry is at 0.035 with nothing else clearing 0.05.

**17.** I am reporting those two uncorrected, and I think that is fair, because I did not go looking for them.

**18.** Both sides named their candidate three weeks before I ran anything.

**19.** The superforecasters did something real.

**20.** And the argument between them was being fought over the only two entries on the board that come anywhere near the price both were shown.

**21.** The two agree to one part in ten thousand.

**22.** I did not show that AI cannot forecast.

**23.** My own reading is that it is a matter of when rather than if AI beats humans at forecasting, though I should say plainly that the data here does not establish that.

**24.** It shows two candidates and no confirmed winner. --- Full write-up, analysis code, and all derived data: https://github.com/OJdominus/forecastbench-copier-line

### Removed

**1.** ~~Are AI Forecasters Actually Better Than Superforecasters?~~

**2.** ~~But the wrong headline still went viral.~~

**3.** ~~Good Judgement is a company that sells superforecasting services.~~

**4.** ~~The best in the space and made of individuals with a documented track record of predicting world events more accurately than almost anyone else, including intelligence analysts with access to classified material.~~

**5.** ~~And it might be a matter of when, not if, AI can actually beat humans at forecasting~~
