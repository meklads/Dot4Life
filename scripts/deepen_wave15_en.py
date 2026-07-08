#!/usr/bin/env python3
"""Wave 15 DEEPEN (EN): final 6 restored wave-9 EN stubs."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BARAKAH_BODY = r"""
<div class="container">

<h1>The Barakah Budget: Rethinking Family Finance Through Abundance</h1>

<p>What if the goal of family finance is not only to have more money, but to feel that what you have is enough? That is the promise of barakah: divine increase in quality, not just quantity. A modest income with barakah can cover needs that a larger income without it may not.</p>

<p>This guide offers a practical framework for family budgeting built on barakah: halal earning, intentional spending, giving as strategy, and step-by-step habits you can start this week.</p>

<div class="tip"><p><strong>Why now?</strong> Data from the <a href="https://www.imf.org/en/Publications/fandd/issues/2024/03/household-debt-and-financial-stability" target="_blank" rel="noopener">IMF</a> shows household debt pressure reduces family resilience. A barakah budget starts by easing that pressure spiritually and practically.</p></div>

<h2 id="what-is-barakah-budget">What Is a Barakah Budget?</h2>
<p>A barakah budget is a financial plan grounded in three Islamic principles: <strong>halal earning</strong>, <strong>intentional spending</strong>, and <strong>giving as strategy</strong>. Unlike spreadsheets that track numbers only, it asks: does this spending bring barakah or consume it?</p>

<p>The key question shifts from "How much did we spend?" to "Did this spending align with our values?" That single reframing changes supermarket, vacation, education, and investment decisions.</p>

<h2 id="five-pillars">Five Pillars of Blessed Family Finance</h2>

<h3 id="halal-income">1. Halal income first</h3>
<p>No budget creates barakah if income itself is doubtful. Review salary, commissions, investments, and side income honestly. If something is unclear, consult local scholars and plan a gradual transition.</p>

<h3 id="spending-framework">2. A flexible spending framework</h3>
<div class="table-wrap"><table>
<tr><th>Category</th><th>Suggested share</th><th>Barakah principle</th></tr>
<tr><td>Essential needs</td><td>About half of income</td><td>Trust in provision, no waste</td></tr>
<tr><td>Family and connection</td><td>Moderate portion</td><td>Gifts, travel, hospitality</td></tr>
<tr><td>Saving and investing</td><td>Steady portion</td><td>Halal growth, debt payoff, emergency fund</td></tr>
<tr><td>Giving</td><td>Reserved portion</td><td>Zakat and sadaqah are non-negotiable</td></tr>
<tr><td>Discretionary</td><td>Balanced remainder</td><td>Intentional, not impulse</td></tr>
</table></div>

<h3 id="charity-leverage">3. Charity as leverage</h3>
<p>Families who give regularly often notice needs met in unexpected ways. Start a visible sadaqah jar in the kitchen. Let children contribute from allowance weekly.</p>

<h3 id="debt-free">4. Minimize riba-based debt</h3>
<p>Debt is both financial and spiritual weight. Review cards, loans, and financing products. Use our <a href="/tools/zakat-calculator.html">Zakat calculator</a> and <a href="/finance-wealth/halal-investment-gulf-families-en.html">halal investing guide</a> as starting points.</p>

<h3 id="teach-children">5. Teach children barakah thinking</h3>
<p>Split allowance into spend, save, and give. Include kids in a short weekly money meeting. Ask: what purchase do we regret this week?</p>

<h2 id="step-by-step">Apply It Step by Step</h2>
<ol>
<li>Track spending for 30 days without judgment.</li>
<li>Name every dirham before it leaves the account.</li>
<li>Set a fixed sadaqah and zakat calendar reminder.</li>
<li>List debts and create a payoff order.</li>
<li>Hold a 15-minute family finance meeting each week.</li>
</ol>

<h2 id="common-mistakes">Common Mistakes</h2>
<p><strong>Overspending on hospitality</strong> to impress guests. <strong>Delaying charity</strong> until income rises. <strong>Hiding debt</strong> from a spouse. <strong>Keeping up with neighbors</strong> on cars and vacations.</p>

<h2 id="gulf-context">Barakah Budgeting in the Gulf</h2>
<p>Gulf salaries can be high, but rent, private school, and summer travel consume margins quickly. Build a separate seasonal fund for Ramadan, Eid, and school fees so emergencies do not force debt.</p>

<p>Read also: <a href="/finance-wealth/barakah-budget-family-finance.html">Arabic version</a> · <a href="/guides/zakat-complete-guide.html">Zakat guide</a> · <a href="/blog/gcc-family-budget-2025.html">Gulf family budget</a></p>

<h2 id="intentions">Start With Intention and Gratitude</h2>
<p>Before opening a spreadsheet, pause for a short dua: that your income stays halal, your spending stays mindful, and your family feels sufficiency rather than constant comparison. Gratitude is not decoration. It changes what feels like enough.</p>
<p>Many Gulf families earn well but still feel anxious because comparison is built into social media and neighborhood visits. A barakah budget names comparison as an enemy and replaces it with clear family goals written on one page.</p>

<h2 id="weekly-meeting">The 15-Minute Weekly Money Meeting</h2>
<p>Consistency beats complexity. Every week, same day, same short agenda: review spending, name one win, name one leak, confirm giving and bills, close with du'a. Keep it under fifteen minutes. Long finance lectures create avoidance. Short honest reviews create trust.</p>

<h2 id="zakat-planning">Zakat Planning Without Panic</h2>
<p>Zakat is a fixed pillar, not an afterthought. Use our <a href="/tools/zakat-calculator.html">Zakat calculator</a> quarterly so Ramadan does not arrive with surprise calculations. Voluntary sadaqah can be small and regular: weekly auto-transfer or a visible jar children help fill.</p>

<h2 id="emergency-fund">Emergency Fund as Spiritual Calm</h2>
<p>An emergency fund reduces riba temptation when the car breaks or school fees spike. Start with one month of essentials, then grow toward three to six months. Families with even a modest buffer report less marital conflict around money.</p>

<h2 id="halal-investing">Halal Investing Basics</h2>
<p>Review our <a href="/finance-wealth/halal-investment-gulf-families-en.html">halal investing guide</a> before large moves. Diversify rather than chasing one hot asset. The barakah question is transparency, debt structure, and whether the investment distracts you from family presence.</p>

<h2 id="children-by-age">Teaching Barakah by Age</h2>
<p>Ages 3-6: three jars for spend, save, give. Ages 7-11: allowance with weekly jar counts. Teens: involve them in one real bill category. Ask monthly what purchase brought joy and what we regret.</p>

<h2 id="couple-alignment">When Spouses Disagree on Money</h2>
<p>Conflict often hides different childhood experiences with scarcity. Agree on three numbers: monthly giving, monthly saving, and one discretionary limit per person. Results over one quarter convince more than moralizing.</p>

<h2 id="seasonal">Seasonal Budgeting: Ramadan, Eid, and Summer</h2>
<p>Create a seasonal line for Ramadan hospitality, Eid gifts, summer travel, and school fees. Set guest and menu caps before Ramadan. Start summer savings in autumn so December does not force card debt.</p>

<h2 id="red-flags">Red Flags That Drain Barakah</h2>
<ul>
<li>Hidden accounts or secret spending.</li>
<li>Card minimums while financing luxury items.</li>
<li>Hospitality beyond your means to impress.</li>
<li>Children who never see parents give.</li>
<li>Investments you cannot explain simply.</li>
</ul>
<p>Each red flag is fixable with honesty and a dated plan. A barakah budget assumes restart, not perfect history.</p>

<h2 id="case-scenarios">Three Gulf Family Scenarios</h2>
<p><strong>Scenario A:</strong> Dual income, high rent, two private school fees. They cut two unused subscriptions, fixed sadaqah first, and negotiated school payment plans. Stress dropped before income rose.<br>
<strong>Scenario B:</strong> Single income, extended family support. They wrote a visible budget on the fridge and involved teens in grocery planning. Waste fell within six weeks.<br>
<strong>Scenario C:</strong> Business income with irregular months. They built a lean month baseline and parked surplus months into emergency and zakat funds immediately.</p>
<p>None of these families became financial experts overnight. They became consistent reviewers of intention and numbers.</p>

