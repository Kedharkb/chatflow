# Chatflow Setup Guide

Welcome to the Chatflow project! This guide will help you set up the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following software installed:

- *Ubuntu >= 20.04*
- *Python 3.x*
- *Git*
- *Visual Studio Code (VS Code)*

## Step 1: Clone the Repository

First, clone the Chatflow repository to your local machine:

git clone https://github.com/Kedharkb/chatflow.git  <br>
cd chatflow

## Step 2: Set Up Python Virtual Environment
Setting up a Python virtual environment will help manage dependencies:<br>

Install the python3-venv package:<br>
sudo apt install python3-venv<br>

Create the virtual environment:<br>
python3 -m venv chatenv<br>
Activate the virtual environment:<br>

source chatenv/bin/activate <br>

## Step3. Install Dependencies for ChromaDB
sudo apt-get update
sudo apt-get install sqlite3 libsqlite3-dev
sudo apt-get install python3-dev

## Step4. Install Python Dependencies
pip install -r requirements.txt

## Step5. Open Visual Studio Code.
Navigate to the Extensions view (click on the Extensions icon in the Sidebar or press Ctrl+Shift+X).
Search for "Promptflow" and install the extension.

## Step6.  Create OpenAI Connection
pf connection create --file ./openai.yaml --set api_key=xxxxx --name open_ai_connection





6