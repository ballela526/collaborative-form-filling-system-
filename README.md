# collaborative-form-filling-system

# 1.Collaborative Form Filling App (Python + Redis + WebSockets)

A real-time collaborative form-filling web application built using:

- Python (FastAPI / Socket.IO backend)
- Redis (for pub/sub and state management)
- HTML + TailwindCSS (frontend)
- WebSockets (for real-time form synchronization)

---

Features

- Admin can create custom forms with any number of fields using JSON
- Users can join a form using a unique form ID
- Real-time synchronization between multiple users editing the same form
- Redis pub/sub ensures low-latency updates and shared state management


Tech Stack

| Component     | Technology          |
|---------------|---------------------|
| Backend       | Python, FastAPI, python-socketio |
| Frontend      | HTML, TailwindCSS, Vanilla JS |
| Realtime Sync | WebSockets (Socket.IO) |
| State Storage | Redis (async pub/sub) |

---

Installation and Setup

* Clone the Repository
```bash
git clone https://github.com/your-username/collaborative-form-filling.git
cd collaborative-form-filling

#2. Set Up Environment Variables
Create a .env file in the root directory with the following content:

env
Copy
Edit
REDIS_HOST=localhost
REDIS_PORT=6379
Make sure Redis is running on your machine at port 6379.

#3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt

#4. Start the Backend Server
bash
Copy
Edit
python -m app.main

# 5. Open the Frontend
Open index.html in your browser. You can open it in multiple tabs or separate browsers to simulate multiple users.

Sample Form JSON
Use the following example when creating a form:

json
Copy
Edit
[
  { "label": "Name", "type": "text" },
  { "label": "Age", "type": "number" },
  { "label": "Email", "type": "email" }
]
Usage Flow
The admin creates a form by entering a title and field structure in JSON.

A form ID is generated and displayed.

Other users can join using that form ID.

All users see real-time updates as the form is filled.