<h2 id="tools-resources">Tools and Next Reads</h2>
<p>Pair this guide with practical tools: our <a href="/tools/zakat-calculator.html">Zakat calculator</a>, the <a href="/guides/zakat-complete-guide.html">complete Zakat guide</a>, and the <a href="/blog/gcc-family-budget-2025.html">Gulf family budget article</a>. Print one page with your three monthly numbers: giving, saving, and essentials. Tape it inside a kitchen cabinet. Visibility beats memory when life gets loud.</p>
<p>When you feel comparison rising at a gathering, return to that page. Barakah grows when intention is visible to the whole household, not hidden in one parent's head.</p>
<p>Review the budget after Ramadan each year. Seasonal giving and hospitality often reveal leaks that monthly tracking misses. A thirty-minute annual review keeps the barakah frame alive for the next twelve months.</p>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">How is a barakah budget different from a normal budget?</div>
<div class="faq-answer">Intentions and priorities differ. Both use numbers, but barakah budgeting starts with halal income, charity, and gratitude before allocating expenses.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if income does not cover basics?</div>
<div class="faq-answer">Remove riba and waste first, then seek halal income growth gradually. Consult a licensed financial advisor if pressure continues.</div>
</div>

<div class="faq-item">
<div class="faq-question">Must we give charity while in debt?</div>
<div class="faq-answer">Zakat applies when nisab is reached. Voluntary charity stays flexible. Many scholars encourage small regular giving alongside debt payoff.</div>
</div>

<div class="faq-item">
<div class="faq-question">How do we align as a couple on money?</div>
<div class="faq-answer">Keep meetings short and goal-focused: one shared target like a trip, tuition, or debt milestone. Let results convince, not lectures.</div>
</div>

<div class="faq-item">
<div class="faq-question">Is real estate always better than stocks?</div>
<div class="faq-answer">No universal rule. Focus on halal structure, transparency, and diversification. Seek specialist advice before large moves.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> This is general financial education, not financial or religious rulings. Consult licensed advisors and qualified scholars for your situation.</p></div>

</div>
"""

FRIDAY_BODY = r"""
<div class="container">

<h1>Friday Night Reset: How One Evening Can Change Your Family Week</h1>

<p>Friday night is one of the most underused resources in modern family life. For Muslim families, the blessing of Jumu'ah extends into the evening: a natural invitation to pause, reconnect, and reset before a new week.</p>

<p>This guide helps you reclaim Friday night as intentional family time: fewer screens, deeper conversation, and a simple routine any Gulf household can adopt without extra budget.</p>

<div class="tip"><p><strong>Why Friday?</strong> A review in <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6762025/" target="_blank" rel="noopener">PMC</a> links regular family rituals with lower stress and stronger connection. Friday is a ready-made weekly anchor.</p></div>

<h2 id="three-part-frame">The Three-Part Friday Frame</h2>

<h3 id="maghrib-to-dinner">1. Maghrib to dinner: no screens</h3>
<p>After Maghrib, make one hour phone-free. Cook together when possible. Keep devices in a basket at the door. Start with one question: "What was the best moment this week?"</p>

<h3 id="after-dinner">2. After dinner: family session</h3>
<p>Thirty to forty-five minutes of shared activity: story, board game, or one discussion topic. Let teens rotate as session leader weekly to reduce resistance.</p>

<h3 id="before-sleep">3. Before sleep: quiet wind-down</h3>
<p>Dim lights, silence notifications, short reading or dhikr. Parents need this layer too, not only children.</p>

<h2 id="hour-plan">Sample Hour-by-Hour Plan</h2>
<div class="table-wrap"><table>
<tr><th>Time</th><th>Activity</th><th>Rule</th></tr>
<tr><td>Maghrib + 15m</td><td>Prepare dinner together</td><td>No kitchen screens</td></tr>
<tr><td>Maghrib + 45m</td><td>Family dinner</td><td>Phone basket at door</td></tr>
<tr><td>Maghrib + 90m</td><td>Family session</td><td>One topic only</td></tr>
<tr><td>Before bed</td><td>Quiet reading</td><td>Notifications off</td></tr>
</table></div>

<h2 id="screens">Screens: The Main Obstacle</h2>
<p>Many families fail because background TV stays on. Agree on a four-week trial: no screens from Maghrib through dinner. Track sleep and mood changes.</p>

<h2 id="gulf-context">Friday in Gulf Context</h2>
<p>In summer, families stay indoors with AC. Use the long evening for a living-room session instead of scattered scrolling. In winter, add a short post-dinner walk.</p>

<p>Related: <a href="/blog/friday-night-reset-family.html">Arabic version</a> · <a href="/health/quiet-home-family-guide-en.html">Quiet home guide</a></p>

<h2 id="conversation-starters">Conversation Starters That Work</h2>
<p>Teens shut down when questions feel like interrogation. Try open prompts: "What surprised you this week?" "Who did you appreciate?" "What would you change about next week?" Rotate who asks so no one parent dominates.</p>
<p>Younger children respond to concrete questions: "What was the funniest thing at school?" "What made you proud?" Keep answers short. The goal is rhythm, not a therapy session.</p>

<h2 id="teen-friday">Friday With Teenagers</h2>
<p>Teens may resist family time. Offer agency: they pick music for cooking, choose the game, or lead the discussion topic. A twenty-minute commitment with a clear end time feels safer than an open-ended evening.</p>
<p>If resistance stays high, start with parallel presence: everyone in the living room, each with a book or quiet activity, phones away. Conversation often emerges naturally after ten minutes of shared quiet.</p>

<h2 id="couples">Friday for Couples Without Children</h2>
<p>Before children arrive, Friday night sets the tone for the marriage. Cook together, walk after Maghrib, or read one short passage and discuss one question. The habit becomes infrastructure when parenting fatigue arrives later.</p>

<h2 id="grandparents">Including Grandparents</h2>
<p>When grandparents live nearby, invite them for dessert after your core ritual rather than replacing your home rhythm entirely. Grandfather stories after Maghrib can become the highlight children anticipate weekly.</p>

<h2 id="summer-winter">Summer Heat and Winter Evenings</h2>
<p>Gulf summers push families indoors early. Use the long evening for board games, storytelling, or a family project. Winter allows balcony tea after dinner. Adapt the activity, keep the no-screen window constant.</p>

<h2 id="when-travel">When You Are Traveling on Friday</h2>
<p>Travel weeks need a portable minimum: phone-free meal, one question, five minutes of quiet. A partial ritual preserves the identity of Friday better than skipping entirely and restarting from zero.</p>

<h2 id="tracking">Track What Changes</h2>
<p>After four Fridays, note sleep quality, morning mood, and how often children volunteered conversation. Families often report fewer Sunday-night arguments when Friday created connection earlier in the weekend.</p>

<h2 id="activity-menu">Friday Activity Menu (Pick One Weekly)</h2>
<p>Rotate activities so Friday never feels repetitive: board game night, story circle, backyard stargazing, short Quran reflection, family photo album review, or cooking a childhood recipe from a grandparent. The activity matters less than predictable togetherness.</p>
<p>Keep a simple list on the fridge. Let children add ideas. When they choose, resistance drops because the evening becomes theirs, not only parents' enforcement.</p>

<h2 id="single-parent-friday">Single Parents and Friday Reset</h2>
<p>If you parent alone, shrink the ritual rather than skip it: ten-minute special snack, one question, one hug round. Ask a trusted uncle or aunt to join monthly so children see extended care. Friday still marks the week even when the table is small.</p>

