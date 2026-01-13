import { useState, useEffect, useRef } from 'react'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import './index.css'

const API_URL = "http://localhost:8000/api";

function App() {
  const [view, setView] = useState('dashboard');
  const [role, setRole] = useState('guest'); // guest, admin, teacher, student
  const [stats, setStats] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState("");
  const tableRef = useRef(null);

  useEffect(() => {
    fetchStats();
    fetchSchedule();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_URL}/stats`);
      const data = await res.json();
      setStats(data);
    } catch (e) {
      console.error("Error fetching stats:", e);
    }
  };

  const fetchSchedule = async () => {
    try {
      const res = await fetch(`${API_URL}/schedule`);
      const data = await res.json();
      setSchedule(data);
    } catch (e) {
      console.error("Error fetching schedule:", e);
    }
  };

  const generateSchedule = async () => {
    setLoading(true);
    setNotification("Génération en cours...");
    try {
      const res = await fetch(`${API_URL}/generate`);
      const data = await res.json();
      if (data.status === 'success') {
        setNotification(`Succès ! ${data.count} créneaux générés.`);
        fetchStats();
        fetchSchedule();
      } else {
        setNotification(`Erreur: ${data.message}`);
      }
    } catch (e) {
      setNotification("Erreur de connexion au serveur.");
    }
    setLoading(false);
  };

  const exportToExcel = () => {
    const ws = XLSX.utils.json_to_sheet(schedule);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "EmploiDuTemps");
    XLSX.writeFile(wb, "emploi_du_temps.xlsx");
  };

  const exportToPDF = () => {
    const doc = new jsPDF('l', 'mm', 'a4');
    doc.text("Emploi du Temps Global", 14, 15);

    // Simple way for demo: take snapshot of table
    html2canvas(tableRef.current).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const imgProps = doc.getImageProperties(imgData);
      const pdfWidth = doc.internal.pageSize.getWidth() - 28;
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      doc.addImage(imgData, 'PNG', 14, 25, pdfWidth, pdfHeight);
      doc.save("emploi_du_temps.pdf");
    });
  };

  const exportToImage = () => {
    html2canvas(tableRef.current).then(canvas => {
      const link = document.createElement('a');
      link.download = 'emploi_du_temps.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  };

  return (
    <div className="container">
      {/* Header */}
      <header className="glass glass-panel animate-fade-in" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem' }}>📅 Université - Gestion EDT</h1>
          <p style={{ margin: 0, opacity: 0.7 }}>Interface Moderne & Fluide</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className={`glass-btn ${view === 'dashboard' ? 'primary' : ''}`} onClick={() => setView('dashboard')}>Tableau de Bord</button>
          <button className={`glass-btn ${view === 'schedule' ? 'primary' : ''}`} onClick={() => setView('schedule')}>Emploi du Temps</button>
          <button className={`glass-btn ${view === 'admin' ? 'primary' : ''}`} onClick={() => setView('admin')}>Administration</button>
        </div>
      </header>

      {/* Main Content */}
      <main className="animate-fade-in" style={{ marginTop: '20px' }}>

        {notification && (
          <div className="glass glass-panel" style={{ background: 'rgba(76, 209, 55, 0.2)', marginBottom: '20px', padding: '10px 20px' }}>
            {notification}
            <button onClick={() => setNotification("")} style={{ float: 'right', background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>✕</button>
          </div>
        )}

        {view === 'dashboard' && stats && (
          <div className="glass glass-panel">
            <h2>📊 Vue d'ensemble</h2>
            <div className="dashboard-grid">
              <div className="glass glass-panel stat-card">
                <h3>Enseignants</h3>
                <div className="stat-value">{stats.teachers}</div>
              </div>
              <div className="glass glass-panel stat-card">
                <h3>Modules</h3>
                <div className="stat-value">{stats.modules}</div>
              </div>
              <div className="glass glass-panel stat-card">
                <h3>Salles</h3>
                <div className="stat-value">{stats.rooms}</div>
              </div>
              <div className="glass glass-panel stat-card">
                <h3>Séances Placées</h3>
                <div className="stat-value">{schedule.length}</div>
              </div>
            </div>
          </div>
        )}

        {view === 'admin' && (
          <div className="glass glass-panel">
            <h2>🛠️ Administration</h2>
            <p>Gérez la génération de l'emploi du temps.</p>
            <div style={{ marginTop: '20px' }}>
              <button disabled={loading} onClick={generateSchedule} className="glass-btn primary" style={{ fontSize: '1.2rem', padding: '15px 30px' }}>
                {loading ? "⏳ Génération en cours..." : "🚀 Générer l'Emploi du Temps"}
              </button>
            </div>
          </div>
        )}

        {view === 'schedule' && (
          <div className="glass glass-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2>📅 Emploi du Temps Global</h2>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={exportToExcel} className="glass-btn" style={{ background: '#27ae60' }}>📊 Excel</button>
                <button onClick={exportToPDF} className="glass-btn" style={{ background: '#c0392b' }}>📕 PDF</button>
                <button onClick={exportToImage} className="glass-btn" style={{ background: '#8e44ad' }}>🖼️ Image</button>
              </div>
            </div>
            <div style={{ overflowX: 'auto' }} ref={tableRef}>
              <table>
                <thead>
                  <tr>
                    <th>Jour</th>
                    <th>Heure</th>
                    <th>Module</th>
                    <th>Enseignant</th>
                    <th>Salle</th>
                    <th>Groupe</th>
                  </tr>
                </thead>
                <tbody>
                  {schedule.length === 0 ? (
                    <tr><td colSpan="6" style={{ textAlign: 'center' }}>Aucune donnée. Générez l'EDT d'abord.</td></tr>
                  ) : (
                    schedule.slice(0, 100).map((s, i) => ( // Limit to 100 for perf in demo
                      <tr key={i}>
                        <td>{s.jour}</td>
                        <td>{s.debut} - {s.fin}</td>
                        <td style={{ fontWeight: 'bold' }}>{s.module}</td>
                        <td>{s.enseignant}</td>
                        <td><span style={{ background: '#0f3460', padding: '2px 8px', borderRadius: '4px' }}>{s.salle}</span></td>
                        <td>{s.groupe}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
              {schedule.length > 100 && <p style={{ textAlign: 'center', marginTop: '10px', opacity: 0.7 }}>Affichage des 100 premières séances...</p>}
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App
