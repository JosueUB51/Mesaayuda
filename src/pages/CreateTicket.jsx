import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import { sendMessage } from "../api/ticketsApi";
import "../styles/create-ticket.css";

export default function CreateTicket() {
  const navigate = useNavigate();

  const [text, setText] = useState("");
  const [messages, setMessages] = useState([
    { from: "ai", text: "Hola 👋 ¿En qué puedo ayudarte?" }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim() || loading) return;

    const userText = text;
    setText("");
    setLoading(true);

    // Mensaje del usuario
    setMessages(prev => [...prev, { from: "user", text: userText }]);

    try {
      const response = await sendMessage(userText);

      // IA hace pregunta (texto ambiguo)
      if (response.type === "question") {
        setMessages(prev => [
          ...prev,
          { from: "ai", text: response.message }
        ]);
      }

      // IA ya entendió → crea ticket
      if (response.type === "ticket") {
        navigate("/summary", { state: response.ticket });
        return;
      }

    } catch (err) {
      setMessages(prev => [
        ...prev,
        { from: "ai", text: "Ocurrió un error, intenta nuevamente." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header />

      <main className="page">
        <div className="layout">
          <h1>Hola, Cesar Santiago</h1>
          <p className="subtitle">Hagamos tu solicitud más fácil.</p>

          <div className="ticket-box">

            {/* CONVERSACIÓN */}
            <div className="conversation">
              {messages.map((msg, i) => (
                <div key={i} className={`bubble ${msg.from}`}>
                  {msg.text}
                </div>
              ))}

              {loading && (
                <div className="bubble ai typing">La IA está escribiendo…</div>
              )}
            </div>

            {/* INPUT */}
            <textarea
              placeholder="Describa su solicitud..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSubmit()}
            />

            <div className="actions">
              <button className="attach">+</button>
              <button className="primary" onClick={handleSubmit} disabled={loading}>
                Enviar
              </button>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
