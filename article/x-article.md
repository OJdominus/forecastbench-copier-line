# What ForecastBench's Market Scores Actually Measure

## Introduction

In July this year, the Forecasting Research Institute (FRI) released a report that claims AI models
are performing at the same level with superforecasters on ForecastBench. FRI was careful about it.
They said the confidence intervals overlapped and the result was more consistent with the two being
equal than with AI being better, and they listed all their limitations plainly.

The headline still travelled. In the second heading of its report, they went further to identify an
AI system that ranked above superforecasters on market questions for the first time. And this was
the headline everyone picked and ran with.

FRI argues that market questions are the better test of human-like forecasting skill, as they often
require judgment about novel, one-off events. On that reading it was a significant result that an AI
system beat superforecasters on those questions.

Three weeks later, Good Judgment countered with a response. Good Judgment is a company that sells
superforecasting services, staffed by individuals with a documented track record of predicting world
events more accurately than almost anyone else, including intelligence analysts with access to
classified material. Their argument was that the human scores came from a single session held in
July 2024 and that comparing a continuously improving machine against a two-year-old snapshot of a
human is not a fair race.

But more importantly, they pointed out that in FRI's work, one model prediction had a 0.994
correlation with the market prices it was shown. Meaning that the AI models might not be forecasting
independently but instead copying market prices and making adjustments.

When ForecastBench asks a forecaster about a prediction market, the market price, which is the
crowd's prediction, sits right there in the question. So when a system scores well on market
questions, there are two possible explanations. Either it worked out something the crowd had missed.
Or it looked at the number it was handed and repeated it back with extra steps.

Good Judgment pointed this out. Their exact words: "whether the top systems are forecasting
independently or aggregating market prices with extra steps remains entirely unexplored."

That sentence, an open question, published three weeks ago, is what I investigated in this piece.

## Understanding the ForecastBench Benchmark

Every two weeks FRI collects 500 questions about things that have not happened yet. Will inflation
be above this level by December? Will this conflict still be running in March? Will this person still
hold office next year? They put those questions to AI systems, and they have also put them to a panel
of thirty-nine people known as superforecasters.

These are ordinary people who make exceptionally accurate predictions about future world events. The
term came from a massive research tournament called the Good Judgment Project, led by Philip Tetlock
and Barbara Mellers. They often beat traditional experts and intelligence analysts.

After the questions are resolved, they score them all. The scores go on a public leaderboard with
hundreds of entries. AI systems from Google, from xAI, and from small startups, alongside the human
panel.

ForecastBench asks two kinds of questions, and it scores them separately. The first kind comes out
of a database. Will the temperature in this city exceed this value? Will this stock close above that
price? These are the questions where a machine has an obvious advantage, because the work is mostly
looking things up and doing arithmetic on the past.

The second kind comes from prediction markets: Infer, Metaculus, Polymarket, and Manifold. And this
is the most interesting kind. They test AI models and humans on real-world geopolitics, economics,
and emerging risks.

To be fair across questions, ForecastBench adjusts for difficulty. A hard question should count for
more than an easy one. For market questions, they decided that the difficulty of a question is
exactly how badly the market price did on it. If the crowd got it right, the question was easy. If
the crowd got it wrong, the question was hard.

That is a defensible choice, as they wanted a system where a forecaster can only rank above the
market by genuinely beating it. But it bore a non-obvious consequence.

If difficulty is defined as the market's error, then your score is your error minus the market's
error. Which means the market questions column is not measuring how good you are at forecasting. It
is measuring how much you added to the price you were already shown.

And that means there is a specific score you get for adding nothing at all. For taking the number
you were handed and handing it straight back. I call it the "copier line." On the day I ran the
numbers, it sat at just under seventy-one out of a hundred.

Scoring against a reference is not a new idea. The Brier Skill Score does it, Metaculus's Peer Score
does it, and FRI's own methodology paper weighs both before choosing the method it uses. What is new
here is narrower: on this benchmark the market price is already the reference, whether or not anyone
reads the column that way, and nobody has drawn where zero sits.

A note on process. I sent this to FRI before publishing. They couldn't review it in full and didn't
want to hold up my timeline, but they did answer one thing I had flagged as unresolved: why the
tournament and baseline leaderboards estimate market-question difficulty differently. Tournament
models get tools and scaffolding, so scoring them against the market price is the right reference.
Baseline models are handicapped there, so those questions use two-way fixed effects instead. They
also said they plan to retire the baseline board. Nothing else here has been checked by them.

