import "../styles/confirm-modal.css";

export default function ConfirmModal({ onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-check">✔</div>

        <h2>Ticket creado correctamente</h2>
        <p>Tu solicitud fue registrada con éxito.</p>

        <button onClick={onClose}>Aceptar</button>
      </div>
    </div>
  );
}