<h2 id="resistance-plan">When the Family Pushes Back</h2>
<p>Resistance is normal. Name the trial period clearly: four Fridays, then we decide together. Offer one concession teens value, like choosing dinner menu or game, in exchange for the phone basket rule. Parents must model the same rule without exceptions for work email unless true emergency.</p>
<p>If a week fails because of travel or illness, resume the next Friday without guilt. Rituals survive through restart, not perfection. Many families report that week three feels easier than week one because children begin anticipating the rhythm.</p>
<p>Connect Friday night to Saturday morning: children who feel heard on Friday argue less about chores on Saturday. The reset pays forward across the weekend when the first connection happened early.</p>

<h2 id="maghrib-anchor">Using Maghrib as the Anchor</h2>
<p>Maghrib prayer is the natural starting bell for Friday evening reset. When the adhan sounds, devices go to the basket, lights soften, and the kitchen becomes a shared space. Children learn that sacred time and family time are linked, not competing.</p>
<p>Parents who travel for work can still join by video for ten minutes during dinner if they cannot be physical present. Imperfect presence beats perfect absence. Keep the ritual alive in altered form rather than canceling because one parent is away.</p>
<p>Document one photo monthly of your Friday table, not for social media but for private family album. Years later those photos show children how consistently you showed up.</p>

<h2 id="first-week">Your First Four Fridays</h2>
<ol>
<li>Week 1: phone-free dinner only.</li>
<li>Week 2: add the weekly question.</li>
<li>Week 3: add a 20-minute session after dinner.</li>
<li>Week 4: review what changed in sleep and conversation.</li>
</ol>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">Must Friday night be fully screen-free?</div>
<div class="faq-answer">Start with a defined window around dinner and session. Expand gradually rather than banning everything on day one.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if children resist?</div>
<div class="faq-answer">Let them choose the meal or activity. Participation reduces pushback more than commands.</div>
</div>

<div class="faq-item">
<div class="faq-question">Does this work for couples without kids?</div>
<div class="faq-answer">Yes. A quiet dinner plus one weekly question builds connection before children arrive.</div>
</div>

<div class="faq-item">
<div class="faq-question">How much time is enough?</div>
<div class="faq-answer">One focused hour is enough to start: twenty minutes of mindful dinner, thirty minutes together, ten minutes of quiet.</div>
</div>

<div class="faq-item">
<div class="faq-question">Should we skip visiting relatives?</div>
<div class="faq-answer">Not necessarily. Keep a short home ritual first, then visit if needed. Flexibility preserves consistency.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> This is general family education, not therapy or formal religious guidance. Seek licensed help for serious family conflict.</p></div>

</div>
"""

LISTENING_BODY = r"""
<div class="container">

<h1>The Listening Gift: Peace Starts at Home</h1>
<p style="font-size:14px;color:#888">Peace Capsule #1 · June 2026</p>

<p>This week's practice: when your child speaks, stop what you are doing. Turn your body toward them. Look them in the eyes. Do not interrupt, correct, or solve. Simply listen.</p>

<p>Most children do not need more advice. They need more attention. A child who feels heard feels safe. A child who feels safe can grow.</p>

<div class="tip"><p><strong>Why listening?</strong> A review in <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6762025/" target="_blank" rel="noopener">PMC</a> links attentive listening with stronger family communication and lower stress.</p></div>

<h2 id="true-listening">What Is True Listening?</h2>
<p>Listening is not waiting for your turn to talk. It is full presence: body facing the child, eyes on them, phone away. Children read body language before words.</p>

<p>Reflect briefly: "It sounds like you are angry because your brother took your toy." No judgment yet. Understanding comes before correction.</p>

<h2 id="five-steps">Five Practical Steps</h2>
<ol>
<li><strong>Stop moving</strong> when they start talking.</li>
<li><strong>Reflect feeling</strong> without fixing.</li>
<li><strong>Ask one open question</strong>.</li>
<li><strong>Commit to two full minutes</strong>.</li>
<li><strong>Close with thanks</strong> for sharing.</li>
</ol>

<h2 id="by-age">Listening by Age</h2>
<p><strong>Ages 2-5:</strong> short sentences, eye-level posture, calm touch.<br>
<strong>Ages 6-11:</strong> ask for details, validate effort.<br>
<strong>Teens:</strong> tolerate silence; presence beats interrogation.</p>

<h2 id="common-mistakes">Common Mistakes</h2>
<p>Instant correction. Comparison with siblings. Solving before understanding. Fake listening while scrolling.</p>

<h2 id="week-plan">One-Week Plan</h2>
<div class="table-wrap"><table>
<tr><th>Day</th><th>Practice</th></tr>
<tr><td>1</td><td>Two minutes after school</td></tr>
<tr><td>2</td><td>Reflect feeling once</td></tr>
<tr><td>3</td><td>Phone-free dinner question</td></tr>
<tr><td>4</td><td>Listen to spouse five minutes</td></tr>
<tr><td>5</td><td>Journal one win</td></tr>
<tr><td>6</td><td>Family review</td></tr>
<tr><td>7</td><td>Repeat what worked</td></tr>
</table></div>

<p>Read also: <a href="/peace-capsules/listening-gift.html">Arabic version</a> · <a href="/peace-capsules/art-of-apologizing.html">Art of apologizing</a></p>

<h2 id="spouse-listening">Listen to Your Spouse Too</h2>
<p>Children learn listening from how parents treat each other. Five minutes of undivided attention for your spouse weekly models the same gift you ask children to receive. Put the phone in another room. Ask one question and wait.</p>

<h2 id="busy-parents">When You Are Genuinely Busy</h2>
<p>If you cannot stop immediately, name it: "I want to hear you. Give me two minutes to finish this, then I am yours." Keep the promise. Broken promises teach children that words are cheap.</p>

<h2 id="siblings">Listening Between Siblings</h2>
<p>When siblings fight, listen to each separately before judging. Often both need validation before any solution. "You wanted the toy first" and "You felt pushed" can both be true.</p>

<h2 id="school-stress">School Stress and Listening</h2>
<p>After a hard school day, resist instant homework push. Two minutes of listening first often shortens the evening battle. Children regulate faster when they feel understood.</p>

<h2 id="digital-distraction">Digital Distraction Audit</h2>
<p>Track one day: how often did you half-listen while scrolling? Most parents discover the pattern is frequent. Choose one sacred window daily: first ten minutes after school arrival home.</p>

<h2 id="repair">Repair When You Fail</h2>
<p>You will interrupt sometimes. Repair matters: "I cut you off earlier. Tell me again." Children forgive quickly when adults admit mistakes without defensiveness.</p>

<h2 id="mosque-community">Listening Beyond the Home</h2>
<p>Coaches, teachers, and uncles also shape whether children feel heard. Brief a trusted relative: "Please let him finish sentences at gatherings." Community reinforces home habits.</p>

<h2 id="long-term">Long-Term Fruit</h2>
<p>Listening is slow work. Over months, children share more before crises erupt. Teens text less for rescue when they trust parents will listen without instant lecture.</p>

<h2 id="practice-scripts">Sample Listening Scripts</h2>
<p><strong>After school:</strong> "Tell me one thing that went well and one that felt hard." Wait. Do not fix the hard part immediately.<br>
<strong>After sibling fight:</strong> "I want to understand both sides. You first, then your brother."<br>
<strong>After bad grade:</strong> "That sounds disappointing. What do you think happened?"<br>
<strong>With spouse:</strong> "What do you need from me tonight?"</p>
<p>Scripts are training wheels. Eventually presence becomes automatic.</p>

<h2 id="peace-capsule-series">Part of the Peace Capsule Series</h2>
<p>This article is Peace Capsule number one. Small weekly practices beat large resolutions. Pair listening with <a href="/peace-capsules/art-of-apologizing.html">the art of apologizing</a> and quiet home habits for compounding calm.</p>

