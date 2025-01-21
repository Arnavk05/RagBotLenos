# Overview 

Script that builds a full working chatbot that will answer questions based on data from any given website.

Scrapes a given webpage for all data and subpages using beautifulsoup, converts to pdf format, splits into stream of chunked values and Retrieval-Augmented-Generation is used to generate context for any given query, which is then passed to OpenAI API and streamed to gradio as a working chatbot app.

# How to Run

First run scraper.ipynb inputting the url and base url you want to scrape, feed the output pdf to ingest_database.py (only need to do this once) and then run chatbot.py to run that actual chatbot script.
