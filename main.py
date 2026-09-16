import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import re
import pandas as pd