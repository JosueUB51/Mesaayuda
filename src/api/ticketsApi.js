const API_URL = "http://127.0.0.1:8000";

export async function createTicket(subject) {
  const response = await fetch(`${API_URL}/tickets`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ subject }),
  });

  if (!response.ok) {
    throw new Error("Error al crear el ticket");
  }

  return response.json();
}

export async function sendMessage(text) {
  const res = await fetch("http://localhost:8000/tickets/message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  return res.json();
}