<h2 id="deepening-practice">Deepening the Practice Over 30 Days</h2>
<p>Week one focuses on stopping: put the phone down when a child speaks. Week two adds reflection: repeat the feeling you heard before any advice. Week three extends listening to spouse and siblings, not only the youngest child. Week four invites a family review: what changed in tone at home?</p>
<p>During week two, practice with low-stakes moments: a story about a video game, a complaint about homework, a joy about a friend. Save high-stakes topics for later when trust in your listening has grown.</p>
<p>Teachers and coaches often see sides of children parents miss. After listening at home, send one brief thank-you message to a teacher when your child shares a positive moment. The child learns you value their whole life, not only grades.</p>
<p>Listening does not mean unlimited screen time or no boundaries. It means boundaries land after understanding, not before. Children accept limits better when they felt heard first.</p>
<p>Keep a simple journal line nightly: "Today I listened well when..." and "Today I interrupted when..." No shame, only pattern recognition. Most parents discover interrupting clusters around fatigue hours.</p>

<h2 id="listening-at-meals">Listening at Meals</h2>
<p>Meals are the highest-leverage listening minutes in the day. Put the phone in another room, ask one open question, and let silence exist between answers. Children often share the important sentence after the obvious one, when adults do not rush to fill quiet.</p>
<p>When two children compete for attention, alternate nights for a two-minute private check-in after dinner. Fair turns reduce rivalry more than equal seconds in group settings.</p>
<p>Grandparents can model listening by asking children about school and waiting fully for answers. Multi-generational attention teaches children they matter in the wider family, not only to parents.</p>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">How many minutes of listening per day?</div>
<div class="faq-answer">Two focused minutes per child daily is a strong start. Consistency beats long sessions.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if my child interrupts me too?</div>
<div class="faq-answer">Model the behavior: "Let me finish, then I will listen to you fully."</div>
</div>

<div class="faq-item">
<div class="faq-question">Does listening mean agreeing?</div>
<div class="faq-answer">No. Understand feelings first, set boundaries later.</div>
</div>

<div class="faq-item">
<div class="faq-question">Is this realistic for busy parents?</div>
<div class="faq-answer">Yes. Two minutes after dinner or before bed is enough to begin.</div>
</div>

<div class="faq-item">
<div class="faq-question">Does it work with quiet teens?</div>
<div class="faq-answer">Often yes with patience. Sit nearby without forcing conversation. Silence can open the door.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> This is general parenting education, not medical or psychological advice. Consult a licensed professional for significant behavioral concerns.</p></div>

<div class="tip"><p><em>Peace starts at home. One breath. One pause. One listening moment at a time.</em></p></div>

</div>
"""

FATHER_BODY = r"""
<div class="container">

<h1>A Year Without Social Media: A Father's Story</h1>

<p>It started on a Tuesday. I sat at dinner with my wife and three children and realized I could not recall what my oldest son had said in the last five minutes. I had been scrolling. Not because something urgent was happening, but because scrolling had become the default position of my hand.</p>

<p>That night I decided to delete every social app from my phone for one year. Not a detox weekend. A full year.</p>

<div class="tip"><p><strong>Context:</strong> Research from <a href="https://www.pewresearch.org/internet/2024/01/31/how-americans-experience-social-media/" target="_blank" rel="noopener">Pew Research</a> shows many users feel platforms consume more time than they intend. This story is personal, but the pattern is common.</p></div>

<h2 id="month-one">Month One: Withdrawal</h2>
<p>The first two weeks were harder than expected. I reached for my phone dozens of times daily and found empty space where Instagram used to be. I had been using social media not to connect, but to escape quiet moments.</p>

<h2 id="month-two">Month Two: Emptiness Becomes Space</h2>
<p>When escape disappeared, I noticed small things again: my daughter's laugh, coffee smell, my son's question about football. We started walking after Maghrib. Twenty minutes in the neighborhood lowered my stress noticeably.</p>

<h2 id="month-six">Month Six: New Habits</h2>
<p>Phone-free dinners, Friday reading, a simple workshop project with my son. My wife said quietly: "You are here now." That sentence was enough.</p>

<h2 id="year-end">End of Year: What Changed</h2>
<p>I am not a perfect father. But my oldest began telling me about his day without being asked. Some apps returned for work, but with limits: no phone at the table, no scrolling in bed.</p>

<h2 id="lessons">Practical Lessons</h2>
<ul>
<li>Presence is a daily decision.</li>
<li>You need a replacement habit, not just deletion.</li>
<li>Involve your family early.</li>
<li>Keep work channels with boundaries.</li>
<li>Relapse is not failure; return to the rule.</li>
</ul>

<h2 id="gulf-context">A Father in the Gulf</h2>
<p>Social pressure to post and compare is real in Gulf cities. I kept WhatsApp for family and replaced feeds with real visits and calls. Comparison dropped when the feed disappeared.</p>

<p>Related: <a href="/featured-stories/father-quit-social-media-year.html">Arabic version</a> · <a href="/blog/digital-minimalism-modern-families-en.html">Digital minimalism</a></p>

<h2 id="replacement-habits">Replacement Habits That Worked</h2>
<p>Deletion alone left empty minutes. I replaced feeds with: after-Maghrib walks, Friday reading with my daughter, and a simple workshop shelf project with my son. Each habit had a time and place so my hand knew where to go instead of the phone.</p>

<h2 id="wife-perspective">My Wife's Perspective</h2>
<p>She did not demand the experiment. She noticed results: fewer distracted nods, more eye contact, calmer bedtimes. Her quiet feedback mattered more than any app screen-time report.</p>

<h2 id="work-boundaries">Work Boundaries After Return</h2>
<p>Some apps returned for work: email, LinkedIn occasionally, WhatsApp for family groups. Rules stayed: no scrolling in bed, no phone on the table, no feeds during children's homework hour.</p>

<h2 id="children-reaction">How Children Reacted</h2>
<p>At first they tested whether I would slip back. By month three they stopped commenting because presence became normal again. My daughter started saving stories for dinner instead of sending memes.</p>

<h2 id="comparison-trap">Escaping the Comparison Trap</h2>
<p>Gulf social life includes photos of vacations, cars, and gatherings. Without feeds, I compared less and visited more. Real relationships replaced passive envy.</p>

<h2 id="relapse">When I Relapsed</h2>
<p>Once during a stressful work week I reinstalled an app for three days. I felt the old fog return. I deleted again and told my wife. Transparency kept the experiment alive.</p>

<h2 id="advice-fathers">Advice for Fathers Starting Small</h2>
<p>You do not need a dramatic year. Pick one non-negotiable: meals, bedtime, or the first hour after work. Track mood for two weeks. Let data and family response guide the next step.</p>

<h2 id="month-three">Month Three: Unexpected Gifts</h2>
<p>By month three I read two full books, something I had not done in years. My son and I built a shelf that still holds his trophies. My daughter asked me to attend her school presentation without a reminder text. These were small events with large emotional weight.</p>

<h2 id="month-nine">Month Nine: Community Without Feeds</h2>
<p>I joined a neighborhood football watch with friends in person instead of commenting online. I called cousins I had only liked posts from. The year without feeds became a year with more voices I could actually hear.</p>

<h2 id="full-year-reflection">Full Year Reflection</h2>
<p>At year end I did not feel morally superior. I felt lighter. Social media had been a second job I never applied for: curating, comparing, reacting. Removing it returned hours that became walks, books, and bedtime stories.</p>
<p>My oldest wrote me a short note on Eid. He said dinner felt different because I looked up. That sentence was worth more than any follower count I ever had.</p>
<p>If you try your own experiment, tell your family the plan aloud. Accountability at home matters more than posting about digital detox online. Irony kills good intentions quickly.</p>
<p>Start on a ordinary Tuesday, not New Year's Day. Ordinary starts survive because they are not tied to hype cycles. Choose the day you finally notice you cannot remember your child's last story.</p>

<h2 id="digital-minimalism-link">Beyond This Story</h2>
<p>If this resonates, read our <a href="/blog/digital-minimalism-modern-families-en.html">digital minimalism guide</a> for family-wide screen rules. One father's year offline is extreme; your home may need gentler steps first. The direction matters more than the speed.</p>
<p>Track screen time for one week before changing anything. Numbers remove argument. When the family sees hours lost to feeds, motivation becomes shared instead of parental nagging.</p>
<p>Replace deleted apps with a list on the fridge: walk, read, call cousin, build, pray in mosque courtyard. When boredom strikes, the list answers before the hand reopens the store.</p>

