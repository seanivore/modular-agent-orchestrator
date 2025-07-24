#!/usr/bin/env python3
# /// script
# dependencies = [
#   "anthropic>=0.17.0", 
#   "rich>=13.7.0",
#   "python-dotenv>=1.0.0",
#   "beautifulsoup4>=4.12.2",
#   "requests>=2.31.0",
#   "Pillow>=10.1.0",
#   "openai>=1.4.0"  # Added for Requesty API integration
# ]
# ///

import os
import sys
import json
import base64
import argparse
import asyncio
import requests
import glob as glob_module
import fnmatch
from rich.console import Console
from rich.table import Table
from anthropic import Anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from PIL import Image
import io
import datetime
import json as json_module  # Rename to avoid conflict

# Constants
DEFAULT_MAX_ITERATIONS = 20
MAX_TOKEN_SAFE_LIMIT = 75000

# Simple cache for script files to prevent redundant reading of large files
script_cache = {}

# Load environment variables
load_dotenv()
console = Console()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
brave_api_key = os.getenv("BRAVE_API_KEY")
brave_subscription_token = os.getenv("X_SUBSCRIPTION_TOKEN")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

# Initialize Requesty client if API key exists
requesty_api_key = os.getenv("requesty_api_key")
requesty_client = None
if requesty_api_key:
    try:
        import openai
        requesty_client = openai.OpenAI(
            api_key=requesty_api_key,
            base_url="https://router.requesty.ai/v1"
        )
        console.print("[green]Requesty API client initialized successfully[/green]")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not initialize Requesty client: {str(e)}[/yellow]")

# Define the Claude model to use
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"  # Updated to the correct Claude 3.7 Sonnet model ID

# Global variables for tracking execution state
max_iterations = DEFAULT_MAX_ITERATIONS
conversation_history = []
current_iteration = 0
phase_loops = 0  # Counter for how many times the phase has been extended
phase_complete = False
should_continue_iterations = True