from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent.booking_agent import build_agent
from app.calendar_utils import check_availability, book_meeting
import dateparser
import re

app = FastAPI()

# Enable frontend connection (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Smart datetime extractor
def extract_datetime_phrase(text):
    patterns = [
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}.*?(am|pm|AM|PM)?",
        r"\d{1,2}\s+\w+\s+\d{4}.*?(am|pm|AM|PM)?",
        r"\d{1,2}\s+\w+.*?(am|pm|AM|PM)?",
        r"(tomorrow|today|next \w+|on \w+)\s*(at)?\s*\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)?",
        r"in \d+\s+(minute|minutes|hour|hours)",
        r"\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().strip()
    return ""

# LangGraph agent instance
agent = build_agent()

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("input", "").strip()

        print("👤 User input:", user_input)

        # Step 1: Let LangGraph handle response flow
        result = agent.invoke({"user_input": user_input})
        agent_response = result.get("response", "🤖 Hello!")

        print("🤖 Agent response:", agent_response)

        # Step 2: If agent is still asking for time
        if "when would you like" in agent_response.lower():
            return {"output": agent_response}

        # Step 3: Try to extract date/time
        extracted = extract_datetime_phrase(user_input)
        dt = dateparser.parse(extracted)
        print("🕒 Extracted:", extracted)
        print("📅 Parsed datetime:", dt)

        if dt:
            dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

            available, events = check_availability(dt_str)
            if available:
                booking = book_meeting("TailorTalk Meeting", dt_str)
                return {"output": booking["message"]}
            else:
                return {
                    "output": f"❌ That time is already booked. Try a different time slot."
                }
        else:
            return {
                "output": (
                    f"{agent_response}\n\n"
                    "⏰ I couldn't understand the date/time.\n"
                    "✅ Try examples like:\n"
                    "- Book a meeting **tomorrow at 4 PM**\n"
                    "- Schedule for **03/07/2025 at 3 PM**\n"
                    "- Book in **2 hours**"
                )
            }

    except Exception as e:
        print("🔥 Internal error:", str(e))
        return {"output": f"❌ Internal Server Error: {str(e)}"}
