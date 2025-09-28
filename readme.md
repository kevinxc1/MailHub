# System Design Overview

1. initialize AgentMail Python Client
2. Connect to MailHub6767@gmail.com
3. Check if the recieved application passes screening

## Start the interview process
1. AgentMail sends an email to the applicant for interview times and the applicant responds.
2. AgentMail returns the response from applicant to a human interviewer. If the interviewer says:
    yes: continue to step 3
    No: go back to step 1
3. AgentMail sends an email to applicant asking them to verify. If applicant says:
    yes: continue to 4
    No: go back to step 1
4. AgentMail sends email to interviewer to tell them that the interview is confirmed.

## Back and forth conversation between applicant and interviewer
1. AgentMail receives an email from applicant and AgentMail responds. If applicant:
    replies with more questions: go back to step 1
    doesn't reply/says thanks AgentMail: Process is finished