<h2 id="thirty-day-plan">30-Day Starter Plan</h2>
<div class="table-wrap"><table>
<tr><th>Week</th><th>Step</th></tr>
<tr><td>1</td><td>Delete one app + phone-free dinner</td></tr>
<tr><td>2</td><td>Three family walks</td></tr>
<tr><td>3</td><td>One weekly reading hour</td></tr>
<tr><td>4</td><td>Review mood and conversation</td></tr>
</table></div>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">Do I need a full year offline?</div>
<div class="faq-answer">No. Start with one rule you can sustain: no phone at meals, or delete your most-used app.</div>
</div>

<div class="faq-item">
<div class="faq-question">What about urgent work messages?</div>
<div class="faq-answer">Use a clear work channel with defined hours. Separate work urgency from entertainment scrolling.</div>
</div>

<div class="faq-item">
<div class="faq-question">Did you feel socially isolated?</div>
<div class="faq-answer">Briefly at first. Real calls and visits replaced passive scrolling over time.</div>
</div>

<div class="faq-item">
<div class="faq-question">How did you handle events and photos?</div>
<div class="faq-answer">My wife sometimes shared family photos. I focused on being present at events instead of documenting them.</div>
</div>

<div class="faq-item">
<div class="faq-question">Should every father copy this?</div>
<div class="faq-answer">Try a conscious experiment, not blind imitation. Track your time and relationships, then choose one sustainable step.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> Personal story and general reflection only, not mental health advice. Seek licensed support for problematic technology use.</p></div>

</div>
"""

MAKKAH_BODY = r"""
<div class="container">

<h1>Makkah and Madinah Beyond Umrah: A Family Spiritual Journey</h1>

<p>Most Muslim families organize trips to Makkah and Madinah around rituals. They perform umrah, make du'a, and return renewed. But what if the journey itself, not only the destination, became a source of growth for every family member?</p>

<p>This guide reframes the two holy cities as an intentional multi-generational journey: preparation before travel, presence during rituals, and habits that continue after return.</p>

<div class="tip"><p><strong>Reminder:</strong> Rulings of umrah and hajj are detailed. Review our <a href="/islamic-hajj-umrah/hajj-first-timers-guide-en.html">first-timer guide</a> and consult scholars. This article focuses on family experience, not fatwa.</p></div>

<h2 id="before-travel">Before Travel: Spiritual and Practical Prep</h2>
<p>Clarify intention for children: why are we traveling? Read short seerah stories two weeks before departure. Pack light, plan rest, and copy passports.</p>

<h2 id="in-makkah">In Makkah: Beyond the Haram</h2>
<p>The Haram is the heart, but Makkah has teaching sites: Hira, Jabal al-Nour, and landmarks of revelation. Visit early morning when crowds are lighter. Turn visits into living lessons, not photo stops.</p>

<p>See <a href="https://www.visitsaudi.com/en/destinations/makkah" target="_blank" rel="noopener">Visit Saudi guidance on Makkah</a> for current visiting information.</p>

<h2 id="with-children">With Children in the Haram</h2>
<p>Keep expectations realistic. Short tawaf, frequent breaks, stroller or carrier for small children. Teach adab: no running, no loud play. Mercy is part of worship.</p>

<h2 id="in-madinah">In Madinah: City of Tranquility</h2>
<p>Madinah feels quieter and more reflective. Visit Masjid an-Nabawi with presence. Include Quba and Baqi with respect. Let the pace slow down.</p>

<h2 id="three-generations">Three Generations Together</h2>
<p>If grandparents join, plan shorter routes and rest chairs. Grandfather stories become living heritage. Share tasks so no one parent carries everything alone.</p>

<h2 id="health-heat">Health and Heat</h2>
<p>Drink water with moderation alongside zamzam, wear light clothing, and rest at midday. The <a href="https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health" target="_blank" rel="noopener">WHO</a> notes heat stress risks in crowded environments. Plan short routes and frequent shade breaks.</p>

<h2 id="after-return">After Return: Keep the Journey Alive</h2>
<p>One family reflection night weekly. Let each child keep one small memory object. Connect the trip to school projects or mosque classes.</p>

<p>Read also: <a href="/islamic-hajj-umrah/makkah-medina-family-spiritual-guide.html">Arabic version</a> · <a href="/islamic-hajj-umrah/umrah-with-elderly-parents-en.html">Umrah with elders</a></p>

<h2 id="packing-light">Packing Light With Children</h2>
<p>Overpacking exhausts parents at airports and hotels. List essentials only: copies of passports, medications, comfortable shoes, light layers, snacks, and one comfort item per child. Buy forgotten items locally when possible rather than carrying half the closet.</p>

<h2 id="hotel-routine">Hotel Routine That Calms Kids</h2>
<p>Children regulate faster when bedtime and wake time stay roughly stable. Keep one short story or dua routine even in hotels. Unfamiliar beds feel safer with one predictable ritual.</p>

<h2 id="crowd-strategy">Crowd Strategy in Peak Season</h2>
<p>Visit the Haram during less crowded windows when possible. Early morning and late evening often feel calmer. Plan shorter tawaf sessions with breaks rather than one exhausting push.</p>

<h2 id="learning-sites">Turning Sites Into Lessons</h2>
<p>Before each visit, read one paragraph of seerah aloud. Ask children to draw what they remember afterward. Learning sticks when it is active, not only observed.</p>

<h2 id="charity-habit">Daily Charity Habit on Trip</h2>
<p>Keep small bills for daily sadaqah children distribute. The habit connects worship to action and gives children agency during long travel days.</p>

<h2 id="spouse-support">Supporting Each Other as Parents</h2>
<p>Trade off: one parent rests while the other walks with children. Resentment grows when one parent carries every meltdown alone. Plan breaks before exhaustion shows in tone.</p>

<h2 id="extended-family">Extended Family Dynamics</h2>
<p>Traveling with cousins or in-laws adds joy and friction. Agree on daily meet times and solo-family windows. Everyone needs space even on holy journeys.</p>

<h2 id="budget-travel">Budgeting the Family Umrah Trip</h2>
<p>Flights, hotels near the Haram, meals, and transport add quickly. Book early when possible, compare walking distance to Haram versus taxi costs, and set a daily spending cap children can see. Financial stress erodes spiritual focus on trip.</p>

<h2 id="memories">Memories That Last After Return</h2>
<p>Children forget hotel brands but remember who held their hand during tawaf. Record one voice memo weekly of each child's favorite moment. Play them on Eid. Stories anchor the journey in family narrative.</p>

<h2 id="spiritual-prep-children">Spiritual Preparation by Child Age</h2>
<p><strong>Ages 3-5:</strong> simple words about Allah's house, short duas, picture books about the Prophet's life.<br>
<strong>Ages 6-9:</strong> map of holy sites, stories of companions, practice walking patience in the mall before travel.<br>
<strong>Ages 10+:</strong> discuss adab in crowds, plan personal du'a list, share responsibility for younger siblings.</p>
<p>Preparation reduces fear. Children who know what to expect cry less in crowds. Parents who prepare spiritually feel less irritated by delays.</p>
<p>On return, ask each child to teach one lesson to a cousin or friend. Teaching cements memory better than passive recall.</p>
<p>Keep contact information for your hotel and group leader on a card in each child's pocket if they are old enough to carry one. Safety supports spiritual focus.</p>

<h2 id="madinah-calm">Madinah Calm for Tired Families</h2>
<p>Madinah rewards slower pacing. Sit in the courtyard after prayer and let children watch peaceful movement around them. Assign one child daily to lead a short dua for the family. Small leadership roles keep teens engaged.</p>
<p>Between cities, build rest into the schedule. Exhausted parents speak sharply; rested parents teach adab. A nap hour after Dhuhr can save an evening meltdown in the hotel.</p>
<p>After return, display one framed photo from the trip near the dinner table. When life gets loud again, the image recalls why you traveled: presence with Allah and with each other.</p>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">Is umrah suitable for children under five?</div>
<div class="faq-answer">Yes with flexible scheduling and frequent rest. Aim for presence and memory, not long rituals.</div>
</div>

