import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreateTicket from "./pages/CreateTicket";
import TicketSummary from "./pages/TicketSummary";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreateTicket />} />
        <Route path="/summary" element={<TicketSummary />} />
      </Routes>
    </BrowserRouter>
  );
}
