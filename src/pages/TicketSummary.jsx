import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import Header from "../components/Header";
import ConfirmModal from "../components/ConfirmModal";
import "../styles/ticket-summary.css";

export default function TicketSummary() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);

  if (!state) return null;

  return (
    <>
      <Header user="Cesar Santiago" />

      <main className="page">
        <h2>Resumen de Ticket</h2>

        <div className="summary-card">
          <div className="row">
            <strong>Ticket N°:</strong> {state.ticket_code}
            <span className="time">Hora: {state.created_time.slice(0, 5)}</span>
          </div>

          <div className="row topic-row">
            <strong>Tema de ayuda:</strong>
            <span className="topic">{state.department}</span>
          </div>

          <strong>Solicitud registrada:</strong>
          <p>{state.original_text}</p>

          <strong>Resumen del problema:</strong>
          <p>{state.summary}</p>
        </div>

        <div className="buttons">
          {/* 🟢 Crear Ticket → mostrar anuncio */}
          <button className="primary" onClick={() => setShowModal(true)}>
            Crear Ticket
          </button>

          {/* 🔴 Cancelar → ir al inicio */}
          <button
            className="secondary"
            onClick={() => navigate("/")}
          >
            Cancelar
          </button>
        </div>
      </main>

      {/* 🌟 MODAL BONITO 🌟 */}
      {showModal && (
        <ConfirmModal onClose={() => setShowModal(false)} />
      )}
    </>
  );
}