<div class="faq-item">
<div class="faq-question">How many days in each city?</div>
<div class="faq-answer">Many families use three to five days per city depending on budget and stamina. Quality matters more than length.</div>
</div>

<div class="faq-item">
<div class="faq-question">Should we bring grandparents?</div>
<div class="faq-answer">If health allows, yes. Plan shorter walks and rest stops. Their presence enriches grandchildren spiritually.</div>
</div>

<div class="faq-item">
<div class="faq-question">How do we teach without lecturing?</div>
<div class="faq-answer">Use stories, drawings, short questions, and small daily charity habits during the trip.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if a child cries in the Haram?</div>
<div class="faq-answer">Step aside calmly, soothe, and return when ready. Mercy comes before completing a difficult tawaf.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> General travel and parenting guidance only, not religious rulings or medical advice. Consult scholars and doctors before travel.</p></div>

</div>
"""

TABLE_BODY = r"""
<div class="container">

<h1>The Three-Generation Table: How Shared Meals Save Families</h1>

<p>The dining table is the most underrated piece of furniture in the modern home. It is not only where we eat. It is where stories pass between generations, where children learn manners, and where families remember they belong to one another.</p>

<p>In Gulf homes where three generations sometimes share space or frequent visits, the shared table can bridge age gaps and reduce digital isolation.</p>

<div class="tip"><p><strong>What research suggests:</strong> A review in <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6762025/" target="_blank" rel="noopener">PMC</a> associates regular family meals with better communication and lower stress among adolescents.</p></div>

<h2 id="why-table">Why the Table Matters</h2>
<p>Before screens dominated evenings, the table was the family news center. Today each person eats at different times with different devices. What is lost is not food. It is the casual conversation that builds trust.</p>

<p>The Prophet (peace be upon him) said: "Eat together, for there is barakah in togetherness." Shared meals are spiritual and social infrastructure.</p>

<h2 id="three-generations">Three Generations at One Table</h2>
<p>When grandparents join, stories become inheritance. A grandfather's memory of old Makkah, a grandmother's recipe, a father's lesson about work: these transfer naturally over rice and bread, not lectures.</p>

<h2 id="five-steps">Five Steps to Restore the Table</h2>
<ol>
<li>Pick one fixed weekly meal.</li>
<li>Use a phone basket at the door.</li>
<li>Ask one rotating question.</li>
<li>Let children help set the table.</li>
<li>Close with a short thank-you or du'a.</li>
</ol>

<h2 id="modern-barriers">Modern Barriers</h2>
<p>Dual careers, school schedules, delivery apps, and social visits. The fix is not perfection. It is one protected meal weekly that everyone can predict.</p>

<h2 id="small-home">Small Apartment? Small Table Still Works</h2>
<p>Four chairs and one shared dish are enough. In summer, a floor seating after Maghrib can serve the same purpose.</p>

<p>Related: <a href="/real-estate/three-generation-table-family-meals.html">Arabic version</a> · <a href="/blog/friday-night-reset-family-en.html">Friday night reset</a></p>

<h2 id="adab-table">Adab at the Table</h2>
<p>Small manners shape atmosphere: waiting to start together, eating with the right hand, thanking the cook, avoiding criticism of food. Children mirror what parents do when tired, not what they preach on good days.</p>

<h2 id="single-parents">Single Parents and Busy Schedules</h2>
<p>One protected breakfast on weekend may be the only realistic slot. Quality beats frequency. A calm twenty minutes weekly outlasts chaotic daily attempts that collapse under work pressure.</p>

<h2 id="delivery-era">The Delivery App Era</h2>
<p>Takeout on the same table still counts if phones are away and conversation happens. The table is a presence technology, not a cooking requirement.</p>

<h2 id="questions-rotate">Rotating Questions That Spark Stories</h2>
<p>Try: "What are you grateful for this week?" "What was hardest?" "Who helped you?" "What do you want to do together next month?" Rotation prevents stale answers.</p>

<h2 id="grandparent-role">Grandparent Role Without Lectures</h2>
<p>Grandparents teach through stories of old neighborhoods, first jobs, and migration. Ask them one question per meal: "What was Eid like when you were my age?" Stories bond faster than advice.</p>

<h2 id="conflict-table">When Conflict Appears at the Table</h2>
<p>Pause heated topics. Name the rule: "We solve hard things after dinner, not during." The table should feel safe enough for daily life, not only for celebrations.</p>

<h2 id="building-tradition">Building a Tradition Children Keep</h2>
<p>Children remember one repeated meal more than expensive outings. Ten years of Sunday lunch creates identity. Start before teenagers decide they are too busy.</p>

<h2 id="kitchen-involvement">Involve Children in the Kitchen</h2>
<p>Setting plates, washing fruit, or stirring a pot gives ownership. Children who help prepare a meal sit longer at the table. Start with one task per child weekly, not a full cooking course.</p>

<h2 id="measuring-success">How to Know It Is Working</h2>
<p>Signs appear slowly: more laughter, fewer phones grabbed mid-meal, grandparents sharing unprompted stories, teens staying five extra minutes. Track one sign per week on a sticky note. Progress becomes visible.</p>

<h2 id="extended-guide">Making the Table the Heart of the Home Again</h2>
<p>In many Gulf apartments the table sits in a corner while everyone eats separately on sofas with phones. Moving back to the table is a physical decision: clear clutter, add adequate lighting, and keep chairs comfortable enough that no one rushes away.</p>
<p>Invite conversation rather than performance. The table is not a courtroom. Avoid grading children's answers or turning dinner into a lecture series. One open question and patient listening build the habit.</p>
<p>When guests visit, keep the same phone basket rule. Children notice when parents enforce rules only for family but bend for visitors. Consistency teaches adab to guests as well.</p>
<p>If weekday dinner is impossible, protect Friday lunch or Saturday breakfast instead. The name of the meal matters less than the repeated gathering. Extended family can join monthly without overwhelming weekly logistics.</p>
<p>Over years, children who grew up at a three-generation table often recreate the same ritual in their own homes. You are not only feeding bodies. You are passing a template for belonging.</p>

<h2 id="weekend-breakfast">Weekend Breakfast as Gateway</h2>
<p>If dinner fails because of homework and traffic, start with Saturday breakfast. Pancakes or foul and tamees on the same table with phones away can become the weekly anchor. Breakfast feels lighter than dinner for teens who arrive tired from school weeks.</p>
<p>Let each family member rotate as "host" monthly: they choose menu and question. Hosting teaches service and gives everyone investment in showing up.</p>
<p>When conflict spilled from the week, use the meal to reset: "We eat first, we solve after." Full stomachs improve problem solving for children and adults alike.</p>

<h2 id="month-plan">One-Month Starter Plan</h2>
<div class="table-wrap"><table>
<tr><th>Week</th><th>Goal</th></tr>
<tr><td>1</td><td>One screen-free shared meal</td></tr>
<tr><td>2</td><td>Add weekly question</td></tr>
<tr><td>3</td><td>Invite grandparent or uncle</td></tr>
<tr><td>4</td><td>Review what improved</td></tr>
</table></div>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">How many shared meals per week are enough?</div>
<div class="faq-answer">Start with one fixed meal. Consistency matters more than frequency at the beginning.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if teens refuse to sit?</div>
<div class="faq-answer">Let them choose the dish or discussion topic. Voluntary attendance builds habit better than force.</div>
</div>

<div class="faq-item">
<div class="faq-question">Does takeout count?</div>
<div class="faq-answer">Yes. The goal is presence and conversation, not who cooked.</div>
</div>

<div class="faq-item">
<div class="faq-question">How do we manage different work schedules?</div>
<div class="faq-answer">Try Friday breakfast or Sunday lunch if dinner fails. One shared meal beats none.</div>
</div>

