#  TailorTalk – AI Calendar Booking Assistant

TailorTalk is a conversational AI assistant that books Google Calendar meetings from natural language messages like:

> "Book a meeting tomorrow at 4 PM"  
> "Schedule something on July 2nd at 10am"  
> "Set a meeting in 2 hours"

Built using FastAPI, Streamlit, Google Calendar API, LangGraph, and date parsing, this app turns casual language into real calendar actions.

---

##  Features

- Conversational flow powered by LangGraph  
- Google Calendar integration (via OAuth)  
- Understands flexible time formats like:
  - "tomorrow at 5pm"
  - "12/07/2025 at 10 AM"
  - "in 2 hours"
- Checks availability before booking  
- Confirms meeting with clickable calendar link  
- Remembers intent and follows up  

---

##  Tech Stack

| Layer        | Technology          |
|--------------|---------------------|
| Frontend     | Streamlit           |
| Backend API  | FastAPI             |
| NLP Flow     | LangGraph           |
| Calendar API | Google Calendar API |
| Time Parsing | dateparser          |
| Language     | Python              |

---

##  Folder Structure

"# Tailor_Talk_" 
