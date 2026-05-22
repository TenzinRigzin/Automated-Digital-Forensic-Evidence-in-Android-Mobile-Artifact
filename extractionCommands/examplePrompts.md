# 🕵️ Mobile Forensic Analysis Prompts

Use these prompt templates to extract evidence, build timelines, and audit security using your local AI dashboard.

---

## 🚨 Phase 1: Critical Security & Risk
*Use these to instantly flag threats or unauthorized access.*

- **OTP & 2FA Scan:** "Scan the logs for 'code', 'verification', 'OTP', or 'password'. List the sender and timestamp for each occurrence."
- **Financial Audit:** "Extract every message containing currency symbols ($, ₹, €, 'USD', 'INR') or transaction alerts. Tabulate the amounts and senders."
- **Suspicious Links:** "List every website URL (http/https) found in the text logs. Do any look like phishing domains?"
- **Network Cross-Check:** "Cross-reference the Wi-Fi dump with the SMS logs. Was the device connected to a public network during the latest message exchange?"

---

## ⏳ Phase 2: Timeline & Chronology
*These prompts leverage the 'Chronological Engine' to prioritize recent events.*

- **Latest Activity:** "Based strictly on the top rows of the file, what are the absolute most recent 5 messages received? Who sent them?"
- **The 'Gap' Analysis:** "Look at the timestamps between [Date A] and [Date B]. Are there any long periods of silence or missing logs?"
- **Event Reconstruction:** "Create a minute-by-minute timeline of all incoming and outgoing messages for [Date]. Organize them from morning to night."
- **Reverse-Order Check:** "Compare the tone of the messages at the top of the file (newest) vs. the bottom (oldest). Has the user's sentiment changed over time?"

---

## 👥 Phase 3: Social & Behavioral Profiling
*Use these to understand relationships and intent.*

- **The 'Frequency' Map:** "Who is the most frequent contact in these logs? Summarize the general topic of their conversation."
- **Keyword Hunter:** "I am looking for a specific conversation about [Topic, e.g., 'meeting', 'debt', 'package']. Find the exact message body and date."
- **Unknown Numbers:** "List all messages sent from numbers that do not have a saved contact name (if visible). Summarize their content."
- **Sentiment Scan:** "Identify any conversations that contain aggressive, urgent, or threatening language."

---

## ⚙️ Technical Operators
*Use these to formatting the AI's output.*

- **Epoch Conversion:** "Note that the 'date' column is in Unix Epoch milliseconds. Please convert all timestamps to human-readable 'YYYY-MM-DD HH:MM:SS' format in your answer."
- **Clean List:** "Output the results as a clean markdown table with columns: Sender, Date, and Message Content."
- **Raw Evidence:** "Quote the message text exactly as it appears in the log. Do not paraphrase."
