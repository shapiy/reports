# Reports

Send customized emails with Toggl time reports.

[![Build Status](https://travis-ci.com/shapiy/reports.svg?branch=master)](https://travis-ci.com/shapiy/reports)

## Introduction
[Scheduled email reports](https://support.toggl.com/analyzing-time-and-reporting/other-reporting-sections-and-features/scheduled-reports-to-email) is a Premium Toggl feature.
`Reports` allow to save money especially if you are an individual user working with a single
customer. 

The code in this repo is basically an [AWS Lambda](https://aws.amazon.com/lambda/?sc_channel=PS&sc_campaign=acquisition_UA&sc_publisher=google&sc_medium=lambda_b&sc_content=lambda_e&sc_detail=aws%20lambda&sc_category=lambda&sc_segment=150979667187&sc_matchtype=e&sc_country=UA&s_kwcid=AL!4422!3!150979667187!e!!g!!aws%20lambda&ef_id=EAIaIQobChMIwff_h_yz4QIVkh0YCh2AFw4wEAAYASAAEgJ_7fD_BwE:G:s) function.
The lambda is meant to be invoked by a Cron trigger every week or so. Emails
are sent using [Sendgrid](https://sendgrid.com/marketing/sendgrid-services-cro/?extProvId=5&extPu=49397-gaw&extLi=164417502&sem_adg=8807285742&extCr=8807285742-338975812295&extSi=&extTg=&keyword=%2Bsendgrid&extAP=1t1&extMT=b&gclid=EAIaIQobChMI7-2_lfyz4QIV1eeaCh2SUAA6EAAYASAAEgLu-vD_BwE) API. This model 
is cost effective: Running one AWS Lambda weekly or even daily is [very cheap](https://aws.amazon.com/lambda/pricing/). 
As for emails, Sengrid [Free plan](https://sendgrid.com/free/) offers an order of magnitude more emails than we need.              

## Getting started
TBD

## Development
### Running tests and static code analysis
```bash
tox
``` 

### Updating tox dependencies
```bash
pipenv lock --requirements > requirements.txt
pipenv lock --requirements --dev | grep -v '^\-e .$' > requirements-dev.txt
```  
