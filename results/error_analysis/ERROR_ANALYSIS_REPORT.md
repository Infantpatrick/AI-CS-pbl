# ERROR ANALYSIS REPORT

## Overview
- **Model Used:** Fine-tuned BERT (`models/bert_phishing`)
- **Test Dataset Size:** 8789 samples

## Error Metrics
- **True Positives (TP):** 4331
- **True Negatives (TN):** 1609
- **False Positives (FP):** 2737
- **False Negatives (FN):** 112

- **False Positive Rate:** 0.6298
- **False Negative Rate:** 0.0252
- **Precision:** 0.6128
- **Recall:** 0.9748
- **F1-score:** 0.7525

## Representative False Positives (Legitimate -> Phishing)
**Example 1:**
> global risk management operations weekly operating report tammie , attached is the global risk management operations update for louise ' s weekly report , week ending february 2 . if you have any questions , please let me know . thanks , brian

**Example 2:**
> sociolinguistics michael g . smith language and power in the creation of the ussr 1917 - - 1953 1998 . 23 x 15 , 5 cm . vii , 294 pages cloth dm 178 , - / approx . us $ 111 . 00 isbn 3-11 - 016197 - 4 contributions to the sociology of language 80 mouton de gruyter * berlin * new york this is the fir...

**Example 3:**
> [Spambayes-checkins] spambayes/spambayes hammie.py,1.16,1.17 Update of /cvsroot/spambayes/spambayes/spambayes In directory sc8-pr-cvs8.sourceforge.net:/tmp/cvs-serv21792 Modified Files: hammie.py Log Message: Why was this missing? Index: hammie.py ====================================================...

**Example 4:**
> postings hi , i ' m working on a phonetics project about modern irish and i ' m having a hard time finding sources . can anyone recommend books or articles in english ? i ' , specifically interested in palatal ( slender ) consonants , so any work on that would be helpful too . thanks ! laurel sutton...

**Example 5:**
> Re: USA USA WE ARE NUMBER ....six. On Wed, 24 Jul 2002, Tom wrote: > "Around the world, there is a growing sense that democracy has not > delivered development" Sakiko Fukuda-Parr UN report author Or perhaps it is the unregulated and out of control capitalism used as a tool to concentrate wealth and...

## Representative False Negatives (Phishing -> Legitimate)
**Example 1:**
> from : feng from : mr . feng lee . hang seng bank ltd sai wan ho branch 171 shaukiwan road hong kong . sir , let me start by introducing myself . i am mr feng lee . director of operations of the hang seng bank ltd , sai wan ho branch . i have a mutual beneficial business suggestion for you . before ...

**Example 2:**
> hello $ name return - path : received : from [ 216 . 35 . 187 . 6 ] ( helo webmillion . com ) by mxl 2 . clusterl . charter . net ( communigate pro smtp 3 . 5 . 9 ) with esmtp id 4992751 for knb 4 menu @ charter . net ; fri , 26 apr 2002 08 : 09 : 39 - 0400 received : from es - wmstagel [ 216 . 35 ....

**Example 3:**
> please endeavour to use this for charity . from : mrs . ruth makary . please endeavour to use this for charity . calvary greetings ! ! my name is mrs . ruth makary a 65 yrs old lady . i am a cancer patient and a nationality of kuwait . i am married to mr . sammy makary who worked with kuwait embassy...

**Example 4:**
> breaking news would you ref inance if you knew you ' d save thousands ? we ' ll get you lnterest as low as 3 . 23 % . have bad c [ r ] edit ? no problem ! low rates are fixed no matter what . fill out our small online form and we ' ll show you how . get the house and / or car you always wanted , it ...

**Example 5:**
> [Notice Update Activity] : Your AppIe ID has been locked for security reason. Dear Client, Due to a problem with your ca{ip}rd, we have been unable to charge your ac{ip}c{ip}ount. Your A{ip}p{ip}p{ip}le ID automatically locks to protect your se{ip}cu{ip}rity and you can't sign in to any Ap{ip}p{ip}l...

## Error Patterns Identified
Based on the misclassified examples, common patterns include:
- **Ambiguous Legitimate Emails (FP):** Short or automated notifications often mimic phishing patterns.
- **Urgency Language (FP):** Legitimate emails containing strong urgency (e.g. "urgent meeting", "password reset") triggered the model.
- **Obfuscated Text (FN):** Phishing emails that use highly obfuscated text or entirely legitimate-looking corporate language occasionally slipped past.

## Conclusion and Limitations
The model struggles primarily with false positives, suggesting it is highly sensitive to phishing indicators and operates aggressively. While good for security, this requires users to whitelist legitimate senders manually to reduce notification fatigue. Future iterations could use secondary features (like sender domains or URL analysis) to lower the false positive rate.
