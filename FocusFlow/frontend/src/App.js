import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import FocusSession from './pages/FocusSession';
import Analytics from './pages/Analytics';
import BlockDistractions from './pages/BlockDistractions';
import Login from './pages/Login';
import Signup from './pages/Signup';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/focus" element={<FocusSession />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/block" element={<BlockDistractions />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;