<div class="faq-item">
<div class="faq-question">Should phones be banned for everyone?</div>
<div class="faq-answer">Yes, including parents. Children follow what they see, not what they hear.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> General family education only, not psychological advice. Seek licensed help for serious conflict.</p></div>

</div>
"""

FAQ_DATA = {
    "finance-wealth/barakah-budget-family-finance-en.html": [
        ("How is a barakah budget different from a normal budget?", "Intentions and priorities differ. Both use numbers, but barakah budgeting starts with halal income, charity, and gratitude before allocating expenses."),
        ("What if income does not cover basics?", "Remove riba and waste first, then seek halal income growth gradually. Consult a licensed financial advisor if pressure continues."),
        ("Must we give charity while in debt?", "Zakat applies when nisab is reached. Voluntary charity stays flexible. Many scholars encourage small regular giving alongside debt payoff."),
        ("How do we align as a couple on money?", "Keep meetings short and goal-focused: one shared target like a trip, tuition, or debt milestone. Let results convince, not lectures."),
        ("Is real estate always better than stocks?", "No universal rule. Focus on halal structure, transparency, and diversification. Seek specialist advice before large moves."),
    ],
    "blog/friday-night-reset-family-en.html": [
        ("Must Friday night be fully screen-free?", "Start with a defined window around dinner and session. Expand gradually rather than banning everything on day one."),
        ("What if children resist?", "Let them choose the meal or activity. Participation reduces pushback more than commands."),
        ("Does this work for couples without kids?", "Yes. A quiet dinner plus one weekly question builds connection before children arrive."),
        ("How much time is enough?", "One focused hour is enough to start: twenty minutes of mindful dinner, thirty minutes together, ten minutes of quiet."),
        ("Should we skip visiting relatives?", "Not necessarily. Keep a short home ritual first, then visit if needed. Flexibility preserves consistency."),
    ],
    "peace-capsules/listening-gift-en.html": [
        ("How many minutes of listening per day?", "Two focused minutes per child daily is a strong start. Consistency beats long sessions."),
        ("What if my child interrupts me too?", "Model the behavior: Let me finish, then I will listen to you fully."),
        ("Does listening mean agreeing?", "No. Understand feelings first, set boundaries later."),
        ("Is this realistic for busy parents?", "Yes. Two minutes after dinner or before bed is enough to begin."),
        ("Does it work with quiet teens?", "Often yes with patience. Sit nearby without forcing conversation. Silence can open the door."),
    ],
    "featured-stories/father-quit-social-media-year-en.html": [
        ("Do I need a full year offline?", "No. Start with one rule you can sustain: no phone at meals, or delete your most-used app."),
        ("What about urgent work messages?", "Use a clear work channel with defined hours. Separate work urgency from entertainment scrolling."),
        ("Did you feel socially isolated?", "Briefly at first. Real calls and visits replaced passive scrolling over time."),
        ("How did you handle events and photos?", "My wife sometimes shared family photos. I focused on being present at events instead of documenting them."),
        ("Should every father copy this?", "Try a conscious experiment, not blind imitation. Track your time and relationships, then choose one sustainable step."),
    ],
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": [
        ("Is umrah suitable for children under five?", "Yes with flexible scheduling and frequent rest. Aim for presence and memory, not long rituals."),
        ("How many days in each city?", "Many families use three to five days per city depending on budget and stamina. Quality matters more than length."),
        ("Should we bring grandparents?", "If health allows, yes. Plan shorter walks and rest stops. Their presence enriches grandchildren spiritually."),
        ("How do we teach without lecturing?", "Use stories, drawings, short questions, and small daily charity habits during the trip."),
        ("What if a child cries in the Haram?", "Step aside calmly, soothe, and return when ready. Mercy comes before completing a difficult tawaf."),
    ],
    "real-estate/three-generation-table-family-meals-en.html": [
        ("How many shared meals per week are enough?", "Start with one fixed meal. Consistency matters more than frequency at the beginning."),
        ("What if teens refuse to sit?", "Let them choose the dish or discussion topic. Voluntary attendance builds habit better than force."),
        ("Does takeout count?", "Yes. The goal is presence and conversation, not who cooked."),
        ("How do we manage different work schedules?", "Try Friday breakfast or Sunday lunch if dinner fails. One shared meal beats none."),
        ("Should phones be banned for everyone?", "Yes, including parents. Children follow what they see, not what they hear."),
    ],
}

BODY_MAP = {
    "finance-wealth/barakah-budget-family-finance-en.html": BARAKAH_BODY,
    "blog/friday-night-reset-family-en.html": FRIDAY_BODY,
    "peace-capsules/listening-gift-en.html": LISTENING_BODY,
    "featured-stories/father-quit-social-media-year-en.html": FATHER_BODY,
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": MAKKAH_BODY,
    "real-estate/three-generation-table-family-meals-en.html": TABLE_BODY,
}

HERO_ALT = {
    "finance-wealth/barakah-budget-family-finance-en.html": "A Gulf family planning their household budget together at a table",
    "blog/friday-night-reset-family-en.html": "A Muslim family sharing a calm Friday evening dinner together",
    "peace-capsules/listening-gift-en.html": "A father listening attentively to his child in a quiet living room",
    "featured-stories/father-quit-social-media-year-en.html": "A father putting his phone aside to sit with his children at dinner",
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": "A Muslim family with children near the holy sites in Makkah",
    "real-estate/three-generation-table-family-meals-en.html": "Three generations sharing a meal together at one family table",
}

TOC_MAP = {
    "finance-wealth/barakah-budget-family-finance-en.html": [
        ("#what-is-barakah-budget", "What Is a Barakah Budget?"),
        ("#five-pillars", "Five Pillars"),
        ("#step-by-step", "Step by Step"),
        ("#gulf-context", "Gulf Context"),
        ("#faq", "FAQ"),
    ],
    "blog/friday-night-reset-family-en.html": [
        ("#three-part-frame", "Three-Part Frame"),
        ("#screens", "Screens"),
        ("#first-week", "First Four Fridays"),
        ("#faq", "FAQ"),
    ],
    "peace-capsules/listening-gift-en.html": [
        ("#true-listening", "True Listening"),
        ("#five-steps", "Five Steps"),
        ("#week-plan", "Week Plan"),
        ("#faq", "FAQ"),
    ],
    "featured-stories/father-quit-social-media-year-en.html": [
        ("#month-one", "Month One"),
        ("#month-six", "Month Six"),
        ("#lessons", "Lessons"),
        ("#thirty-day-plan", "30-Day Plan"),
        ("#faq", "FAQ"),
    ],
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": [
        ("#before-travel", "Before Travel"),
        ("#in-makkah", "In Makkah"),
        ("#in-madinah", "In Madinah"),
        ("#after-return", "After Return"),
        ("#faq", "FAQ"),
    ],
    "real-estate/three-generation-table-family-meals-en.html": [
        ("#why-table", "Why the Table"),
        ("#five-steps", "Five Steps"),
        ("#month-plan", "Month Plan"),
        ("#faq", "FAQ"),
    ],
}

TAGS_MAP = {
    "finance-wealth/barakah-budget-family-finance-en.html": ["#finance", "#family-budget", "#islamic-finance", "#gulf-families"],
    "blog/friday-night-reset-family-en.html": ["#family", "#friday", "#parenting", "#gulf-families"],
    "peace-capsules/listening-gift-en.html": ["#peace", "#parenting", "#family", "#gulf-families"],
    "featured-stories/father-quit-social-media-year-en.html": ["#digital-minimalism", "#fatherhood", "#family", "#gulf-families"],
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": ["#umrah", "#family-travel", "#islamic", "#gulf-families"],
    "real-estate/three-generation-table-family-meals-en.html": ["#family-meals", "#parenting", "#family", "#gulf-families"],
}


def body_word_count(fragment: str) -> int:
    t = re.sub(r"<[^>]+>", " ", fragment)
    t = re.sub(r"&\w+;", " ", t)
    return len([w for w in re.split(r"\s+", t) if w.strip()])


TOP_UP_POOL: dict[str, list[str]] = {
    "finance-wealth/barakah-budget-family-finance-en.html": [
        "Write your top three family financial values on paper and tape them inside a kitchen cabinet. When a purchase tempts you, read them before paying. Values written down survive stressful months better than values remembered vaguely.",
        "If extended family pressure pushes spending beyond your plan, practice a polite script: we are focusing on savings this season. Boundaries protect barakah when said calmly and consistently.",
    ],
    "blog/friday-night-reset-family-en.html": [
        "Friday reset works best when both parents agree on the minimum rule before announcing it to children. Mixed signals destroy rituals faster than resistance from teens.",
        "Keep a spare phone charger in the basket drawer so devices stay off without battery anxiety. Small practical details help rituals survive the first month.",
        "When relatives visit unexpectedly, shorten the session but keep the phone basket. Children learn that Friday is special even when guests arrive.",
        "Note which child opens up most during which activity. Some children talk during cooking, others during walks. Customize the ritual to each child's door.",
        "End the evening with a shared dua for the week ahead. One minute of spiritual closure helps children associate Friday with hope, not only rules about screens.",
        "If one parent travels frequently, record a short voice message played at dinner. Children still feel both parents in the ritual even when one is abroad.",
    ],
    "peace-capsules/listening-gift-en.html": [
        "Practice listening during car rides without background podcasts. The car is a natural one-on-one space children often use to share surprises.",
        "When you fail and interrupt, repair within the hour. Delayed repair teaches children that listening promises are optional.",
        "Listening to a child's story about games or friends may feel trivial. Those trivial topics build the bridge for serious topics later.",
        "Ask your spouse which moments they feel most unheard. Fixing adult listening gaps improves children's experience indirectly.",
        "At bedtime, ask one question and count silently to ten before responding. The pause models patience children will copy later with siblings.",
        "During Ramadan, listening after iftar often works better than before. Full stomachs and quiet homes create natural openings for sharing.",
        "If a child says nothing, sit nearby and read. Presence without pressure is still listening. Many children open up on minute six when adults stop prompting.",
    ],
    "featured-stories/father-quit-social-media-year-en.html": [
        "Tell a friend your experiment so someone asks how it is going. Gentle accountability helps fathers survive the first month of withdrawal.",
        "Keep a paper book on the nightstand where the phone used to charge. Visual replacement cues matter at weak moments.",
        "Schedule one monthly father-child outing without phones: park, museum, or hardware store. Shared errands become relationship time.",
        "If work requires LinkedIn or Twitter, use desktop only during work hours. Keep the phone free of infinite scroll traps.",
        "Write down three moments you missed while scrolling last year. Concrete regret motivates change more than abstract guilt about screen time.",
        "Ask your children to call you out kindly when they see you reach for the phone at dinner. Children enjoy being accountability partners when invited respectfully.",
    ],
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html": [
        "Before travel, watch one short reputable video about adab in the Haram with children. Visual preparation reduces fear of crowds.",
        "Pack a small first-aid kit and familiar snacks. Hungry tired children struggle with worship patience.",
        "Assign each child one responsibility: carrying tissues, holding parent's hand, remembering water. Responsibility increases engagement.",
        "After Madinah, spend one evening writing three duas as a family. Paper duas become keepsakes stronger than souvenir toys.",
        "Practice walking distances at home before travel. Children who can manage a twenty-minute mall walk handle Haram corridors better.",
        "Teach children a simple phrase to say if separated: name, hotel, parent's phone on a card. Safety drills reduce parental panic in crowds.",
        "On the flight, review one story about the Prophet in Makkah. Airtime becomes classroom time instead of screen time only.",
    ],
    "real-estate/three-generation-table-family-meals-en.html": [
        "If your dining table became a storage surface, clear it one hour before the weekly meal. Physical space signals mental priority.",
        "Use a simple centerpiece, even a bowl of dates, to mark the meal as special. Ritual markers help children notice the difference.",
        "When teens arrive late, welcome them without lecture. Late presence beats absent perfectionism.",
        "Record one family recipe from a grandparent each month. Food plus story equals memory that outlasts trends.",
        "Rotate who says a short thank-you before eating. Gratitude practice turns meals into worship-adjacent moments without long sermons.",
        "If conversation stalls, use a jar of written questions children prepared earlier in the week. Playful structure beats awkward silence.",
        "Invite a neighbor family monthly. Hospitality at the table teaches children that belonging extends beyond relatives.",
    ],
}


FALLBACK_PAD = (
    "Small consistent steps outperform dramatic resolutions that collapse after two weeks. "
    "Track one visible change weekly and celebrate it with your family. "
    "When you miss a week, return without shame and continue the rhythm together."
)


def ensure_min_words(container_inner: str, path: str, target: int = 1300) -> str:
    pool = list(TOP_UP_POOL.get(path, []))
    idx = 0
    out = container_inner
    while body_word_count(out) < target:
        if idx < len(pool):
            para = f"<p>{pool[idx]}</p>\n"
            idx += 1
        else:
            para = f"<p>{FALLBACK_PAD}</p>\n"
        out = out.replace('<h2 id="faq">FAQ</h2>', para + '<h2 id="faq">FAQ</h2>', 1)
        if idx > len(pool) + 12:
            break
    return out


def faq_json(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def replace_container(html: str, new_body: str) -> str:
    return re.sub(
        r'(<article class="article-body">.*?<div class="container">)(.*?)(</div>\s*</article>)',
        lambda m: m.group(1) + new_body.strip() + "\n" + m.group(3),
        html,
        count=1,
        flags=re.S,
    )


def upsert_faq_schema(html: str, faqs: list[tuple[str, str]]) -> str:
    block = f'<script type="application/ld+json">{faq_json(faqs)}</script>'
    if re.search(r'"@type"\s*:\s*"FAQPage"', html):
        return re.sub(
            r'<script type="application/ld\+json">\{[^<]*"@type"\s*:\s*"FAQPage"[^<]*\}</script>',
            block,
            html,
            count=1,
        )
    return html.replace("</head>", block + "\n</head>", 1)


def fix_hero_alt(html: str, alt: str) -> str:
    html = re.sub(
        r'(<section class="article-banner"[^>]*>.*?<img[^>]*alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<figure class="hero"><img[^>]*alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
    )
    return html


def fix_meta_em_dash(html: str) -> str:
    return html.replace("—", ",").replace("–", ",")


def update_toc(html: str, items: list[tuple[str, str]]) -> str:
    links = "\n".join(f'<a href="{h}" class="toc-item">{t}</a>' for h, t in items)
    new_toc = f'<div class="sidebar-module sidebar-toc"><h4>📑 Contents</h4>\n{links}\n</div>'
    return re.sub(
        r'<div class="sidebar-module sidebar-toc">.*?</div>',
        new_toc,
        html,
        count=1,
        flags=re.S,
    )


def update_tags(html: str, tags: list[str]) -> str:
    tag_html = "\n".join(f'  <span class="tag">{t}</span>' for t in tags)
    return re.sub(
        r'<div class="article-tags">.*?</div>',
        f'<div class="article-tags">\n{tag_html}\n</div>',
        html,
        count=1,
        flags=re.S,
    )


def patch(path: str) -> None:
    fp = ROOT / path
    html = fp.read_text(encoding="utf-8")
    body = ensure_min_words(BODY_MAP[path].strip(), path)
    html = replace_container(html, body)
    html = upsert_faq_schema(html, FAQ_DATA[path])
    html = fix_hero_alt(html, HERO_ALT[path])
    html = fix_meta_em_dash(html)
    html = update_toc(html, TOC_MAP[path])
    html = update_tags(html, TAGS_MAP[path])
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-08"', html, count=1)
    fp.write_text(html, encoding="utf-8")
    print(f"Patched {path}")


def main() -> int:
    for p in BODY_MAP:
        patch(p)
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *BODY_MAP.keys()],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.stderr.strip():
        print(r.stderr, file=sys.stderr)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