## Findings

I pulled every forecast in the system: 423,396 of them, across 572 entries, going back to the start.
527 of those entries had enough resolved market questions to test.

For each entry I asked one question. Over all the market questions it answered, did it do better
than the price it was shown by enough that we can be confident it was not luck?

I used a standard statistical method for this. You take an entry's questions, draw a random sample
of them with replacement, recompute the average, and do that two thousand times. That gives you a
range. If the whole range sits on the better side of zero, the result holds up. If the range
straddles zero, you cannot tell it apart from chance.

**I.** Out of 527 entries, 437 of them did worse than the price they were shown, 88 could not be
distinguished from it, and 2 beat it.

Then I corrected for the fact that I had run 527 tests at once. This matters, because when you test
enough things, some clear a 95% bar by luck alone. Of the 527, 437 are clearly below the market, so
their true score is not near zero. That leaves 90 that could plausibly be sitting at zero. **If none
of those 90 had any real edge, chance alone would put 2.2 of them below the line. Two are there.**

Running the standard correction, a 5% false discovery rate across all 527, gives zero entries that
demonstrably beat the market and 442 that demonstrably lose to it.

So the honest version is this. Nobody on that board can be shown to beat the price they were handed.
Almost everybody can be shown to lose to it.

**II.** The two that come closest are an AI system called Cassi and the superforecaster panel. Their
exact p-values are 0.004 and 0.017, and the next strongest entry is at 0.035 with nothing else
clearing 0.05.

I am reporting those two uncorrected, and I think that is fair, because I did not go looking for
them. FRI's July post was specifically about Cassi ranking above the humans on market questions for
the first time, while Good Judgment's rebuttal was specifically defending the humans against that
claim. Both sides named their candidate three weeks before I ran anything.

Turns out both sides were right about their own claim. Cassi did something real. The superforecasters
did something real. And the argument between them was being fought over the only two entries on the
board that come anywhere near the price both were shown.

**III.** Another finding was that the panel of ordinary members of the public, the control group in
the original study, scored significantly worse than the market price they were shown. Being handed a
good answer and then adjusting it made them worse off.

**IV.** The superforecasters made their predictions once, in July 2024. They have not made any since.
Their answers are frozen. The questions they answered have resolved, so the facts are frozen too.
But between April and August of this year, their published score fell by nearly five points.

I worked out why. The scoring system rescales everyone's number against the average difficulty of the
whole question pool, and the pool has been getting harder. When the pool gets harder, the anchor
moves, and every score moves with it. Anyone whose performance is frozen absorbs the whole adjustment.

Checked this two ways that do not depend on each other: worked the anchor backwards out of the
published leaderboard and measured it directly from a separate file the Institute publishes every day.
The two agree to one part in ten thousand.

So when Good Judgment quoted the score gap in April, they were quoting it correctly. And by August
the same leaderboard, untouched, had reversed the ordering.

In conclusion, the number people are arguing about is not stable enough to argue about.

## Conclusion

The Forecasting Research Institute was right, and Good Judgment's numbers were accurate on the day
they published them.

However, what is missing is one line on a chart. Publish the copier line. The score you would get for
handing back the price you were shown. Their own code already computes everything needed for it.
Drawing it would let anyone reading that leaderboard see at a glance which entries are contributing
something and which are relaying a number.

And there is a bigger version of this, which is why I think the work matters beyond one benchmark.

Almost every modern AI evaluation hands the system something useful before asking it to perform.
Reading comprehension tests hand it the passage. Coding benchmarks hand it the tools and often the
hints. Medical benchmarks hand it the clinical guideline. In every one of those cases there is a
score for simply reproducing what you were given, and in almost none of them is that score published.

So the leaderboard says 84 out of 100, and it feels like a lot, and nobody has mentioned that
repeating the input back scores 81.

Additionally, I want to be careful about what is shown here. I did not show that AI cannot forecast.
What I have shown is that on one specific benchmark, on one specific kind of question, the published
score measures something narrower than people think it measures, and that by that narrower measure
nothing on the board is demonstrably adding information.

I also think humans are not safe. The AI model that came closest came closer than the humans did.
My own reading is that it is a matter of when rather than if AI beats humans at forecasting, though I
should say plainly that the data here does not establish that. It shows two candidates and no
confirmed winner.

---

*Full write-up, analysis code, and all derived data:
https://github.com/OJdominus/forecastbench-copier-line*
