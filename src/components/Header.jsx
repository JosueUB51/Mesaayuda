import "../styles/layout.css";
import logo from "../assets/mesaayuda.png";

export default function Header({ user }) {
  return (
    <header className="header">
      <div className="logos">
        <img src={logo} alt="Mesa de Ayuda" />
      </div>
      {user && <span className="user">Bienvenido, {user}</span>}
    </header>
  );
}
